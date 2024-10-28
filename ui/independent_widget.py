import sys

from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import pyqtSignal, QSize, Qt, QPropertyAnimation, QVariantAnimation, QEasingCurve, QTime, QTimer
from PyQt5.QtGui import QIcon, QMovie, QFont
from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QDesktopWidget, QLabel, QHBoxLayout, QPushButton, \
    QApplication, QFrame, QWidget, QGraphicsOpacityEffect

from typing import Iterable


class HSeparateLine(QWidget):
    def __init__(self, *args, separate_info: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.separate_info = separate_info
        self.setup_ui()
        pass

    def setup_ui(self):
        self.hl_central = QHBoxLayout(self)

        self.lb_separate_info = QLabel(self.separate_info)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setLineWidth(20)
        self.line.setMidLineWidth(10)

        self.hl_central.addWidget(self.lb_separate_info)
        self.hl_central.addWidget(self.line, 1)


class VSeparateLine(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        pass

    def setup_ui(self):
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(20)
        self.setMidLineWidth(10)


class PromptCenterTop(QDialog):
    '''
    消息弹窗, 在QMessageBox上封装一层, 自带一些样式。需调用exec()显示
    '''

    closed_signal = pyqtSignal(str)

    def __init__(self, icon, title: str, text: str, buttons: Iterable[QMessageBox.StandardButton]=[QMessageBox.Ok], default_btn=None):
        """
        :param icon: QMessageBox.Icon
        :param title:
        :param text:
        :param buttons:
        """
        super().__init__()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.mb = QMessageBox(self)
        self.mb.setStyleSheet("""
                    PromptCenterTop {
                        background-color: white;
                    }
                    QLabel {
                        background-color:white;
                    }
                    QPushButton{
                        color:black;
                        border: 1px solid #8f8f91;
                        border-radius: 10px;
                        background-color: white;
                        min-width: 80px;
                        min-height: 30px;
                        font-size: 20px;
                    }
                    QPushButton:hover{
                        background-color:#F5F5F5;
                    }
                """)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('./static/imgs/splash.png'))
        self.step_ui(icon, title, text, buttons, default_btn=None)
        pass

    def step_ui(self, icon, title, text, buttons, default_btn=None):
        self.mb.setWindowTitle(title)
        self.mb.setWindowIcon(QIcon('./static/imgs/splash.png'))
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('./static/imgs/splash.png'))
        self.mb.setIcon(icon)
        self.mb.setText(text)

        for button in buttons:
            self.mb.addButton(button)
        pass

    def exec(self):
        self.show()
        res = self.mb.exec()
        return res


class PDFViewer(QAxWidget):
    '''
    pdf查看容器。
    构造时给出pdf路径
    '''

    def __init__(self, pdf_path:str):
        super().__init__()
        self.openPdf(pdf_path)
        pass

    def openPdf(self, path):
        self.clear()
        if not self.setControl('Adobe PDF Reader'):
            return QMessageBox.critical(self, '错误', '没有安装 adobe pdf reader')
        self.dynamicCall('LoadFile(const QString&)', path)


class RotationProgressDialog(QDialog):
    """狗头加载弹窗"""

    btn_clicked = pyqtSignal()  # 设置按钮时，按钮的点击事件

    def __init__(self, dia_size: QSize = QSize(150, 150), label: QLabel = None, btn: QPushButton = None, parent=None):
        super().__init__(parent)
        self.__is_allow_close = False
        self.__exec_close_count = 0  # 大于0，被展示次数。 小于0，被关闭次数
        self.pb_operation = btn
        self.lb_label = label
        self.setup_ui(dia_size)
        pass

    def setup_ui(self, dia_size):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.hl_movie_center = QHBoxLayout()
        self.movie = QMovie("./static/imgs/wait_logo.gif")
        self.movie.setScaledSize(dia_size)
        if not self.movie.isValid():
            print("Failed to load animation.")
            return
        self.lb_movie_container = QLabel()  # 使用QLabel来显示动画
        self.lb_movie_container.setMovie(self.movie)
        self.hl_movie_center.addStretch(1)
        self.hl_movie_center.addWidget(self.lb_movie_container)
        self.hl_movie_center.addStretch(1)
        self.layout.addLayout(self.hl_movie_center)
        if self.lb_label is None:
            pass
        else:
            self.hl_label_center = QHBoxLayout()
            self.lb_label.setStyleSheet("""
                QLabel{
                    font-size: 20px;
                    color:#df9622;
                }
            """)
            self.hl_label_center.addStretch(1)
            self.hl_label_center.addWidget(self.lb_label)
            self.hl_label_center.addStretch(1)
            self.layout.addLayout(self.hl_label_center)

        if self.pb_operation is None:
            pass
        else:
            self.hl_btn_center = QHBoxLayout()
            self.pb_operation.clicked.connect(self.clicked_operate)
            self.pb_operation.setStyleSheet("""
            QPushButton{
                color:white;
                border: 1px solid #8f8f91;
                border-radius: 10px;
                background-color: #f9b03c;
                width: 100px;
                height: 40px;
                font-size: 20px;
            }
            QPushButton:hover {
                color: #ffffff;
                background-color:#df9622;
            }
            """)
            self.hl_btn_center.addStretch(1)
            self.hl_btn_center.addWidget(self.pb_operation)
            self.hl_btn_center.addStretch(1)
            self.layout.addLayout(self.hl_btn_center)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        pass

    def closeEvent(self, event):
        if self.is_allow_close:
            event.accept()
        else:
            event.ignore()
        pass

    @property
    def is_allow_close(self):
        return self.__is_allow_close

    @is_allow_close.setter
    def is_allow_close(self, value):
        value = bool(value)
        self.__is_allow_close = value
        pass

    def clicked_operate(self):
        self.btn_clicked.emit()
        pass

    def exec_loading(self):
        self.__exec_close_count += 1
        if not self.__exec_close_count > 0:
            return
        self.is_allow_close = False
        self.movie.start()
        self.exec()
        pass

    def close_loading(self):
        self.__exec_close_count -= 1
        if not self.__exec_close_count == 0:
            return
        self.is_allow_close = True
        self.movie.deleteLater()
        self.close()
        pass


class FadeOutPrompt(QDialog):
    """FadeOutPrompt.show()"""
    def __init__(self, text:str, *args, duration_time=1000, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.duration_time = duration_time
        self.init_params()
        self.setup_ui()
        self.animation_init()
        pass

    def get_text(self):
        return self.text

    def set_text(self, text:str):
        self.text = text
        self.lb_content.setText(text)
        print(self.lb_content.text())

    def init_params(self):
        # 依靠最外部父控件来定位中心位置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 获取屏幕尺寸，动态设置字体大小
        screen_size = QApplication.primaryScreen().size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()
        self.label_font = QFont()
        self.label_font.setPointSize(round(screen_height/100 if screen_height < screen_width else screen_width/100))
        self.qss = """
                    QDialog{
                        background-color: #2c2c2c;
                        border-radius: 10%;
                        padding-top: 20px;
                        padding-bottom: 20px;
                        padding-left: 30px;
                        padding-right: 30px;
                    }
                    QLabel{
                        color:white;
                    }
                    """
        self.setStyleSheet(self.qss)
        pass

    def setup_ui(self):

        self.goe_opacity = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.goe_opacity)
        self.vl_container_center = QVBoxLayout(self)
        self.hl_container_center = QHBoxLayout()
        self.lb_content = QLabel(self.text)
        self.lb_content.setFont(self.label_font)

        # 使文本控件水平&垂直居中
        self.hl_container_center.addStretch(1)
        self.hl_container_center.addWidget(self.lb_content)
        self.hl_container_center.addStretch(1)
        self.vl_container_center.addStretch(1)
        self.vl_container_center.addLayout(self.hl_container_center)
        self.vl_container_center.addStretch(1)
        pass

    # def animation_init(self):
    #     self.fade_out = QPropertyAnimation(self.goe_opacity, b"opacity")
    #     self.fade_out.setDuration(2000)
    #     self.fade_out.setStartValue(1.0)
    #     self.fade_out.setEndValue(0.0)
    #     self.fade_out.start()
    #     self.fade_out.finished.connect(lambda :print(11111111111111))
    #     pass

    def animation_init(self):
        # 定义动画曲线
        self.ec_opacity = QEasingCurve(QEasingCurve.InExpo)
        # 定义动画
        self.fade_out = QVariantAnimation()
        self.fade_out.setDuration(self.duration_time)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.valueChanged.connect(self.running_animation)
        self.fade_out.finished.connect(self.close)
        self.fade_out.setEasingCurve(self.ec_opacity)
        self.fade_out.start()
        pass

    def running_animation(self, value):
        self.goe_opacity.setOpacity(value)
        if value == 0:
            self.fade_out.stop()
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = PromptCenterTop(QMessageBox.Warning, "提示", "tttttt")
    w = FadeOutPrompt("登录成功")
    w.show()
    sys.exit(app.exec_())
    pass
