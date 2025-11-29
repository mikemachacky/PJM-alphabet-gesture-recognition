import time
from PyQt6.QtCore import QTimer


COOLDOWN_SECONDS = 1.5
THRESHOLD = 0.8
SEQ_LENGTH = 30

class Controller:
    """Controller (C) — łączy widok i model oraz obsługuje sekwencję i timer.
    Timer jest tworzony z parentem view, więc działa w pętli Qt.
    """
    def __init__(self, model, camera, view):
        self.model = model
        self.camera = camera
        self.view = view
        self.sequence = []
        self.recognized_text = ''
        self.last_prediction_time = 0.0

        # połączenia sygnałów widoku
        self.view.spacePressed.connect(self.on_space)
        self.view.backspacePressed.connect(self.on_backspace)
        self.view.resetPressed.connect(self.on_reset)

        # timer aktualizujący klatki — 30 ms
        self.timer = QTimer(self.view)
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

    def on_space(self):

        self.recognized_text += ' '
        self.view.set_text(self.recognized_text)

    def on_backspace(self):
        self.recognized_text = self.recognized_text[:-1]
        self.view.set_text(self.recognized_text)

    def on_reset(self):
        self.recognized_text = ''
        self.view.set_text(self.recognized_text)

    def update(self):
        ok, frame, landmarks = self.camera.read()
        if not ok:
            return

        current_time = time.time()
        cooldown_remaining = max(0, COOLDOWN_SECONDS - (current_time - self.last_prediction_time))

        if landmarks is not None:
            self.sequence.append(landmarks)
            if len(self.sequence) == SEQ_LENGTH:
                try:
                    label, prob = self.model.predict(self.sequence)
                except Exception as e:
                    # jeśli model wyrzuci błąd, nie przerywamy aplikacji
                    print('Prediction error:', e)
                    label, prob = None, 0.0
                if label is not None and prob > THRESHOLD and cooldown_remaining == 0:
                    self.recognized_text += label
                    self.last_prediction_time = current_time

                self.sequence.pop(0)

        else:
            self.sequence = []

        # Aktualizacja widoku
        progress = int((1 - cooldown_remaining / COOLDOWN_SECONDS) * 100)
        self.view.set_progress(progress, f'Cooldown: {cooldown_remaining:.1f}s')
        self.view.update_video(frame)
        self.view.set_text(self.recognized_text)

    def stop(self):
        self.timer.stop()
        self.camera.release()
