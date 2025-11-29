import os
import sys
from PyQt6.QtWidgets import QApplication

def resource_path(relative_path):
    """Zwraca poprawną ścieżkę do zasobów w PyInstaller --onefile."""
    if hasattr(sys, '_MEIPASS'):
        # zasoby wypakowane do katalogu tymczasowego
        return os.path.join(sys._MEIPASS, relative_path)
    # tryb developerski
    return os.path.join(os.path.dirname(__file__), relative_path)

# ścieżki i załadowanie etykiet
TFLITE_MODEL_PATH =  resource_path("model/migaj_small.tflite")
LABELS_PATH = resource_path("model/labels.txt")

with open(LABELS_PATH, 'r') as f:
    LABELS = [l.strip() for l in f.readlines()]

from model import GestureModel
from camera import Camera
from view import GestureView
from controller import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = GestureModel(TFLITE_MODEL_PATH, LABELS)
    camera = Camera(0)
    view = GestureView()

    controller = Controller(model, camera, view)

    view.show()

    exit_code = app.exec()
    controller.stop()
    sys.exit(exit_code)
