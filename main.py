import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QHeaderView, QMessageBox, \
    QProgressBar
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtCore import QThread, pyqtSignal


# Thread for network scanning (to prevent UI freezing)
class ScanThread(QThread):
    progress_update = pyqtSignal(int)  # Signal to emit scan progress updates

    def run(self):
        # Placeholder for actual network scanning logic
        for i in range(101):
            self.progress_update.emit(i)  # Emit progress (0 to 100)
            self.msleep(100)  # Simulate scan time (adjust later)


# Main window class for the IP scanner application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Net Device Scanner")  # Set window title
        self.resize(1280, 768)  # Set initial window size
        self.setMinimumSize(800, 600)  # Set minimum window size

        # Menu bar setup
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction("Scan")  # Placeholder for scan action
        file_menu.addAction("Export Table")  # Placeholder for export action
        file_menu.addAction("Exit").triggered.connect(self.close)  # Exit action
        about_menu = menu.addMenu("About")
        about_menu.addAction("About")  # Placeholder for about action

        # Table widget setup
        self.table = QTableWidget()
        self.table.setRowCount(0)  # Initially empty table
        self.table.setColumnCount(10)  # 10 columns for scan results
        column_headers = ["IP", "Host Name", "MAC Address", "State", "OS",
                          "Open Ports", "Ping (ms)", "TTL", "Vendor", "Notes"]
        self.table.setHorizontalHeaderLabels(column_headers)  # Set column names

        # Configure table column resizing
        for i in range(self.table.columnCount() - 1):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.table.horizontalHeader().setStretchLastSection(True)

        # Status Bar setup
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Progress Bar setup
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Main layout and central widget setup
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.status_bar)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    # Slot to start network scan
    def scan_network(self):
        self.progress_bar.setValue(0)  # Reset progress bar

        self.scan_thread = ScanThread()
        self.scan_thread.progress_updated.connect(self.progress_bar.setValue)  # Connect progress signal
        self.scan_thread.finished.connect(self.scan_finished)
        self.scan_thread.start()

    # Slot to update status bar when scan is finished
    def scan_finished(self):
        self.status_bar.showMessage("Scan completed")

    # Static method (placeholder) for exporting table data
    @staticmethod
    def export_table():
        print("Exporting table")

    # Event handler for closing the window
    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to exit?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            QApplication.quit()
        else:
            event.ignore()


# Main entry point for the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
