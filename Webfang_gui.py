import sys
import os
import subprocess
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QTextCursor

class WebFangGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WEBFANG")
        self.setGeometry(200, 200, 1000, 750)

        # === Frame-by-frame background ===
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        self.frame_index = 0
        self.frame_paths = sorted([
            os.path.join("frames", f)
            for f in os.listdir("frames")
            if f.endswith(".png")
        ])

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # ~10 FPS

        # === Main GUI ===
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background-color: rgba(0, 0, 0, 130);")
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Header
        logo = QLabel("WEBFANG")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: #00cfff; font-size: 48pt; font-weight: bold;")
        layout.addWidget(logo)

        # Preset buttons
        button_row = QHBoxLayout()
        commands = {
            "Scan URL": "-u https://example.com",
            "Subdomains": "--subdomains https://example.com",
            "DNS Bruteforce": "--dns-bruteforce https://example.com",
            "Run All": "-a https://example.com"
        }
        for label, cmd in commands.items():
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, c=cmd: self.input_field.setText(c))
            button_row.addWidget(btn)
        layout.addLayout(button_row)

        # CLI input
        cli_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter WebFang arguments...")
        cli_row.addWidget(self.input_field)

        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run_webfang)
        cli_row.addWidget(self.run_btn)

        self.save_btn = QPushButton("Save Output")
        self.save_btn.clicked.connect(self.save_output)
        cli_row.addWidget(self.save_btn)
        layout.addLayout(cli_row)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        # Footer
        footer = QLabel('<a href="https://github.com/Talyx66">github.com/Talyx66</a>')
        footer.setAlignment(Qt.AlignCenter)
        footer.setOpenExternalLinks(True)
        footer.setStyleSheet("color: #cccccc; font-size: 9pt;")
        layout.addWidget(footer)

        self.central_widget.setLayout(layout)

    def update_frame(self):
        if not self.frame_paths:
            return
        current_frame = QPixmap(self.frame_paths[self.frame_index])
        self.bg_label.setPixmap(current_frame)
        self.frame_index = (self.frame_index + 1) % len(self.frame_paths)

    def resizeEvent(self, event):
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        return super().resizeEvent(event)

    def run_webfang(self):
        args = self.input_field.text().strip()
        if not args:
            self.output_area.append("[!] No input.\n")
            return

        self.output_area.append(f"\n>>> python3 webfang.py {args}\n")
        self.run_btn.setText("Running...")
        self.run_btn.setEnabled(False)
        QApplication.processEvents()

        try:
            result = subprocess.getoutput(f"python3 webfang.py {args}")
        except Exception as e:
            result = f"[ERROR] {str(e)}"

        self.display_output(result)

        self.run_btn.setText("Run")
        self.run_btn.setEnabled(True)

    def display_output(self, text):
        self.output_area.moveCursor(QTextCursor.End)
        for line in text.splitlines():
            self.append_colored_line(line)
            QApplication.processEvents()
            time.sleep(0.01)

    def append_colored_line(self, line):
        if line.startswith("[+]"):
            color = "#00ff88"
        elif line.startswith("[-]"):
            color = "#ff5555"
        elif line.startswith("[!]"):
            color = "#ffff55"
        else:
            color = "#eeeeee"
        self.output_area.append(f"<span style='color:{color}'>{line}</span>")

    def save_output(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Output", "webfang_output.txt", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(self.output_area.toPlainText())
                QMessageBox.information(self, "Saved", f"Output saved to {filename}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebFangGUI()
    window.show()
    sys.exit(app.exec_())
