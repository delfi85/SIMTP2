from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox

class ExponentialWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Distribución Exponencial")

        layout = QVBoxLayout()

        self.lambda_label = QLabel("Ingrese el valor de lambda:")
        layout.addWidget(self.lambda_label)

        self.lambda_entry = QLineEdit()
        layout.addWidget(self.lambda_entry)

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.confirm_lambda)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def confirm_lambda(self):
        lambda_value = self.lambda_entry.text()
        try:
            lambda_value = float(lambda_value)
            if lambda_value <= 0:
                QMessageBox.critical(self, "Error", "El valor de lambda debe ser mayor que 0.")
            else:
                QMessageBox.information(self, "Éxito", f"Valor de lambda aceptado: {lambda_value}")
                # Aquí puedes realizar cualquier acción adicional que desees con el valor de lambda
        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese un valor numérico para lambda.")
