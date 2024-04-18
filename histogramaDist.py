from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HistogramDistWindow(QWidget):
    def __init__(self, numeros, k_intervalos):
        super().__init__()
        self.setWindowTitle("Histograma")
        self.setGeometry(200, 50, 1000, 600)

        self.numeros = numeros
        self.k_intervalos = k_intervalos

        layout = QVBoxLayout(self)

        # Crear el canvas para el histograma
        self.figure_hist = Figure(figsize=(10, 6))
        self.canvas_hist = FigureCanvas(self.figure_hist)
        layout.addWidget(self.canvas_hist)

        # Crear etiquetas para mostrar los datos estadísticos
        self.label_N = QLabel()
        layout.addWidget(self.label_N)
        self.label_Maximo = QLabel()
        layout.addWidget(self.label_Maximo)
        self.label_Minimo = QLabel()
        layout.addWidget(self.label_Minimo)
        self.label_Rango = QLabel()
        layout.addWidget(self.label_Rango)
        self.label_Amplitud = QLabel()
        layout.addWidget(self.label_Amplitud)
        self.label_Media = QLabel()
        layout.addWidget(self.label_Media)
        self.label_VarMuestral = QLabel()
        layout.addWidget(self.label_VarMuestral)
        self.label_VarPoblacional = QLabel()
        layout.addWidget(self.label_VarPoblacional)

        # Actualizar los gráficos y mostrar los datos estadísticos
        self.mostrar_datos_estadisticos()

        # Actualizar los gráficos
        self.update_plots()

    def update_plots(self):
        self.plot_histogram()

    def plot_histogram(self):
        ax = self.figure_hist.add_subplot(111)
        ax.hist(self.numeros, bins=self.k_intervalos, color='skyblue', edgecolor='black')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Histograma de Números Aleatorios')
        ax.grid(True)
        self.canvas_hist.draw()

    def calcular_datos_estadisticos(self, numeros, k_intervalos):
        min_value = round(min(numeros), 4)
        max_value = round(max(numeros), 4)
        interval_length = round((max_value - min_value) / k_intervalos, 4)

        # Calcular los datos estadísticos necesarios
        n = len(numeros)
        range_value = round(max_value - min_value, 4)
        media = round(sum(numeros) / n, 4)
        variance_muestral = round(sum((x - media) ** 2 for x in numeros) / (n - 1), 4)
        variance_poblacional = round(sum((x - media) ** 2 for x in numeros) / n, 4)

        return {
            "N": n,
            "Máximo": max_value,
            "Mínimo": min_value,
            "Rango": range_value,
            "Amplitud": interval_length,
            "Media": media,
            "Varianza Muestral": variance_muestral,
            "Varianza Poblacional": variance_poblacional
        }

    def mostrar_datos_estadisticos(self):
        # Obtener los datos estadísticos
        datos_estadisticos = self.calcular_datos_estadisticos(self.numeros, self.k_intervalos)

        # Mostrar los datos estadísticos en las etiquetas
        self.label_N.setText(f"N: {datos_estadisticos['N']}")
        self.label_Maximo.setText(f"Máximo: {datos_estadisticos['Máximo']}")
        self.label_Minimo.setText(f"Mínimo: {datos_estadisticos['Mínimo']}")
        self.label_Rango.setText(f"Rango: {datos_estadisticos['Rango']}")
        self.label_Amplitud.setText(f"Amplitud: {datos_estadisticos['Amplitud']}")
        self.label_Media.setText(f"Media: {datos_estadisticos['Media']}")
        self.label_VarMuestral.setText(f"Varianza Muestral: {datos_estadisticos['Varianza Muestral']}")
        self.label_VarPoblacional.setText(f"Varianza Poblacional: {datos_estadisticos['Varianza Poblacional']}")
