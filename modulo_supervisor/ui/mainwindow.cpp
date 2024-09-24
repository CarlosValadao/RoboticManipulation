#include "MainWindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), activateButton(new QPushButton("Ativar Robô", this)), timer(new QTimer(this)), infoLabel(new QLabel(this)), positionLabel(new QLabel(this)), robotActivated(false) {

    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    // Configuração da janela e dos widgets
    setWindowTitle("Controle do Robô");
    setFixedSize(800, 600);
    setStyleSheet("background-color: black; color: white; font-family: 'Courier New';");

    // Configuração do botão
    activateButton->setGeometry(10, 10, 150, 30);
    activateButton->setStyleSheet("background-color: gray; color: white; font-size: 14px;");

    // Configuração do label de informações
    infoLabel->setGeometry(10, 50, 300, 30);
    infoLabel->setText("Pressione o botão para ativar o robô.");

    // Configuração do label para exibir a posição do robô
    positionLabel->setGeometry(180, 10, 200, 30);
    positionLabel->setStyleSheet("color: yellow; font-size: 14px;");
    positionLabel->setText("Posição: (0, 0)"); // Valor inicial

    // Conexão do botão de ativação
    connect(activateButton, &QPushButton::clicked, this, &MainWindow::activateRobot);

    timer = new QTimer(this);
    // Conexão do temporizador para atualizar a posição do robô
    connect(timer, &QTimer::timeout, this, &MainWindow::updateTrajectory);
}

void MainWindow::paintEvent(QPaintEvent *event) {
    QMainWindow::paintEvent(event);

    // Pintura da trajetória
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.setPen(QPen(Qt::green, 3)); // Define a cor e a espessura da linha

    // Desenhar a trajetória (certifique-se de que há mais de um ponto)
    if (trajectory.size() > 1) {
        for (int i = 1; i < trajectory.size(); ++i) {
            painter.drawLine(trajectory[i - 1], trajectory[i]);
        }
    }
}

void MainWindow::activateRobot() {
    robotActivated = !robotActivated;

    if (robotActivated) {
        activateButton->setText("Desativar Robô");
        trajectory.clear();  // Limpa a trajetória anterior
        timer->start(500);   // Atualiza a cada 500ms (simulando movimento)
    } else {
        activateButton->setText("Ativar Robô");
        timer->stop();
    }
}

void MainWindow::updateTrajectory() {
    if (!robotActivated) return;

    // Simulando a recepção de novas coordenadas
    float lastX = trajectory.isEmpty() ? 200 : trajectory.last().x();
    float lastY = trajectory.isEmpty() ? 200 : trajectory.last().y();

    float newX = lastX + (std::rand() % 2 == 0 ? -10 : 10);  // Movimento aleatório fixo no eixo X
    float newY = lastY + (std::rand() % 2 == 0 ? -10 : 10);  // Movimento aleatório fixo no eixo Y


    // Adiciona o novo ponto à lista de coordenadas
    trajectory.append(QPoint(newX, newY));

    // Atualizar o texto da label com a posição do robô
    positionLabel->setText(QString("Posição: (%1, %2)").arg(newX).arg(newY));

    // Atualiza a tela para desenhar a nova posição
    update();
}

void MainWindow::receiveCoordinates(int x, int y) {
    trajectory.append(QPoint(x, y));
    update(); // Atualiza a tela
}
