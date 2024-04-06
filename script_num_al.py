from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, \
    QMessageBox, QFrame
import random
import openpyxl
import tempfile
import os
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar tamaño de la ventana
        self.resize(500, 300)  # Tamaño personalizado

        # Configurar layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Parte superior: Texto "RANDOM NUMBERS"
        random_numbers_label = QLabel("RANDOM NUMBERS")
        random_numbers_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        random_numbers_label.setFont(QFont("Haettenschweiler", 24))
        layout.addWidget(random_numbers_label)

        # Añadir línea negra debajo del título "RANDOM NUMBERS"
        line_top = QFrame()
        line_top.setFrameShape(QFrame.HLine)
        line_top.setFrameShadow(QFrame.Sunken)
        line_top.setStyleSheet("color: black")
        layout.addWidget(line_top)

        # Crear un layout horizontal para los campos de entrada "Cantidad" y "K-Intervalos"
        cantidad_layout = QHBoxLayout()

        cantidad_label = QLabel("Cantidad:")
        cantidad_layout.addWidget(cantidad_label)
        self.cantidad_entry = QLineEdit()
        cantidad_layout.addWidget(self.cantidad_entry)

        k_intervalos_label = QLabel("K-Intervalos:")
        cantidad_layout.addWidget(k_intervalos_label)
        self.k_intervalos_entry = QLineEdit()
        cantidad_layout.addWidget(self.k_intervalos_entry)
        self.k_intervalos_entry.setValidator(QIntValidator(10, 25))  # Restringe la entrada a valores entre 10 y 25

        # Añadir el layout horizontal al layout principal
        layout.addLayout(cantidad_layout)

        # Crear un layout horizontal para los botones "Generar" y "Cancelar"
        buttons_layout = QHBoxLayout()

        self.generar_button = QPushButton("Generar")
        buttons_layout.addWidget(self.generar_button)

        self.cancelar_button = QPushButton("Cancelar")
        buttons_layout.addWidget(self.cancelar_button)

        # Añadir el layout de botones al layout principal
        layout.addLayout(buttons_layout)

        # Conectar botón "Generar" a la función de generación de números aleatorios
        self.generar_button.clicked.connect(self.generar_aleatorios)

        # Habilitar generación al presionar la tecla Enter
        self.cantidad_entry.returnPressed.connect(self.generar_aleatorios)

        # Conectar botón "Cancelar" para cerrar la aplicación
        self.cancelar_button.clicked.connect(self.close)

        self.setWindowTitle("Generador de números aleatorios")

    def generar_numeros_aleatorios(self, cantidad, k_intervalos):
        numeros_aleatorios = []
        for _ in range(cantidad):
            numero = round(random.random(), 4)
            numeros_aleatorios.append(numero)
        return numeros_aleatorios

    def guardar_excel(self, numeros):
        # Crear archivo Excel
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Numeros Aleatorios"

        for i, numero in enumerate(numeros, start=1):
            sheet.cell(row=i, column=1, value=numero)

        # Guardar archivo Excel como archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            temp_filename = temp_file.name
            wb.save(temp_filename)

        # Abrir el archivo temporal en el sistema
        os.startfile(temp_filename)

    def generar_aleatorios(self):
        cantidad = self.cantidad_entry.text()
        k_intervalos = self.k_intervalos_entry.text()

        if not cantidad or not k_intervalos:
            QMessageBox.critical(self, "Error", "Por favor, complete todos los campos.")
            return

        try:
            cantidad = int(cantidad)
            k_intervalos = int(k_intervalos)

            if cantidad <= 0:
                QMessageBox.critical(self, "Error", "Por favor ingrese un número positivo mayor que 0.")
                return

            if k_intervalos not in [10, 15, 20, 25]:
                QMessageBox.critical(self, "Error",
                                     "Por favor ingrese uno de los siguientes K-Intervalos: 10, 15, 20, 25.")
                return

            if cantidad > 1000000:
                QMessageBox.critical(self, "Error", "El límite máximo es de un millón de números aleatorios.")
                return

            numeros = self.generar_numeros_aleatorios(cantidad, k_intervalos)
            self.guardar_excel(numeros)

        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese números enteros válidos en ambos campos.")


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
