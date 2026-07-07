import sys

from PyQt6.QtWidgets import QApplication

from app.views.main_window import ImageGeneratorWindow


def main():
    app = QApplication(sys.argv)
    window = ImageGeneratorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
