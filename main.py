#first brush-through

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QLabel, QWidget, QComboBox, QProgressBar
)
import subprocess


class BootableUSBApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bootable USB Creator")
        self.setGeometry(100, 100, 400, 300)

        # Main layout
        layout = QVBoxLayout()

        # ISO File selection
        self.iso_label = QLabel("Select ISO File:")
        layout.addWidget(self.iso_label)

        self.file_button = QPushButton("Choose ISO")
        self.file_button.clicked.connect(self.select_iso_file)
        layout.addWidget(self.file_button)

        # USB Drive selection
        self.drive_label = QLabel("Select USB Drive:")
        layout.addWidget(self.drive_label)

        self.drive_combo = QComboBox()
        self.refresh_drives()
        layout.addWidget(self.drive_combo)

        # Progress bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Write Button
        self.write_button = QPushButton("Create Bootable USB")
        self.write_button.clicked.connect(self.create_bootable_usb)
        layout.addWidget(self.write_button)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_iso_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select ISO File", "", "ISO Files (*.iso)")
        if file_path:
            self.iso_label.setText(f"ISO File: {file_path}")
            self.iso_file = file_path

    def refresh_drives(self):
        # This is an example; replace it with actual disk detection logic.
        drives = ["Disk 1 - /dev/sda", "Disk 2 - /dev/sdb"]
        self.drive_combo.addItems(drives)

    def create_bootable_usb(self):
        iso_file = getattr(self, 'iso_file', None)
        selected_drive = self.drive_combo.currentText()

        if not iso_file or not selected_drive:
            self.iso_label.setText("Error: ISO file or drive not selected!")
            return

        # Example: Write ISO using dd (Linux/macOS example)
        try:
            self.progress.setValue(0)
            subprocess.run(
                ["dd", f"if={iso_file}", f"of={selected_drive.split(' ')[-1]}", "bs=4M", "status=progress"],
                check=True
            )
            self.progress.setValue(100)
            self.iso_label.setText("Bootable USB Created Successfully!")
        except subprocess.CalledProcessError as e:
            self.iso_label.setText(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BootableUSBApp()
    window.show()
    sys.exit(app.exec_())

