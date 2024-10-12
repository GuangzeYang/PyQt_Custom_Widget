import functools
import sys

from PyQt5.QtCore import Qt, QRect, QVariantAnimation, QPropertyAnimation, QSize, QParallelAnimationGroup, pyqtProperty, \
    QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QBrush, QColor, QPen, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QGraphicsDropShadowEffect, QApplication, QHBoxLayout, QVBoxLayout, \
    QLayout


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
        self.rect_x_range = self.width() - (self.height() - 2 * 3)
        self.anni = QVariantAnimation(self)
        self.anni.valueChanged.connect(self.onValueChanged)
        self.anni.finished.connect(self.onFinished)
        self.anni.setDuration(200)
        self.anni.setStartValue(self.rect_x_round)
        self.anni.setEndValue(abs(self.rect_x_round - self.rect_x_range))
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
        font.setPixelSize(self.height() // 2)
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
            rect_radius = self.height() // 2
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
            rect_width = (self.height() - 2 * diff_pix)
            rect_height = (self.height() - 2 * diff_pix)
            rect_radius = (self.height() - 2 * diff_pix) // 2
            painter.drawRoundedRect(self.rect_x_round, rect_y, rect_width, rect_height, rect_radius, rect_radius)

            # ON txt set
            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(int(self.height() / 3), int(self.height() / 3.5), 50, 20), Qt.AlignLeft, 'ON')
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
            rect_radius = self.height() // 2
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
            rect_width = (self.height() - 2 * diff_pix)
            rect_height = (self.height() - 2 * diff_pix)
            rect_radius = (self.height() - 2 * diff_pix) // 2
            painter.drawRoundedRect(self.rect_x_round, rect_y, rect_width, rect_height, rect_radius, rect_radius)

            # OFF txt set
            painter.setPen(QPen(QColor('#D3D3D3')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(int(self.width() * 1 / 2), int(self.height() / 3.5), 50, 20), Qt.AlignLeft, 'OFF')


class ShadowPushButton(QPushButton):
    """阴影按钮"""

    def __init__(self):
        super().__init__()
        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)  # 阴影的模糊半径
        shadow.setOffset(5, 5)  # 阴影偏移量
        shadow.setColor(QColor(0, 0, 0, 160))  # 阴影颜色（带透明度）
        self.setGraphicsEffect(shadow)
        pass


class HoverLargeButton(QPushButton):
    """
    悬浮变大按钮
    Note：
        1.在布局中使用时，需要指定该按钮的左右限制（添加控件或加拉伸）。亦或可以设置布局的约束方式 hl_window.setSizeConstraint(QLayout.SetNoConstraint)
    """
    mouse_enter = pyqtSignal(object)
    mouse_leave = pyqtSignal(object)

    def __init__(self, *args, zoom_factor: float = 1.2, zoom_duration: int = 80, **kwargs):
        super().__init__(*args, **kwargs)
        self._zoom_factor = zoom_factor
        self._zoom_duration = zoom_duration
        self._geometry_before_zoom = self.geometry()
        self._font_size_before_zoom = self.font().pointSizeF()
        QTimer.singleShot(100, self.update_compont_info)
        self._is_use_size_hint = True

        self.zoom_in_geometry = QPropertyAnimation(self, b'cus_geometry')
        self.zoom_in_font = QPropertyAnimation(self, b'font_size')
        self.zoom_in_geometry.setDuration(self._zoom_duration)
        self.zoom_in_font.setDuration(self._zoom_duration)

        self.zoom_out_geometry = QPropertyAnimation(self, b'cus_geometry')
        self.zoom_out_font = QPropertyAnimation(self, b'font_size')
        self.zoom_out_geometry.setDuration(self._zoom_duration)
        self.zoom_out_font.setDuration(self._zoom_duration)

        self._is_zoom_in_finished = True
        self.zoom_in_group = QParallelAnimationGroup()
        self.zoom_in_group.finished.connect(self.zoom_in_finish)
        self.zoom_in_group.addAnimation(self.zoom_in_geometry)
        self.zoom_in_group.addAnimation(self.zoom_in_font)

        self._is_zoom_out_finished = True
        self.zoom_out_group = QParallelAnimationGroup()
        self.zoom_out_group.finished.connect(self.zoom_out_finish)
        self.zoom_out_group.addAnimation(self.zoom_out_geometry)
        self.zoom_out_group.addAnimation(self.zoom_out_font)
        pass

    def enterEvent(self, event):
        self.mouse_enter.emit(self)
        # 更新当前控件大小
        if self._is_zoom_out_finished:
            self.update_compont_info()
        else:
            self.zoom_out_group.stop()
            self._is_zoom_out_finished = True
        self._is_use_size_hint = False

        # 形状放大。不关心动画的起始值是什么，只在乎动画的结束值必须是所有动画开始前的控件大小的zoom_factor倍
        start_rect = self.geometry()
        stop_rect = self.cal_zoom_in_rect()
        print('enterEvent', start_rect, stop_rect)
        self.zoom_in_geometry.setStartValue(start_rect)
        self.zoom_in_geometry.setEndValue(stop_rect)

        # 字体放大。
        start_font_size = self.font().pointSizeF()
        stop_font_size = self._font_size_before_zoom * self._zoom_factor
        self.zoom_in_font.setStartValue(start_font_size)
        self.zoom_in_font.setEndValue(stop_font_size)



        self.zoom_in_group.start()
        self._is_zoom_in_finished = False
        pass

    def leaveEvent(self, event):
        self.mouse_leave.emit(self)
        # 形状缩小。巧了，这个只关注动画的最初值
        start_rect = self.geometry()
        stop_rect = self._geometry_before_zoom
        self.zoom_out_geometry.setStartValue(start_rect)
        self.zoom_out_geometry.setEndValue(stop_rect)

        # 字体缩小。
        start_font_size = self.font().pointSizeF()
        stop_font_size = self._font_size_before_zoom
        self.zoom_out_font.setStartValue(start_font_size)
        self.zoom_out_font.setEndValue(stop_font_size)

        if not self._is_zoom_in_finished:
            self.zoom_in_group.stop()
            self._is_zoom_in_finished = True
        self._is_use_size_hint = False
        self.zoom_out_group.start()
        self._is_zoom_out_finished = False
        pass

    def sizeHint(self):
        if self._is_use_size_hint:
            return super().sizeHint()
        print('@', self.change_value.size())
        return self.change_value.size()

    @property
    def zoom_duration(self):
        return self._zoom_duration

    @zoom_duration.setter
    def zoom_duration(self, value):
        self._zoom_duration = value
        self.zoom_in_geometry.setDuration(self._zoom_duration)
        self.zoom_out_geometry.setDuration(self._zoom_duration)

    @pyqtProperty(float)
    def font_size(self):
        return self.font().pointSizeF()

    @font_size.setter
    def font_size(self, value):
        font = self.font()
        font.setPointSizeF(value)
        self.setFont(font)

    @pyqtProperty(QRect)
    def cus_geometry(self):
        return self.geometry()

    @cus_geometry.setter
    def cus_geometry(self, value):
        self.change_value = value
        self.setGeometry(self.change_value)

    def zoom_out_finish(self):
        self._is_zoom_out_finished = True

    def zoom_in_finish(self):
        self._is_zoom_in_finished = True

    def cal_zoom_in_rect(self):
        center_point = self._geometry_before_zoom.center()
        end_width = self._geometry_before_zoom.width() * self._zoom_factor
        end_height = self._geometry_before_zoom.height() * self._zoom_factor
        print('cal_zoom_in_rect', center_point, end_width, end_height)
        return QRect(
            int(center_point.x() - end_width // 2),  # 新左上角 x 坐标
            int(center_point.y() - end_height // 2),  # 新左上角 y 坐标
            int(end_width),  # 新宽度
            int(end_height)  # 新高度
        )

    def update_compont_info(self):
        # 更新当前控件的几何信息
        self._geometry_before_zoom = self.geometry()
        self._font_size_before_zoom = self.font().pointSizeF()


class HoverCircularButton(QPushButton):
    """悬浮变大按钮——圆形。图标跟随变大"""
    mouse_enter = pyqtSignal(object)
    mouse_leave = pyqtSignal(object)

    def __init__(self, *args, zoom_factor: float = 1.3, zoom_duration: int = 80, **kwargs):
        super().__init__(*args, **kwargs)
        self._zoom_factor = zoom_factor
        self._zoom_duration = zoom_duration
        self._geometry_before_zoom = self.geometry()
        self._font_size_before_zoom = self.font().pointSizeF()
        self._icon_size_before_zoom = self.iconSize()
        QTimer.singleShot(100, self.update_compont_info)
        self._is_use_size_hint = True
        self.marker = False

        self.zoom_in_geometry = QPropertyAnimation(self, b'cus_geometry')
        self.zoom_in_font = QPropertyAnimation(self, b'font_size')
        self.zoom_in_iconsize = QPropertyAnimation(self, b'icon_size')
        self.zoom_in_geometry.setDuration(self._zoom_duration)
        self.zoom_in_font.setDuration(self._zoom_duration)
        self.zoom_in_iconsize.setDuration(self._zoom_duration)

        self.zoom_out_geometry = QPropertyAnimation(self, b'cus_geometry')
        self.zoom_out_font = QPropertyAnimation(self, b'font_size')
        self.zoom_out_iconsize = QPropertyAnimation(self, b'icon_size')
        self.zoom_out_geometry.setDuration(self._zoom_duration)
        self.zoom_out_font.setDuration(self._zoom_duration)
        self.zoom_out_iconsize.setDuration(self._zoom_duration)

        self._is_zoom_in_finished = True
        self.zoom_in_group = QParallelAnimationGroup()
        self.zoom_in_group.finished.connect(self.zoom_in_finish)
        self.zoom_in_group.addAnimation(self.zoom_in_geometry)
        self.zoom_in_group.addAnimation(self.zoom_in_font)
        self.zoom_in_group.addAnimation(self.zoom_in_iconsize)

        self._is_zoom_out_finished = True
        self.zoom_out_group = QParallelAnimationGroup()
        self.zoom_out_group.finished.connect(self.zoom_out_finish)
        self.zoom_out_group.addAnimation(self.zoom_out_geometry)
        self.zoom_out_group.addAnimation(self.zoom_out_font)
        self.zoom_out_group.addAnimation(self.zoom_out_iconsize)
        pass

    def enterEvent(self, event):
        self.mouse_enter.emit(self)
        if self._is_zoom_out_finished:
            self.update_compont_info()
        else:
            self.zoom_out_group.stop()
            self._is_zoom_out_finished = True
        self._is_use_size_hint = False

        # 形状放大。不关心动画的起始值是什么，只在乎动画的结束值必须是所有动画开始前的控件大小的zoom_factor倍
        start_rect = self.geometry()
        stop_rect = self.cal_zoom_in_rect()
        self.zoom_in_geometry.setStartValue(start_rect)
        self.zoom_in_geometry.setEndValue(stop_rect)

        # 字体放大。
        start_font_size = self.font().pointSizeF()
        stop_font_size = self._font_size_before_zoom * self._zoom_factor
        self.zoom_in_font.setStartValue(start_font_size)
        self.zoom_in_font.setEndValue(stop_font_size)

        start_icon = self.iconSize()
        stop_icon = QSize(int(self._icon_size_before_zoom.width() * self._zoom_factor),
                          int(self._icon_size_before_zoom.height() * self._zoom_factor))
        self.zoom_in_iconsize.setStartValue(start_icon)
        self.zoom_in_iconsize.setEndValue(stop_icon)
        self.zoom_in_group.start()
        self._is_zoom_in_finished = False
        pass

    def leaveEvent(self, event):
        self.mouse_leave.emit(self)
        if not self._is_zoom_in_finished:
            self.zoom_in_group.stop()
            self._is_zoom_in_finished = True
        self._is_use_size_hint = False

        # 形状缩小。巧了，这个只关注动画的最初值
        start_rect = self.geometry()
        stop_rect = self._geometry_before_zoom
        self.zoom_out_geometry.setStartValue(start_rect)
        self.zoom_out_geometry.setEndValue(stop_rect)

        # 字体缩小。
        start_font_size = self.font().pointSizeF()
        stop_font_size = self._font_size_before_zoom
        self.zoom_out_font.setStartValue(start_font_size)
        self.zoom_out_font.setEndValue(stop_font_size)

        start_icon = self.iconSize()
        stop_icon = self._icon_size_before_zoom
        self.zoom_out_iconsize.setStartValue(start_icon)
        self.zoom_out_iconsize.setEndValue(stop_icon)

        self.zoom_out_group.start()
        self._is_zoom_out_finished = False
        pass

    def sizeHint(self):
        if self._is_use_size_hint:
            return super().sizeHint()
        self.setStyleSheet(f"border: 1px solid black;border-radius:{self.width()//2}px;")
        return self.change_value.size()

    @property
    def zoom_duration(self):
        return self._zoom_duration

    @zoom_duration.setter
    def zoom_duration(self, value):
        self._zoom_duration = value
        self.zoom_in_geometry.setDuration(self._zoom_duration)
        self.zoom_out_geometry.setDuration(self._zoom_duration)

    @pyqtProperty(float)
    def font_size(self):
        return self.font().pointSizeF()

    @font_size.setter
    def font_size(self, value):
        font = self.font()
        font.setPointSizeF(value)
        self.setFont(font)

    @pyqtProperty(QRect)
    def cus_geometry(self):
        return self.geometry()

    @cus_geometry.setter
    def cus_geometry(self, value):
        self.change_value = value
        self.setGeometry(self.change_value)

    @pyqtProperty(QSize)
    def icon_size(self):
        return self.iconSize()

    @icon_size.setter
    def icon_size(self, size):
        self.setIconSize(size)

    def zoom_out_finish(self):
        self._is_zoom_out_finished = True

    def zoom_in_finish(self):
        self._is_zoom_in_finished = True

    def cal_zoom_in_rect(self):
        center_point = self._geometry_before_zoom.center()
        end_width = self._geometry_before_zoom.width() * self._zoom_factor
        end_height = self._geometry_before_zoom.height() * self._zoom_factor
        return QRect(
            int(center_point.x() - end_width // 2),  # 新左上角 x 坐标
            int(center_point.y() - end_height // 2),  # 新左上角 y 坐标
            int(end_width),  # 新宽度
            int(end_height)  # 新高度
        )

    def update_compont_info(self):
        # 更新当前控件的几何信息
        self._geometry_before_zoom = self.geometry()
        self._font_size_before_zoom = self.font().pointSizeF()
        self._icon_size_before_zoom = self.iconSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.resize(500, 500)
    hl_window = QHBoxLayout(window)
    hl_window.setSizeConstraint(QLayout.SetNoConstraint)
    btn_test = HoverLargeButton('测试')
    btn_test_2 = QPushButton('陪衬')
    # hl_window.addStretch(1)
    hl_window.addWidget(btn_test)
    hl_window.addWidget(btn_test_2)
    # hl_window.addStretch(1)
    window.show()
    sys.exit(app.exec_())
    pass
