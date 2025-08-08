# main.py
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QWidget, 
                               QSpacerItem, QSizePolicy)
from PySide6.QtGui import QAction, QIcon
# ▼▼▼ ¡Importa Qt para acceder a los estilos de botón! ▼▼▼
from PySide6.QtCore import QSize, Qt

from app.views.terminal_view import TerminalView
from app.core.database import create_db_and_tables

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HorizonFlows POS")
        self.setGeometry(100, 100, 1440, 900)
        self.setMinimumSize(1280, 800)

        # --- Create Toolbar ---
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        # ▼▼▼ ¡ESTA ES LA LÍNEA CLAVE! ▼▼▼
        # Le dice a la barra de herramientas que ponga el texto al lado del ícono.
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        # --- Spacer to push all items to the right ---
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # --- Add all toolbar actions ---
        action_terminal = QAction(QIcon("app/icons/terminal.svg"), "Terminal", self)
        action_terminal.setCheckable(True)
        action_terminal.setChecked(True)
        toolbar.addAction(action_terminal)
        
        toolbar.addAction(QAction(QIcon("app/icons/inventory.svg"), "Inventario", self))
        toolbar.addAction(QAction(QIcon("app/icons/shopping-cart.svg"), "Compras", self))
        toolbar.addAction(QAction(QIcon("app/icons/users.svg"), "Clientes", self))
        toolbar.addAction(QAction(QIcon("app/icons/bar-chart.svg"), "Reportes", self))
        
        toolbar.addAction(QAction(QIcon("app/icons/settings.svg"), "Settings", self))

        # --- Set the central widget ---
        terminal_widget = TerminalView()
        self.setCentralWidget(terminal_widget)

if __name__ == "__main__":
    # Create the database and tables if they don't exist
    create_db_and_tables()
    app = QApplication(sys.argv)

    # Load the stylesheet
    try:
        with open("app/views/styles.qss", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Warning: 'styles.qss' not found. The application will run without custom styles.")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())