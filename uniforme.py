from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal

class UniformWindow(QMainWindow):
    valuesConfirmed = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Distribución Uniforme")
        self.setGeometry(800, 50, 500, 200)

        # Creamos un widget central y un layout vertical
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Etiquetas y campos de entrada para A y B
        label_a = QLabel("Valor de A:")
        self.input_a = QLineEdit()
        layout.addWidget(label_a)
        layout.addWidget(self.input_a)

        label_b = QLabel("Valor de B:")
        self.input_b = QLineEdit()
        layout.addWidget(label_b)
        layout.addWidget(self.input_b)

        # Botón para confirmar valores
        confirm_button = QPushButton("Confirmar")
        confirm_button.clicked.connect(self.confirm_values)
        layout.addWidget(confirm_button)

    def confirm_values(self):
        a = self.input_a.text()
        b = self.input_b.text()

        try:
            a = float(a)
            b = float(b)

            if b <= a:
                raise ValueError("El valor de B debe ser mayor que el valor de A.")

            # Emitir la señal con los valores de A y B
            self.valuesConfirmed.emit(a, b)
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
