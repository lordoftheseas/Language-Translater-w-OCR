import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from translate import Translator
import easyocr

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Example GUI")
        self.setWindowIcon(QIcon("profile.png"))

        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafafa;
            }
            QLabel {
                font-family: Arial, sans-serif;
                font-size: 14pt;
                padding: 10px;
            }
            QTextEdit, QTextBrowser {
                font-family: Arial, sans-serif;
                font-size: 12pt;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QComboBox {
                font-family: Arial, sans-serif;
                font-size: 12pt;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                font-family: Arial, sans-serif;
                font-size: 12pt;
                background-color: #5cb85c;
                color: #fff;
                padding: 10px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QToolBar QToolButton {
                color: black;
                border: 1px solid black;
                padding: 5px;
                border-radius: 4px;
                background-color: #fff;
            }
            QToolBar QToolButton:hover {
                background-color: #f0f0f0;
            }
            QToolBar QToolButton:checked, QToolBar QToolButton:pressed {
                background-color: #ddd;
            }
        """)

        # EasyOCR Reader
        self.reader = easyocr.Reader(['en'])

        self.output = QTextEdit()
        self.input = QTextEdit()
        self.file_display = QTextBrowser()
        self.file_display.setFixedHeight(50)  # Set the fixed height of the file name display

        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

        self.button_action = QAction("File", self)
        self.button_action.setStatusTip("Choose a file!")
        self.button_action.triggered.connect(self.open_file_dialog)
        self.toolbar.addAction(self.button_action)

        self.setStatusBar(QStatusBar(self))

        # Dropdown menu for language selection
        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems(["Japanese", "German", "French", "Chinese"])

        # Button to trigger translation
        self.translate_button = QPushButton("Translate")
        self.translate_button.clicked.connect(self.translate_text)

        layout = QVBoxLayout()
        layout.addWidget(self.file_display)
        layout.addWidget(self.input)
        layout.addWidget(self.language_dropdown)
        layout.addWidget(self.translate_button)
        layout.addWidget(self.output)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window
        self.setCentralWidget(container)
    
        self.show_popup()

    def show_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("File button allows you to select images to extract text from them")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "Images (*.png *.jpeg *.jpg)")

        if file_path:
            self.file_display.setHtml(f"<b>Selected File:</b> {file_path}")
            self.selected_file_path = file_path

            # Read text from the image using EasyOCR
            result = self.reader.readtext(file_path)
            if result:
                text_in_image = "\n".join([detection[1] for detection in result])
                self.input.setText(text_in_image)

    def translate_text(self):
        # Get the text from the QTextEdit
        text = self.input.toPlainText()

        # Get the selected language from the dropdown
        target_language = self.language_dropdown.currentText()
        language_code = {
            'Japanese': 'ja',
            'German': 'de',
            'French': 'fr',
            'Chinese': 'zh'
        }.get(target_language, 'en')

        translator = Translator(to_lang=language_code)
        translation = translator.translate(text)
        self.output.setText(translation)
        self.output.setStyleSheet("color: black; font-size: 14pt; background-color: #e0f7fa; padding: 5px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
