import sys
from time import sleep
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtGui import QPainter, QColor
import SupervisorClient
from threading import Thread
from constants import NXT_BLUETOOTH_MAC_ADDRESS
from os import environ

"""
class Position(Enum):
    BASE = "Base"
    PATIO = "Pátio"
    ESTOQUE = "Estoque"

def checkArea(y):
    if 1 <= y < :
        return Position.BASE
    elif  <= y < :
        return Position.PATIO
    elif <= y < :
        return Position.ESTOQUE
    else:
        return "ERROR"
"""

# thread para enviar as coordenadas do robô


class RobotPositionThread(QThread):
    position_updated = pyqtSignal(int, int)

    def run(self):
        while True:
            # formato 'new_x;new_y'
            received_messages = supervisor_client.get_data_msgs()
            if(received_messages):
                (new_x, new_y) = received_messages[-1]
                self.position_updated.emit(new_x, new_y)

class RobotArea(QFrame):
    def __init__(self):
        super().__init__()
        self.robot_position = [35, 60]  # posição inicial do robô

    def update_robot_position(self, new_position):
        self.robot_position = new_position
        self.update()  # atualiza a posição do robô

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
        painter.drawRect(20, 50, 50, 300)

        # estoque (direita)
        painter.drawRect(self.width() - 70, 50, 50, 300)

        # desenhar as bancadas
        square_width = 80
        square_height = 80
        offset_x = 150
        offset_y = 50
        spacing = 20
        
        for row in range(3):
            for col in range(2):
                x = offset_x + col * (square_width + spacing)
                y = offset_y + row * (square_height + spacing)
                painter.setPen(Qt.black)
                painter.drawRect(x, y, square_width, square_height)

        # desenhar o robô
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(self.robot_position[0], self.robot_position[1], 20, 20)


class RobotInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Controle do Robô')
        self.setGeometry(100, 100, 700, 400)

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

    def toggle_robot(self):
        if not self.robot_active:
            self.robot_active = True
            self.button.setText('Desativar Robô')
            supervisor_client.send_message('1;1')
            self.position_thread.start()
        else:
            self.robot_active = False
            self.button.setText('Ativar Robô')
            supervisor_client.send_message('0')
            self.position_thread.terminate()

    def update_robot_position(self, new_x, new_y):
        # limita a posição do robô
        robot_area_width = self.robot_area.width()
        robot_area_height = self.robot_area.height()

        # garante que o robô não saia dos limites da área
        new_x = max(0, min(new_x, robot_area_width - 20))  # -20 para manter o círculo visível
        new_y = max(0, min(new_y, robot_area_height - 20))

        # atualiza a posição do robô na área
        self.robot_area.update_robot_position([new_x, new_y])

        # atualiza o campo de coordenadas com a nova posição do robô
        self.coordinates_label.setText(f'Coordenadas: ({new_x}, {new_y})')


if __name__ == '__main__':
    environ['QT_QPA_PLATFORM'] = 'xcb'
    supervisor_client = SupervisorClient.SupervisorClient(NXT_BLUETOOTH_MAC_ADDRESS)
    supervisor_client.catch_all_messages()
    app = QApplication(sys.argv)
    window = RobotInterface()
    window.show()
    sys.exit(app.exec_())