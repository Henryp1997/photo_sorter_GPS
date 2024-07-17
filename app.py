from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo sorter")
        self.setFixedHeight(350)
        self.setFixedWidth(500)

        layout = QGridLayout()

        browse_btn = QPushButton(self)
        browse_btn.setText("Browse...")
        browse_btn.clicked.connect(self.open_dialog)
        browse_layout = QVBoxLayout()
        browse_layout.addWidget(QLabel("Select image directory:"))
        browse_layout.addWidget(browse_btn)
        layout.addLayout(browse_layout, 0, 0)

        coords = (
            QLabel("Bottom latitude:"),
            QLineEdit(self),
            QLabel("Top latitude:"),
            QLineEdit(self),
            QLabel("Left longitude:"),
            QLineEdit(self),
            QLabel("Right longitude:"),
            QLineEdit(self),
        )
        
        region_layout = QVBoxLayout()
        region_layout.addWidget(QLabel("Create new region. Find the bounding box for your new region using Google Maps coordinates."))
        region_layout.addWidget(Color("white"))
        for item in coords:
            region_layout.addWidget(item)
        
        layout.addLayout(region_layout, 0, 1)

        # finally set widget layout to variable layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open File",
            directory="",
            filter="All Files (*);; PNG Files (*.png)",
        )        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_gui = Main()
    main_gui.show()
    sys.exit(app.exec())