from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QTextEdit
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
import cv2

class GestureView(QWidget):
    """View (V) — PyQt6. Emituje sygnały zdarzeń (space/backspace/reset).
    Odpowiedzialna tylko za prezentację i zbieranie zdarzeń od użytkownika.
    """
    spacePressed = pyqtSignal()
    backspacePressed = pyqtSignal()
    resetPressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Chodź i zamigaj! 😀')

        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)

        # przyciski pomocnicze
        btn_space = QPushButton('Spacja')
        btn_space.clicked.connect(lambda:self.spacePressed.emit())

        btn_reset = QPushButton('Resetuj tekst')
        btn_reset.clicked.connect(lambda: self.resetPressed.emit())

        btn_undo = QPushButton('Cofnij (Backspace)')
        btn_undo.clicked.connect(lambda: self.backspacePressed.emit())

        right_col = QVBoxLayout()
        right_col.addWidget(self.text_display)
        right_col.addWidget(btn_undo)
        right_col.addWidget(btn_space)
        right_col.addWidget(btn_reset)

        main_layout = QHBoxLayout()
        left = QVBoxLayout()
        left.addWidget(self.video_label)
        left.addWidget(self.progress)
        main_layout.addLayout(left)
        main_layout.addLayout(right_col)

        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        # bezpośrednio emitujemy sygnały — kontroler podłączy logikę
        if event.key() == Qt.Key.Key_Space:
            self.spacePressed.emit()
        elif event.key() == Qt.Key.Key_Backspace:
            self.backspacePressed.emit()
        else:
            super().keyPressEvent(event)

    def update_video(self, frame, overlay_text:str = None):
        # Oczekuje BGR (OpenCV) frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if overlay_text:
            cv2.putText(
                frame_rgb, overlay_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA
            )

        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def set_progress(self, value: int, text: str = ''):
        self.progress.setValue(value)
        if text:
            self.progress.setFormat(text)

    def set_text(self, text: str):
        self.text_display.setPlainText(text)
