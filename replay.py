import sys
from PyQt5.QtWidgets import QApplication, QWidget

from config import WINDOW_HEIGHT, WINDOW_WIDTH

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    w.setWindowTitle('my first window')
    w.show()

    sys.exit(app.exec_())