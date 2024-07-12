import sys

from PyQt5.QtWidgets import QApplication

from ui.independent_widget import PDFViewer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFViewer(r"C:\Users\21276\Desktop\自由空间法使用文档.pdf")
    window.show()
    sys.exit(app.exec_())
    pass