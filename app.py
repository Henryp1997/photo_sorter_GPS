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

class RegionWidget(QWidget):
    def __init__(self, lat_long):
        super().__init__()
        layout = QGridLayout()
        layout.addWidget(QLabel("Coordinate:"), 0, 0)
        layout.addWidget(QLineEdit(self), 0, 1)
        layout.addWidget(QLabel("Direction:"), 0, 2)
        dropdown = QComboBox()
        if lat_long == "lat":
            dropdown.addItems(["N", "S"])
        else:
            dropdown.addItems(["W", "E"])
        layout.addWidget(dropdown, 0, 3)
        self.setLayout(layout)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo sorter")
        self.setFixedHeight(450)

        layout = QGridLayout()

        browse_btn = QPushButton(self)
        browse_btn.setText("Browse...")
        browse_btn.clicked.connect(self.open_dialog)
        browse_widget = QWidget()
        browse_widget.setFixedWidth(200)
        browse_layout = QVBoxLayout()
        browse_layout.addWidget(QLabel("Select image directory:"))
        browse_layout.addWidget(browse_btn)

        browse_widget.setLayout(browse_layout)
        layout.addWidget(browse_widget, 0, 0)

        coords = (
            QLabel("Region name:"),
            QLineEdit(),
            QLabel("Bottom latitude:"),
            RegionWidget("lat"),
            QLabel("Top latitude:"),
            RegionWidget("lat"),
            QLabel("Left longitude:"),
            RegionWidget("long"),
            QLabel("Right longitude:"),
            RegionWidget("long"),
        )
        
        # add new region column
        region_widget = QWidget()
        region_widget.setFixedWidth(400)

        # vertical column layout
        region_layout = QVBoxLayout()

        region_label = QLabel("Create new region. Find the bounding box for your new region using Google Maps coordinates.")
        region_label.setWordWrap(True)

        region_layout.addWidget(region_label)
        for i, item in enumerate(coords):
            region_layout.addWidget(item)
        
        region_widget.setLayout(region_layout)
        layout.addWidget(region_widget, 0, 1)

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