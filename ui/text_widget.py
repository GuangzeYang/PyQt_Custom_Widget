import sys
import enum
import time

from PyQt5.QtCore import QLine, QTime, QTimer, QAbstractItemModel
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QGraphicsDropShadowEffect, QApplication, QWidget, QHBoxLayout, QVBoxLayout, \
    QListWidget, QListWidgetItem, QListView, QCheckBox, QLabel


class ShadowColor(enum.Enum):
    GRAY = (176, 176, 176)
    GREEN = (77, 255, 77)
    RED = (255, 77, 77)


class LineEditVerify(QLineEdit):
    """
    可改变边界阴影颜色的输入框。验证时，根据结果手动调用toggle_color切换颜色.
    默认色为 灰色
    """
    qss_style = """
    QLineEdit{
        border: 1px solid #A9A9A9;
        border-radius: 5%;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(self.qss_style)
        self.toggle_cache = None
        self.setup_ui()
        pass

    def setup_ui(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setOffset(0, 0)
        self.shadow_effect.setColor(QColor(*ShadowColor.GRAY.value))
        # QTimer.singleShot(1000, lambda: self.toggle_color(ShadowColor.RED))
        # QTimer.singleShot(2000, lambda: self.toggle_color(ShadowColor.RED))

        self.setGraphicsEffect(self.shadow_effect)
        pass

    def toggle_color(self, color: ShadowColor):
        if not isinstance(color, ShadowColor):
            return
        blus_radius = 20 if color != ShadowColor.GRAY else 5
        self.shadow_effect.setBlurRadius(blus_radius)
        if color == self.toggle_cache:
            QTimer.singleShot(50, lambda: self.shadow_effect.setColor(QColor(*ShadowColor.GRAY.value)))
            QTimer.singleShot(450, lambda: self.shadow_effect.setColor(QColor(*color.value)))
        else:
            self.shadow_effect.setColor(QColor(*color.value))
            self.toggle_cache = color
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: white;")
    window.resize(500, 500)
    vl_window = QVBoxLayout(window)
    line_edit_1 = LineEditVerify()
    line_edit_2 = QLineEdit()
    vl_window.addStretch(1)
    vl_window.addWidget(line_edit_1)
    vl_window.addWidget(line_edit_2)
    vl_window.addStretch(1)
    window.show()
    sys.exit(app.exec_())
    pass
