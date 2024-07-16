import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from ui.independent_widget import PDFViewer, PromptCenterTop

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = PDFViewer(r"C:\Users\21276\Desktop\自由空间法使用文档.pdf")
    window = PromptCenterTop(QMessageBox.Critical, '警告', '位移台尚未连接成功！', [QMessageBox.Yes])
    window.show()
    sys.exit(app.exec_())
    pass