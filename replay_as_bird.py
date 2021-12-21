import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui
import numpy as np
import os
import cv2

from config import FPS, WINDOW_HEIGHT, WINDOW_SIZE, WINDOW_WIDTH
from game import Game
from offscreen import render

_image_togray = lambda img: cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
_image_resize = lambda img: cv2.resize(img, (80, 80))
_image_threshold = lambda img: cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)[1]
image_preprocess = lambda img: _image_threshold(_image_togray(_image_resize(img)))


SAVE_DIR = os.path.join('log', 'actions')
SAVE_LISTS = os.listdir(SAVE_DIR)
SAVE_LISTS.sort()

if len(SAVE_LISTS) > 0:
    with open(os.path.join(SAVE_DIR, SAVE_LISTS[-1]), 'r') as f:
        seed = f.readline()[:-1]
        operations = eval(f.readline())

game = Game(WINDOW_SIZE, True)
game.reset(seed)
current_frame = 0

def timerEvent():
    global label_image, current_frame
    image_data = render(game)
    image_data = image_preprocess(image_data)
    h, w = image_data.shape[:2]
    c = 1 if len(image_data.shape) < 3 else image_data.shape[2]
    mode = QtGui.QImage.Format_RGBA8888 if c == 4 else QtGui.QImage.Format_Grayscale8
    image = QtGui.QImage(image_data, w, h, w * c, mode)
    # image = QtGui.QImage(image_data, w, h, w * c, QtGui.QImage.Format_Grayscale8)

    pixmap = QtGui.QPixmap.fromImage(image)
    label_image.setPixmap(pixmap)

    if game.ready:
        game.start()
        current_frame = 0
    elif game.running:
        if len(operations) > current_frame:
            for _ in range(operations[current_frame]):
                game.click()
        current_frame += 1
        game.update()


def clickEvent(e: QtGui.QMouseEvent):
    if game.dead:
        game.reset(seed)

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