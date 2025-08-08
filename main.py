# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

# Importa la función para crear la base de datos del paso anterior
from app.core.database import create_db_and_tables

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Sistema POS")
        self.setGeometry(100, 100, 800, 600) # (x, y, ancho, alto)

        # Un simple widget de bienvenida por ahora
        label = QLabel("¡Bienvenido a tu Punto de Venta!", self)
        label.setGeometry(0, 0, 800, 600)
        label.setAlignment(Qt.AlignCenter)


if __name__ == "__main__":
    # 1. Crea la base de datos y las tablas al iniciar
    create_db_and_tables()

    # 2. Inicia la aplicación de la interfaz gráfica
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 3. Ejecuta el bucle de eventos de la aplicación
    sys.exit(app.exec())