from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox

class NormalWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Distribución Normal")

        layout = QVBoxLayout()

        self.mean_label = QLabel("Ingrese el valor de la media:")
        layout.addWidget(self.mean_label)

        self.mean_entry = QLineEdit()
        layout.addWidget(self.mean_entry)

        self.variance_label = QLabel("Ingrese el valor de la varianza:")
        layout.addWidget(self.variance_label)

        self.variance_entry = QLineEdit()
        layout.addWidget(self.variance_entry)

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.confirm_parameters)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def confirm_parameters(self):
        mean_value = self.mean_entry.text()
        variance_value = self.variance_entry.text()
        try:
            mean_value = float(mean_value)
            variance_value = float(variance_value)
            if variance_value <= 0:
                QMessageBox.critical(self, "Error", "La varianza debe ser mayor que 0.")
            elif mean_value < 0:
                QMessageBox.critical(self, "Error", "La media debe ser mayor o igual que 0.")
            else:
                QMessageBox.information(self, "Éxito", f"Valores aceptados: Media={mean_value}, Varianza={variance_value}")
                # Aquí puedes realizar cualquier acción adicional que desees con la media y la varianza
        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese valores numéricos para la media y la varianza.")
