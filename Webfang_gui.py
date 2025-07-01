import sys
import subprocess
import time
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QTextCursor, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect
from PyQt5.QtMultimediaWidgets import QVideoWidget

class WebFangGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WEBFANG")
        self.setGeometry(200, 200, 1000, 750)

        # ==== VIDEO BACKGROUND ====
        self.video_widget = QVideoWidget(self)
        self.video_widget.setGeometry(0, 0, self.width(), self.height())
        self.video_widget.lower()

        self.video_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_path = os.path.abspath("Talyxlogo6.mp4")
        self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.video_player.setVideoOutput(self.video_widget)
        self.video_player.play()
        self.video_player.mediaStatusChanged.connect(self.loop_video)

        # ==== MAIN WIDGET ====
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background-color: rgba(0, 0, 0, 80);")
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()

        # Logo Text
        logo_label = QLabel("WEBFANG")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setObjectName("logoLabel")
        main_layout.addWidget(logo_label)

        # Bat image
        bat_label = QLabel()
        bat_pixmap = QPixmap("2749.png")
        bat_label.setPixmap(bat_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        bat_label.setAlignment(Qt.AlignCenter)
        bat_label.setStyleSheet("opacity: 0.2;")
        main_layout.addWidget(bat_label)

        # Command buttons
        preset_layout = QHBoxLayout()
        commands = {
            "Scan URL": "-u https://example.com",
            "Subdomains": "--subdomains https://example.com",
            "DNS Bruteforce": "--dns-bruteforce https://example.com",
            "Run All": "-a https://example.com"
        }
        for label, cmd in commands.items():
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, c=cmd: self.input_field.setText(c))
            preset_layout.addWidget(btn)
        main_layout.addLayout(preset_layout)

        # Input + Run + Save
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

        # Output
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        main_layout.addWidget(self.output_area)

        # Footer
        footer = QLabel()
        footer.setText(
            'Made by Talyx  |  <a href="https://github.com/Talyx66" style="color:#00cfff;">github.com/Talyx66</a>'
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setOpenExternalLinks(True)
        footer.setStyleSheet("color: #cccccc; font-size: 9pt;")
        main_layout.addWidget(footer)

        self.central_widget.setLayout(main_layout)

        # ==== AUDIO ====
        self.bg_audio = QMediaPlayer()
        self.bg_audio.setMedia(QMediaContent(QUrl.fromLocalFile("matx.mp3")))
        self.bg_audio.setVolume(10)
        self.bg_audio.play()
        self.bg_audio.mediaStatusChanged.connect(self.loop_audio)

        self.fang_sound = QSoundEffect()
        self.fang_sound.setSource(QUrl.fromLocalFile("fang.wav"))
        self.fang_sound.setVolume(0.6)

    def resizeEvent(self, event):
        self.video_widget.setGeometry(0, 0, self.width(), self.height())
        return super().resizeEvent(event)

    def loop_video(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.video_player.setPosition(0)
            self.video_player.play()

    def loop_audio(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.bg_audio.setPosition(0)
            self.bg_audio.play()

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
            color = "#cccccc"
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

    def play_scan_sound(self):
        self.fang_sound.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: black;
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
            background-color: rgba(17, 26, 40, 160);
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
