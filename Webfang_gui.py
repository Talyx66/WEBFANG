import sys
import time
from PyQt5.QtWidgets import ( 
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QTextCursor, QPixmap, QMovie
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from concurrent.futures import ThreadPoolExecutor

# Import your existing modules
from modules import dnsdumpster, headers, shodan_lookup, spider, urlscan, whois_lookup

class WebFangGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WEBFANG")
        self.setGeometry(200, 200, 1000, 750)

        # === ORIGINAL BACKGROUND & MATRIX ===
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("Talyxlogo.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.bg_label.setGeometry(200, 300, self.width(), self.height())
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        self.matrix_label = QLabel(self)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.2)
        self.matrix_label.setGraphicsEffect(opacity_effect)
        self.matrix_movie = QMovie("blue_matrix_rain.gif")
        self.matrix_label.setMovie(self.matrix_movie)
        self.matrix_movie.start()
        self.matrix_label.setGeometry(0, 0, 120, 200)
        self.matrix_label.setScaledContents(True)
        self.matrix_label.lower()
        self.matrix_label.stackUnder(self.bg_label)

        # Central widget
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: rgba(0, 0, 0, 15);")
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()

        # Neon text logo
        logo_label = QLabel("WEBFANG")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Bat logo
        bat_label = QLabel(self.central_widget)
        bat_pixmap = QPixmap("2749.png").scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        bat_label.setPixmap(bat_pixmap)
        bat_label.setAlignment(Qt.AlignCenter)
        bat_label.setStyleSheet("opacity: 0.2;")
        bat_label.setAttribute(Qt.WA_TranslucentBackground)
        main_layout.insertWidget(1, bat_label)

        # === PRESET BUTTONS ===
        preset_layout = QHBoxLayout()
        buttons = {
            "Scan URL": self.run_url_scan,
            "Subdomains": self.run_subdomains,
            "DNS Bruteforce": self.run_dns_bruteforce,
            "Headers": self.run_headers,
            "Shodan": self.run_shodan,
            "WHOIS": self.run_whois,
            "Spider": self.run_spider,
            "Run All": self.run_all
        }
        for name, func in buttons.items():
            btn = QPushButton(name)
            btn.clicked.connect(func)
            preset_layout.addWidget(btn)
        main_layout.addLayout(preset_layout)

        # Input + Save
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter target, e.g., example.com")
        input_layout.addWidget(self.input_field)

        self.save_button = QPushButton("Save Output")
        self.save_button.clicked.connect(self.save_output)
        input_layout.addWidget(self.save_button)
        main_layout.addLayout(input_layout)

        # Output
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        main_layout.addWidget(self.output_area)

        # Footer
        footer = QLabel('Made by Talyx  |  <a href="https://github.com/Talyx66" style="color:#00cfff;">github.com/Talyx66</a>')
        footer.setAlignment(Qt.AlignCenter)
        footer.setOpenExternalLinks(True)
        footer.setStyleSheet("color: #aaaaaa; font-size: 10pt; padding: 6px;")
        main_layout.addWidget(footer)

        self.central_widget.setLayout(main_layout)

        # Audio
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("matx.mp3")))
        self.player.setVolume(10)
        self.player.play()
        self.player.mediaStatusChanged.connect(self.handle_media_status)

        self.fang_sound = QSoundEffect()
        self.fang_sound.setSource(QUrl.fromLocalFile("fang.wav"))
        self.fang_sound.setVolume(0.6)

    # === RESIZE EVENT ===
    def resizeEvent(self, event):
        self.bg_label.setPixmap(QPixmap("Talyxlogo.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.matrix_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    # === OUTPUT HELPERS ===
    def animate_output(self, text):
        self.output_area.moveCursor(QTextCursor.End)
        for line in text if isinstance(text, list) else [text]:
            self.append_colored_line(str(line))
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

    # === SAVE OUTPUT ===
    def save_output(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Output", "webfang_output.txt", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.output_area.toPlainText())
                QMessageBox.information(self, "Saved", f"Output saved to {filename}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save: {e}")

    # === AUDIO ===
    def play_scan_sound(self):
        self.fang_sound.play()

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    # === MODULE RUNNERS ===
    def run_url_scan(self):
        target = self.input_field.text().strip()
        if target:
            self.play_scan_sound()
            self.animate_output(urlscan.scan(target))

    def run_subdomains(self):
        target = self.input_field.text().strip()
        if target:
            self.play_scan_sound()
            self.animate_output(spider.subdomain_enum(target))

    def run_dns_bruteforce(self):
        target = self.input_field.text().strip()
        if target:
            self.play_scan_sound()
            self.animate_output(dnsdumpster.dns_bruteforce(target))

    def run_headers(self):
        target = self.input_field.text().strip()
        if target:
            self.play_scan_sound()
            self.animate_output(headers.scan(target))

    def run_shodan(self):
        target = self.input_field.text().strip()
        if target:
            self.play_scan_sound()
            self.animate_output(shodan_lookup(target))

    def run_whois(self):
        target = self.input_field.text().strip()
        if target:
            self.play_scan_sound()
            self.animate_output(whois_lookup.run(target))

    def run_spider(self):
        target = self.input_field.text().strip()
        if target:
            self.play_scan_sound()
            self.animate_output(spider.crawl(target))

    def run_all(self):
        target = self.input_field.text().strip()
        if not target:
            self.output_area.append("[!] Please enter a target.\n")
            return
        self.play_scan_sound()
        funcs = [self.run_url_scan, self.run_subdomains, self.run_dns_bruteforce,
                 self.run_headers, self.run_shodan, self.run_whois, self.run_spider]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(f) for f in funcs]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    self.output_area.append(f"[!] Error: {e}")

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

