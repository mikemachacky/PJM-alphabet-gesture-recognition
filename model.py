import numpy as np
import tensorflow as tf

SEQ_LENGTH = 30

class GestureModel:
    """Model (M) — odpowiedzialny za ładowanie TFLite i predykcję."""
    def __init__(self, tflite_path: str, labels: list):
        self.tflite_path = tflite_path
        self.labels = labels
        self.interpreter = tf.lite.Interpreter(model_path=self.tflite_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def _normalize_sequence(self, sequence_array):
        seq = np.array(sequence_array)
        origin = seq[0][0]
        return seq - origin

    def predict(self, sequence):
        """Oczekuje listy SEQ_LENGTH elementów, każdy 21x3 (=63). Zwraca (label, prob)."""
        seq = np.array(sequence)
        if seq.shape != (SEQ_LENGTH, 21, 3):
            raise ValueError(f"Nieprawidłowy kształt sekwencji: {seq.shape}")
        norm = self._normalize_sequence(seq)
        input_data = norm.reshape(1, SEQ_LENGTH, 63).astype(np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        idx = int(np.argmax(output))
        return self.labels[idx], float(np.max(output))