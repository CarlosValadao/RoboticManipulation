import sys
from time import sleep
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtGui import QPainter, QColor
import SupervisorClient
from threading import Thread
from constants import NXT_BLUETOOTH_MAC_ADDRESS
from os import environ

# thread para enviar as coordenadas do robô

class RobotPositionThread(QThread):
    position_updated = pyqtSignal(int, int, int)

    def run(self):
        while True:
            # formato 'new_x;new_y;regiao'
            received_messages = supervisor_client.get_data_msgs()
            if(received_messages):
                for data_msg in received_messages:
                    (new_x, new_y, region) = data_msg
                    self.position_updated.emit(new_x, new_y, region)
                    
class RobotCommThread(QThread):
    control_signal = pyqtSignal(int)
    def run(self):
        while True:
            received_comms = supervisor_client.get_response_msgs()
            if received_comms:
            	for comm in received_comms:
            		self.control_signal.emit(comm)
            	

class RobotArea(QFrame):
    def __init__(self):
        super().__init__()
        self.robot_position = [30, 40]  # posição inicial do robô
        self.rastro = []  # lista para armazenar o rastro do robô
        self.setFixedSize(540, 360)  # Definindo um tamanho fixo para a área do robô

    def update_robot_position(self, new_position):
        self.robot_position = new_position
        self.rastro.append(new_position)  # adiciona a nova posição ao rastro
        self.update()  # atualiza a área do robô

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # cor do fundo
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, self.width(), self.height())

        # desenha as áreas de recarga e estoque
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        
        # recarga (esquerda)
        painter.drawRect(1, 1, 80, 358)

        # estoque (direita)
        painter.drawRect(self.width() - 81, 1, 80, 358)

        # desenhar as bancadas
        square_width = 60
        square_height = 60
        offset_x = 165
        offset_y = 1
        spacing = 89
        
        for row in range(3):
            for col in range(2):
                x = offset_x + col * (square_width + spacing)
                y = offset_y + row * (square_height + spacing)
                painter.setPen(Qt.black)
                painter.drawRect(x, y, square_width, square_height)

        # desenhar o rastro do robô
        painter.setBrush(QColor(200, 0, 0, 150))  # cor do rastro com transparência
        for pos in self.rastro:
            painter.drawEllipse(pos[0], pos[1], 5, 5)  # desenha cada posição do rastro

        # desenhar o robô
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(self.robot_position[0], self.robot_position[1], 20, 20)


class RobotInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Controle do Robô')
        self.setFixedSize(800, 400)  # Definindo um tamanho fixo para a janela principal

        # layout principal
        self.main_layout = QHBoxLayout()

        # cria um painel lateral para o botão e as coordenadas
        self.control_panel = QFrame(self)
        self.control_panel.setFixedWidth(200)
        self.control_layout = QVBoxLayout()

        # botão para ativar o robô
        self.button = QPushButton('Ativar Robô', self)
        self.button.clicked.connect(self.toggle_robot)
        self.control_layout.addWidget(self.button)
        
        # botao para fechar a janela
        self.quit_button = QPushButton('Sair', self)
        self.quit_button.clicked.connect(self.close_application)

        self.control_layout.addWidget(self.quit_button)

        # exibe a região do robô
        self.region_label = QLabel('Região: Base', self)
        self.control_layout.addWidget(self.region_label)

        # exibe as coordenadas do robô
        self.coordinates_label = QLabel('Coordenadas: (150, 150)', self)
        self.control_layout.addWidget(self.coordinates_label)

        # layout do painel de controle
        self.control_panel.setLayout(self.control_layout)
        self.main_layout.addWidget(self.control_panel)

        # área do robô
        self.robot_area = RobotArea()
        self.robot_area.setStyleSheet("background-color: white;")
        self.main_layout.addWidget(self.robot_area)

        self.setLayout(self.main_layout)

        self.robot_active = False

        # cria a thread de posição
        self.position_thread = RobotPositionThread()
        self.position_thread.position_updated.connect(self.update_robot_position)
        
        # cria a thread de comunicação
        self.comm_thread = RobotCommThread()
        self.comm_thread.control_signal.connect(self.control_interface)

    def toggle_robot(self):
        self.comm_thread.start()
        if not self.robot_active:
            supervisor_client.send_message(request_code=0)
            
    def control_interface(self, control):
        if control == 3:
            self.robot_active = True
            self.button.setText('Robô Ativado')
            self.button.setEnabled(False)
            self.robot_area.rastro.clear()
            self.position_thread.start()
        elif control == 2:
            self.button.setText('Ativar Robô')
            self.button.setEnabled(True)
            self.position_thread.terminate()
            self.robot_active = False
            

    def update_robot_position(self, new_x, new_y, regiao):
        # limita a posição do robô
        robot_area_width = self.robot_area.width()
        robot_area_height = self.robot_area.height()

        # garante que o robô não saia dos limites da área
        new_x = max(0, min(new_x + 30, robot_area_width - 20))  # -20 para manter o círculo visível
        new_y = max(0, min(new_y + 40, robot_area_height - 20))

        # atualiza a posição do robô na área
        self.robot_area.update_robot_position([new_x, new_y])

        #if regiao == 0:
            #self.robot_area.update_robot_position([30, 270])
        #elif regiao == 1:
            #self.robot_area.update_robot_position([260, 170])
        #else:
            #self.robot_area.update_robot_position([490, 270])

        # atualiza o campo de coordenadas com a nova posição do robô
        self.coordinates_label.setText(f'Coordenadas: ({new_x}, {new_y})')
        if regiao == 0:
            self.region_label.setText('Região: Base')
        elif regiao == 1:
            self.region_label.setText('Região: Pátio')
        elif regiao == 2:
            self.region_label.setText('Região: Estoque')
        else:
            self.region_label.setText('Região: Desconhecida')

    def close_application(self):
        print("Aplicação fechando...")
        self.close()  # Fecha a janela

if __name__ == '__main__':
    environ['QT_QPA_PLATFORM'] = 'xcb'
    supervisor_client = SupervisorClient.SupervisorClient(NXT_BLUETOOTH_MAC_ADDRESS)
    supervisor_client.catch_all_messages()
    app = QApplication(sys.argv)
    window = RobotInterface()
    window.show()
    sys.exit(app.exec_())
