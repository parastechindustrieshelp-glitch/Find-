import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTextBrowser, QLabel, QFrame)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from googleapiclient.discovery import build

# --- कॉन्फ़िगरेशन ---
API_KEY = "AIzaSyAgFEJCzD5O6XuFE8rCu2NbuoEwavV-c34"
CX_ID = "478b0e1f052504da2"

class MegaUltimateSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Home')
        self.setGeometry(100, 100, 450, 800) # मोबाइल जैसा पोर्ट्रेट मोड
        self.setStyleSheet("background-color: white; color: black;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 20)

        # "find" टाइटल (फोटो के अनुसार)
        header = QLabel('find')
        header.setFont(QFont('Arial', 48))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: black; margin-bottom: 20px;")
        layout.addWidget(header)

        # सर्च बार और आइकन सेक्शन
        search_container = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Find Every Thing')
        self.search_input.setStyleSheet("""
            border: none;
            border-bottom: 2px solid #777;
            font-size: 18px;
            padding: 5px;
            color: #333;
        """)
        self.search_input.returnPressed.connect(self.perform_search)
        
        # सर्च और माइक आइकन (सिंपल बटन के रूप में)
        search_btn = QPushButton('🔍')
        search_btn.setStyleSheet("border: none; font-size: 24px; background: transparent;")
        search_btn.clicked.connect(self.perform_search)

        mic_btn = QPushButton('🎤')
        mic_btn.setStyleSheet("border: none; font-size: 24px; background: transparent;")
        
        search_container.addWidget(self.search_input)
        search_container.addWidget(search_btn)
        search_container.addWidget(mic_btn)
        layout.addLayout(search_container)

        # "Powered by Brave" की तरह "Powered by Mega Ultimate"
        powered_by = QLabel('Powered by Mega Ultimate') # आप यहाँ Brave भी लिख सकते हैं
        powered_by.setAlignment(Qt.AlignCenter)
        powered_by.setStyleSheet("color: #555; font-size: 12px; margin-top: 5px;")
        layout.addWidget(powered_by)

        # रिजल्ट एरिया
        self.result_display = QTextBrowser()
        self.result_display.setOpenExternalLinks(True)
        self.result_display.setStyleSheet("border: none; background: white; margin-top: 20px;")
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def perform_search(self):
        query = self.search_input.text()
        if not query: return
        
        self.result_display.setHtml("<p style='text-align:center;'>Searching...</p>")
        
        try:
            service = build("customsearch", "v1", developerKey=API_KEY)
            res = service.cse().list(q=query, cx=CX_ID).execute()
            items = res.get('items', [])

            if items:
                html = ""
                for item in items:
                    html += f"<p><a href='{item['link']}' style='color:blue; font-size:16px;'>{item['title']}</a><br>{item['snippet']}</p><hr>"
                self.result_display.setHtml(html)
            else:
                self.result_display.setText("No results.")
        except Exception as e:
            self.result_display.setText(f"Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MegaUltimateSearch()
    ex.show()
    sys.exit(app.exec_())

