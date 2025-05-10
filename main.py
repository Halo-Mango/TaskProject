"""
This file starts the Task App
It creates the application, opens the main window
to keep the app running
"""
from logic import *
import sys
def main():
    app = QApplication([])
    window = Logic()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()