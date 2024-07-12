from PyQt5.QtCore import Qt, QRect, QVariantAnimation
from PyQt5.QtGui import QPainter, QFont, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget, QPushButton


class SwitchButton(QWidget):
    '''
    switch开关， state=True 开启
    '''
    def __init__(self, parent=None):
        super(SwitchButton, self).__init__(parent)
        # 圆钮移动时的坐标，初始化为3
        self.rect_x_round = 3
        self.is_animating = False
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # SwitchButtonstate：True is ON，False is OFF
        self.state = False

    def mousePressEvent(self, event):
        '''
        set click event for state change
        '''
        if self.is_animating:
            event.ignore()
            return
            pass

        self.is_animating = True
        super(SwitchButton, self).mousePressEvent(event)
        self.state = False if self.state else True
        self.rect_x_range = self.width() - (self.height()-2*3)
        self.anni = QVariantAnimation(self)
        self.anni.valueChanged.connect(self.onValueChanged)
        self.anni.finished.connect(self.onFinished)
        self.anni.setDuration(200)
        self.anni.setStartValue(self.rect_x_round)
        self.anni.setEndValue(abs(self.rect_x_round-self.rect_x_range))
        self.anni.start()

    def onValueChanged(self, value):
        self.rect_x_property = value

    def onFinished(self):
        self.is_animating = False
        pass

    @property
    def rect_x_property(self):
        return self.rect_x_round

    @rect_x_property.setter
    def rect_x_property(self, value):
        self.rect_x_round = value
        self.update()

    def paintEvent(self, event):
        '''Set the button'''
        super(SwitchButton, self).paintEvent(event)
        # Create a renderer and set anti-aliasing and smooth transitions
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform, True)
        # Defining font styles
        font = QFont("Arial")
        font.setPixelSize(self.height()//2)
        painter.setFont(font)
        # SwitchButton state：ON
        if self.state:
            # Drawing background
            painter.setPen(Qt.NoPen)
            brush = QBrush(QColor('green'))
            painter.setBrush(brush)
            # Top left corner of the rectangle coordinate
            rect_x = 0
            rect_y = 0
            rect_width = self.width()
            rect_height = self.height()
            rect_radius = self.height()//2
            painter.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, rect_radius, rect_radius)
            # Drawing slides circle
            pen = QPen(QColor('white'))
            pen.setWidth(1)
            painter.setPen(pen)
            brush.setColor(QColor('#ffffff'))
            painter.setBrush(brush)
            # Phase difference pixel point
            # Top left corner of the rectangle coordinate
            diff_pix = 3
            rect_y = diff_pix
            rect_width = (self.height()-2*diff_pix)
            rect_height = (self.height()-2*diff_pix)
            rect_radius = (self.height()-2*diff_pix)//2
            painter.drawRoundedRect(self.rect_x_round, rect_y, rect_width, rect_height, rect_radius, rect_radius)

            # ON txt set
            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(int(self.height()/3), int(self.height()/3.5), 50, 20), Qt.AlignLeft, 'ON')
        # SwitchButton state：OFF
        else:
            # Drawing background
            painter.setPen(Qt.NoPen)
            brush = QBrush(QColor('#808080'))
            painter.setBrush(brush)
            # Top left corner of the rectangle coordinate
            rect_x = 0
            rect_y = 0
            rect_width = self.width()
            rect_height = self.height()
            rect_radius = self.height()//2
            painter.setPen(QColor('white'))
            painter.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, rect_radius, rect_radius)
            # Drawing slides circle

            pen = QPen(QColor('white'))
            pen.setWidth(1)
            painter.setPen(pen)
            brush.setColor(QColor('#ffffff'))
            painter.setBrush(brush)
            # Phase difference pixel point
            diff_pix = 3
            # Top left corner of the rectangle coordinate
            rect_y = diff_pix
            rect_width = (self.height()-2*diff_pix)
            rect_height = (self.height()-2*diff_pix)
            rect_radius = (self.height()-2*diff_pix)//2
            painter.drawRoundedRect(self.rect_x_round, rect_y, rect_width, rect_height, rect_radius, rect_radius)

            # OFF txt set
            painter.setPen(QPen(QColor('#D3D3D3')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(int(self.width()*1/2), int(self.height()/3.5), 50, 20), Qt.AlignLeft, 'OFF')


class PushButtonShadow(QPushButton):
    def __init__(self):
        super().__init__()
        pass