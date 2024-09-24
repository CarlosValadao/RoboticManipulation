#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPainter>
#include <QTimer>
#include <QVector>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    void paintEvent(QPaintEvent *event) override;

public slots:
    void activateRobot();
    void updateTrajectory();
    void receiveCoordinates(int x, int y);

private:
    QPushButton *activateButton;
    QVector<QPoint> trajectory;
    QTimer *timer;
    QLabel *infoLabel; // Adicionado para informações
    QLabel *positionLabel; // Label para exibir a posição atual do robô
    bool robotActivated;
};

#endif // MAINWINDOW_H
