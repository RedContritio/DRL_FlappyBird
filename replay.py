import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui
import numpy as np

from config import FPS, WINDOW_HEIGHT, WINDOW_SIZE, WINDOW_WIDTH
from game import Game
from offscreen import render

game = Game(WINDOW_SIZE)

def timerEvent():
    global label_image
    image_data = render(game)
    image = QtGui.QImage(image_data, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH * 4, QtGui.QImage.Format_RGBA8888)

    pixmap = QtGui.QPixmap.fromImage(image)
    label_image.setPixmap(pixmap)

def clickEvent(e: QtGui.QMouseEvent):
    print('click')
    pass

app = QApplication(sys.argv)


label_image = QtWidgets.QLabel()
label_image.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
label_image.setWindowTitle('flappy Bird Replay')
label_image.show()
timerEvent()

label_image.mousePressEvent = clickEvent

timer = QtCore.QTimer()
timer.timeout.connect(timerEvent)
timer.start(1000 / FPS)

sys.exit(app.exec_())