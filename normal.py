import sys
import tempfile

import openpyxl
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox, QApplication
import numpy as np
from test_chi2_normal import NormWindow
import pandas as pd
import os


class NormalWindow(QWidget):
    def __init__(self, numeros, k_intervalos):
        super().__init__()
        self.numeros = numeros
        self.k_intervalos = k_intervalos

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

    def box_muller_transform(self, u, mu, sigma):
        # Inicializa un vector vacío para almacenar los números generados
        z = np.empty(len(u))

        for i in range(0, len(u), 2):
            # Aplica la transformación de Box-Muller a cada par de elementos
            R = np.sqrt(-2.0 * np.log(u[i]))
            theta = 2.0 * np.pi * u[i + 1] if i + 1 < len(u) else 2.0 * np.pi * np.random.uniform(0, 1)
            z[i] = R * np.cos(theta)
            if i + 1 < len(u):
                z[i + 1] = R * np.sin(theta)

        # Ajusta los números generados a la media y la varianza deseadas
        z = mu + z * sigma

        return z

    def box_muller_transform2(self, numeros, mu, desviacion):
        # Inicializa un vector vacío para almacenar los números generados, pero comprueba
        # que el tamaño del vector sea par, ya que necesitamos siempre dos numeros para generar
        # otros dos, por lo tanto si sobra un numero se lo desprecia
        longitud = len(numeros)
        if longitud % 2 == 0:
            z = np.empty(longitud)
        else:
            z = np.empty(longitud - 1)

        # Usamos un for que vaya de 2 en 2 para tomar de a dos numeros en el vector, por eso es el 2 del final del range
        # Tambien usamos la longitud del vector vacio z, ya que debe ser par
        for i in range(0, len(z), 2):
            # Aplica la transformación de Box-Muller a cada par de elementos
            # Tenemos que aplicar la formula para convertir el vector de numeros random
            # Con la funcion max nos aseguramos que nunca aparezca un 0 que haga fallar al programa
            z[i] = round((np.sqrt((-2) * np.log(max(numeros[i], 0.0001))) * np.cos(2 * np.pi * numeros[i + 1])) * desviacion + mu, 4)
            z[i + 1] = round((np.sqrt((-2) * np.log(max(numeros[i], 0.0001))) * np.sin(2 * np.pi * numeros[i + 1])) * desviacion + mu, 4)

        # Esto lo imprime por consola para verificar si no tomamos el ultimo valor en caso de ser impar
        print(len(numeros), len(z))
        return z

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
                QMessageBox.information(self, "Éxito",
                                        f"Valores aceptados: Media={mean_value}, Varianza={variance_value}")
                # Aquí puedes realizar cualquier acción adicional que desees con la media y la varianza
                normales = self.box_muller_transform2(self.numeros, mean_value, variance_value)

                self.guardar_excel(normales)

                if np.isinf(normales).any():
                    print("El vector contiene al menos un valor infinito")
                else:
                    print("El vector no contiene valores infinitos")
                # Create an instance of App (the class that contains the table)
                self.table_window = NormWindow(normales, self.k_intervalos, mean_value, variance_value)

                # Especificamos el tamaño de la ventana de la tabla
                self.table_window.setGeometry(1200, 50, 1300, 1200)

                # Show the App window
                self.table_window.show()

                # Cierra la ventana actual
                self.close()

        except ValueError as e:
            QMessageBox.critical(self, "Error", "Por favor, ingrese valores numéricos para la media y la varianza.")
            print(e)

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

if __name__ == "__main__":
    # Datos de ejemplo
    numeros = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    k_intervalos = 4

    app = QApplication(sys.argv)
    window = NormalWindow(numeros, k_intervalos)
    window.show()
    sys.exit(app.exec_())
