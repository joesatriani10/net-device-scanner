import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QHeaderView, QMessageBox
from PyQt6.QtGui import QCloseEvent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Net Device Scanner")
        self.resize(1280, 768)
        self.setMinimumSize(800, 600)

        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction("Scan")
        file_menu.addAction("Export Table")
        file_menu.addAction("Exit").triggered.connect(self.close)
        about_menu = menu.addMenu("About")
        about_menu.addAction("About")

        # Table
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(
            ["IP", "Host Name", "MAC Address", "State", "OS", "Open Ports", "Ping (ms)", "TTL", "Vendor", "Notes"])

        for i in range(self.table.columnCount() - 1):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.table.horizontalHeader().setStretchLastSection(True)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.status_bar)

        # central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    @staticmethod
    def scan_network():
        print("Scanning network")

    @staticmethod
    def export_table():
        print("Exporting table")

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to exit?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            QApplication.quit()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
