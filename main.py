# main.py
import sys
from PySide6.QtWidgets import QApplication
from app.core.database import create_db_and_tables
from app.views.main_window import MainWindow

if __name__ == "__main__":
    # Crea la base de datos y las tablas si no existen
    create_db_and_tables()
    
    app = QApplication(sys.argv)

    # Carga la hoja de estilos desde la nueva ubicación en 'assets'
    try:
        with open("app/assets/styles/main.qss", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Advertencia: No se encontró 'main.qss'. La aplicación se ejecutará sin estilos personalizados.")
    
    # Crea y muestra la ventana principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())