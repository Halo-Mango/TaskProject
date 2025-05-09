from logic import *
import sys
def main():
    app = QApplication([])
    window = Logic()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()