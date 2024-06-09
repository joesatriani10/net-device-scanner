import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QHeaderView, QMessageBox, \
    QProgressBar, QFileDialog, QTableWidgetItem, QLabel, QLineEdit, QHBoxLayout, QPushButton
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
import csv

# Dummy data for testing 10 rows of data
scan_results = [
    {"IP": "192.168.1.1", "Host Name": "Router", "MAC Address": "00:1A:2B:3C:4D:5E", "State": "Up", "OS": "Linux",
     "Open Ports": "22, 80", "Ping (ms)": "1", "TTL": "64", "Vendor": "TP-Link", "Notes": "Default gateway"},
    {"IP": "192.168.1.10", "Host Name": "PC-John", "MAC Address": "A1:B2:C3:D4:E5:F6", "State": "Up", "OS": "Windows",
     "Open Ports": "135, 445", "Ping (ms)": "3", "TTL": "128", "Vendor": "Dell", "Notes": ""},
    {"IP": "192.168.1.15", "Host Name": "PC-Mary", "MAC Address": "22:44:66:88:AA:CC", "State": "Up", "OS": "Android",
     "Open Ports": "554", "Ping (ms)": "5", "TTL": "64", "Vendor": "Samsung", "Notes": ""},
    {"IP": "192.168.1.20", "Host Name": "Printer", "MAC Address": "11:33:55:77:99:BB", "State": "Up", "OS": "Unknown",
     "Open Ports": "9100", "Ping (ms)": "2", "TTL": "64", "Vendor": "HP", "Notes": ""},
    {"IP": "192.168.1.25", "Host Name": "SmartTV", "MAC Address": "FF:EE:DD:CC:BB:AA", "State": "Up", "OS": "Linux",
     "Open Ports": "80, 5357", "Ping (ms)": "8", "TTL": "64", "Vendor": "LG", "Notes": ""},
    {"IP": "192.168.1.30", "Host Name": "", "MAC Address": "0A:23:45:67:89:AB", "State": "Down", "OS": "",
     "Open Ports": "", "Ping (ms)": "", "TTL": "", "Vendor": "", "Notes": ""},
    {"IP": "192.168.1.35", "Host Name": "Lap-Alice", "MAC Address": "AA:BB:CC:DD:EE:FF", "State": "Up", "OS": "macOS",
     "Open Ports": "548, 631", "Ping (ms)": "4", "TTL": "64", "Vendor": "Apple", "Notes": ""},
    {"IP": "192.168.1.40", "Host Name": "RaspberryPi", "MAC Address": "C0:DE:F1:23:45:67", "State": "Up", "OS": "Linux",
     "Open Ports": "22, 8080", "Ping (ms)": "10", "TTL": "64", "Vendor": "Raspberry Pi Foundation", "Notes": ""},
    {"IP": "192.168.1.45", "Host Name": "", "MAC Address": "12:34:56:78:9A:BC", "State": "Down", "OS": "",
     "Open Ports": "", "Ping (ms)": "", "TTL": "", "Vendor": "", "Notes": ""},
    {"IP": "192.168.1.50", "Host Name": "IPCamera", "MAC Address": "98:76:54:32:10:FE", "State": "Up", "OS": "Unknown",
     "Open Ports": "80, 554", "Ping (ms)": "7", "TTL": "64", "Vendor": "D-Link", "Notes": "Security camera"}
]


# Thread for network scanning (to prevent UI freezing)
class ScanThread(QThread):
    progress_update = pyqtSignal(int)  # Signal to emit scan progress updates

    def run(self):
        # Placeholder for actual network scanning logic
        for i in range(101):
            self.progress_update.emit(i)  # Emit progress (0 to 100)
            self.msleep(100)  # Simulate scan time (adjust later)

        # Emit the scan results to the main thread
        self.progress_update.emit(100)  # Signal scan completion
        self.finished.emit()


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
        file_menu.addAction("Export Table").triggered.connect(self.export_table)  # Placeholder for export action
        file_menu.addAction("Exit").triggered.connect(self.close)  # Exit action
        about_menu = menu.addMenu("About")
        about_menu.addAction("About")  # Placeholder for about action

        # IP range input fields
        ip_start_range_label = QLabel("IP Range:")
        self.ip_start_range_input = QLineEdit()

        ip_end_range_label = QLabel("to")
        self.ip_end_range_input = QLineEdit()

        # Button to start network scan
        self.scan_button = QPushButton("Scan")
        self.scan_button.clicked.connect(self.scan_network)

        # Create a horizontal layout and add the labels and input fields
        ip_range_layout = QHBoxLayout()
        ip_range_layout.addWidget(ip_start_range_label)
        ip_range_layout.addWidget(self.ip_start_range_input)
        ip_range_layout.addWidget(ip_end_range_label)
        ip_range_layout.addWidget(self.ip_end_range_input)
        ip_range_layout.addWidget(self.scan_button)

        # Table widget setup
        self.table = QTableWidget()
        self.table.setRowCount(0)  # Initially empty table
        self.table.setColumnCount(10)  # 10 columns for scan results
        column_headers = ["IP", "Host Name", "MAC Address", "State", "OS",
                          "Open Ports", "Ping (ms)", "TTL", "Vendor", "Notes"]
        self.table.setHorizontalHeaderLabels(column_headers)  # Set column names
        # Add dummy data to table
        for i, row_data in enumerate(scan_results):
            self.table.insertRow(i)
            for j, (key, value) in enumerate(row_data.items()):
                item = QTableWidgetItem(value)
                self.table.setItem(i, j, item)

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
        layout.addLayout(ip_range_layout)  # Add IP range layout to main layout
        layout.addWidget(self.table)  # Add table widget to layout
        layout.addWidget(self.status_bar)  # Add status bar to layout

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    # Slot to start network scan
    def scan_network(self):
        self.progress_bar.setValue(0)  # Reset progress bar

        self.scan_thread = ScanThread()
        self.scan_thread.progress_update.connect(self.progress_bar.setValue)  # Connect progress signal
        self.scan_thread.finished.connect(self.scan_finished)
        self.scan_thread.finished.connect(self.update_table)  # Update table in main thread
        self.scan_thread.start()
        self.scan_button.setEnabled(False)  # Disable scan button during scan

    @pyqtSlot()
    def update_table(self):
        # ... (Retrieve scan results from ScanThread)
        self.table.setRowCount(len(scan_results))  # Update table row count
        for row, data in enumerate(scan_results):
            for col, key in enumerate(data.keys()):
                item = QTableWidgetItem(str(data[key]))
                self.table.setItem(row, col, item)

    # Slot to update status bar when scan is finished
    def scan_finished(self):
        self.status_bar.showMessage("Scan completed")

    # Slot to export table data to CSV file
    def export_table(self):
        try:
            file_name, _ = QFileDialog.getSaveFileName(self, "Export Table", "", "CSV Files (*.csv)")  # Removed options
            if file_name:
                with open(file_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write headers
                    headers = []
                    for column in range(self.table.columnCount()):
                        header_item = self.table.horizontalHeaderItem(column)
                        headers.append(header_item.text() if header_item else "")
                    writer.writerow(headers)

                    # Write data
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for column in range(self.table.columnCount()):
                            item = self.table.item(row, column)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
            self.status_bar.showMessage("Table exported to {}".format(file_name))  # Formatted message
        except Exception as e:
            self.status_bar.showMessage(f"Error exporting table: {str(e)}")

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
