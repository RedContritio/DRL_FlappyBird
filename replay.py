import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui
import numpy as np

from config import FPS, WINDOW_HEIGHT, WINDOW_WIDTH

def timerEvent():
    pass

def clickEvent(e: QtGui.QMouseEvent):
    print('click')
    pass

app = QApplication(sys.argv)

image_data = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.ubyte)
image_data[:, :, 1] = 255
image = QtGui.QImage(image_data, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH * 3, QtGui.QImage.Format_RGB888)

pixmap = QtGui.QPixmap.fromImage(image)

label_image = QtWidgets.QLabel()
label_image.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
label_image.setPixmap(pixmap)
label_image.show()

label_image.mousePressEvent = clickEvent

timer = QtCore.QTimer()
timer.timeout.connect(timerEvent)
timer.start(1000 / FPS)

sys.exit(app.exec_())