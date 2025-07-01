

import sys
import subprocess
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QFont, QTextCursor, QPixmap, QMovie
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect

class WebFangGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WEBFANG")
        self.setGeometry(200, 200, 1000, 750)

        # Full background logo
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("Talyxlogo.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.bg_label.setGeometry(200, 300, self.width(), self.height())
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: rgba(0, 0, 0, 25);")
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()

        # Neon glowing text logo (top center)
        logo_label = QLabel("WEBFANG")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Bat face background (slightly transparent, below logo)
        bat_label = QLabel(self.central_widget)
        bat_pixmap = QPixmap("2749.png")
        bat_pixmap = bat_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        bat_label.setPixmap(bat_pixmap)
        bat_label.setAlignment(Qt.AlignCenter)
        bat_label.setStyleSheet("opacity: 0.2;")
        bat_label.setAttribute(Qt.WA_TranslucentBackground)
        main_layout.insertWidget(1, bat_label)

        # Matrix rain animations on left and right sides
        left_matrix = QLabel(self.central_widget)
        left_matrix_movie = QMovie("matx.gif")
        left_matrix.setMovie(left_matrix_movie)
        left_matrix_movie.start()
        left_matrix.setGeometry(0, 0, 100, 750)
        left_matrix.setAttribute(Qt.WA_TranslucentBackground)
        left_matrix.setStyleSheet("background: transparent;")
        left_matrix.setParent(self.central_widget)
        left_matrix.raise_()

        right_matrix = QLabel(self.central_widget)
        right_matrix_movie = QMovie("matri.gif")
        right_matrix.setMovie(right_matrix_movie)
        right_matrix_movie.start()
        right_matrix.setGeometry(900, 0, 100, 750)
        right_matrix.setAttribute(Qt.WA_TranslucentBackground)
        right_matrix.setStyleSheet("background: transparent;")
        right_matrix.setParent(self.central_widget)
        right_matrix.raise_()

        # Preset buttons for common actions
        preset_layout = QHBoxLayout()
        commands = {
            "Scan URL": "-u https://example.com",
            "Subdomains": "--subdomains https://example.com",
            "DNS Bruteforce": "--dns-bruteforce https://example.com",
            "Run All": "-a https://example.com"
        }
        for name, cmd in commands.items():
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, c=cmd: self.input_field.setText(c))
            preset_layout.addWidget(btn)
        main_layout.addLayout(preset_layout)

        # Input + Run + Save buttons
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter WebFang arguments, e.g. -u https://target")
        input_layout.addWidget(self.input_field)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.play_scan_sound)
        self.run_button.clicked.connect(self.run_webfang)
        input_layout.addWidget(self.run_button)

        self.save_button = QPushButton("Save Output")
        self.save_button.clicked.connect(self.save_output)
        input_layout.addWidget(self.save_button)

        main_layout.addLayout(input_layout)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        main_layout.addWidget(self.output_area)

        # Footer with GitHub link (smaller)
        footer = QLabel()
        footer.setText(
            'Made by Talyx  |  <span style="font-size:9pt;">'
            '<a href="https://github.com/Talyx66" style="color:#00cfff; text-decoration:none;">github.com/Talyx66</a>'
            '</span>'
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setOpenExternalLinks(True)
        footer.setStyleSheet("color: #aaaaaa; font-size: 10pt; padding: 6px;")
        main_layout.addWidget(footer)

        self.central_widget.setLayout(main_layout)

        # Ambient background loop audio
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("matx.mp3")))
        self.player.setVolume(10)
        self.player.play()
        self.player.mediaStatusChanged.connect(self.handle_media_status)

        # Fang bite sound effect
        self.fang_sound = QSoundEffect()
        self.fang_sound.setSource(QUrl.fromLocalFile("fang.wav"))
        self.fang_sound.setVolume(0.6)

    def resizeEvent(self, event):
        self.bg_label.setPixmap(QPixmap("Talyxlogo.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def run_webfang(self):
        args = self.input_field.text().strip()
        if not args:
            self.output_area.append("[!] Please enter command arguments.\n")
            return

        self.output_area.append(f"\n>>> Running: python3 webfang.py {args}\n")
        self.run_button.setText("Scanning...")
        self.run_button.setEnabled(False)

        QApplication.processEvents()
        try:
            result = subprocess.getoutput(f"python3 webfang.py {args}")
        except Exception as e:
            result = f"[ERROR] {str(e)}"

        self.animate_output(result)

        self.run_button.setText("Run")
        self.run_button.setEnabled(True)

    def animate_output(self, text):
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
            color = "#fce94f"
        else:
            color = "#eeeeee"
        self.output_area.setTextColor(Qt.white)
        self.output_area.setTextBackgroundColor(Qt.transparent)
        self.output_area.append(f"<span style='color:{color}'>{line}</span>")

    def save_output(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Output", "webfang_output.txt", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.output_area.toPlainText())
                QMessageBox.information(self, "Saved", f"Output saved to {filename}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save: {e}")

    def play_scan_sound(self):
        self.fang_sound.play()

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #0a0f1c, stop:1 #001d2e
            );
        }
        QWidget {
            background-color: transparent;
            color: #eeeeee;
            font-family: Consolas, monospace;
            font-size: 12pt;
        }
        QLabel#logoLabel {
            color: #00cfff;
            font-size: 54pt;
            font-weight: bold;
            font-family: 'Orbitron', 'Segoe UI', Tahoma, sans-serif;
        }
        QPushButton {
            background-color: #112233;
            border: 1px solid #00cfff;
            padding: 12px;
            border-radius: 8px;
            color: #00cfff;
        }
        QPushButton:hover {
            background-color: #223344;
        }
        QLineEdit, QTextEdit {
            background-color: #111a28;
            border: 1px solid #00cfff;
            border-radius: 6px;
            padding: 8px;
            color: #eeeeee;
            font-size: 11pt;
        }
    """)
    window = WebFangGUI()
    window.show()
    sys.exit(app.exec_())
