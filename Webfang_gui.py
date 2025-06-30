
import sys
import subprocess
import time
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox,
    QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QFont, QTextCursor, QPixmap, QMovie
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect


class WebFangGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WEBFANG")
        self.setGeometry(200, 200, 1000, 750)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()

        # Neon glowing text logo
        logo_label = QLabel("WEBFANG")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Bat face background (slightly transparent)
        bat_label = QLabel()
        bat_img_path = "2749.png"
        if not os.path.isfile(bat_img_path):
            print(f"[WARN] Bat image not found: {bat_img_path}")
        bat_pixmap = QPixmap(bat_img_path)
        bat_pixmap = bat_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        bat_label.setPixmap(bat_pixmap)
        bat_label.setAlignment(Qt.AlignCenter)

        # Set opacity properly
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.15)
        bat_label.setGraphicsEffect(opacity_effect)

        main_layout.insertWidget(1, bat_label)  # Insert below logo_label

        # Matrix rain animations on sides
        matrix_left = QLabel()
        matrix_left_path = "matri.gif"
        if not os.path.isfile(matrix_left_path):
            print(f"[WARN] Matrix GIF not found: {matrix_left_path}")
        matrix_left_movie = QMovie(matrix_left_path)
        matrix_left.setMovie(matrix_left_movie)
        matrix_left_movie.start()
        matrix_left.setFixedWidth(100)
        matrix_left.setAttribute(Qt.WA_TranslucentBackground)
        matrix_left.setStyleSheet("background: transparent;")
        # Will add it to layout wrapper later

        matrix_right = QLabel()
        matrix_right_path = "matri.gif"
        matrix_right_movie = QMovie(matrix_right_path)
        matrix_right.setMovie(matrix_right_movie)
        matrix_right_movie.start()
        matrix_right.setFixedWidth(100)
        matrix_right.setAttribute(Qt.WA_TranslucentBackground)
        matrix_right.setStyleSheet("background: transparent;")

        # Create a horizontal layout for side matrix + central content
        central_layout = QHBoxLayout()
        central_layout.addWidget(matrix_left)

        # Middle widget will hold main_layout widgets (bat, logo, buttons, etc)
        middle_widget = QWidget()
        middle_widget.setLayout(main_layout)
        central_layout.addWidget(middle_widget, stretch=1)

        central_layout.addWidget(matrix_right)

        # Now set central widget's layout to this horizontal layout
        self.central_widget.setLayout(central_layout)

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

        # Ambient background loop audio
        bg_audio_path = "matx.mp3"
        if not os.path.isfile(bg_audio_path):
            print(f"[WARN] Background audio not found: {bg_audio_path}")
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(bg_audio_path)))
        self.player.setVolume(10)
        self.player.play()
        self.player.mediaStatusChanged.connect(self.handle_media_status)

        # Fang bite sound effect
        fang_audio_path = "fang.wav"
        if not os.path.isfile(fang_audio_path):
            print(f"[WARN] Fang audio not found: {fang_audio_path}")
        self.fang_sound = QSoundEffect()
        self.fang_sound.setSource(QUrl.fromLocalFile(fang_audio_path))
        self.fang_sound.setVolume(0.6)

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
