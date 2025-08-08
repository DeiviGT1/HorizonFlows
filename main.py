# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, QSpacerItem, QSizePolicy
from PySide6.QtGui import QAction, QIcon
from app.views.terminal_view import TerminalView
from app.core.database import create_db_and_tables

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HorizonFlows POS")
        self.setGeometry(100, 100, 1440, 900)

        # --- Create Toolbar ---
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        action_terminal = QAction("Terminal", self)
        action_terminal.setCheckable(True)
        action_terminal.setChecked(True)
        
        toolbar.addAction(action_terminal)
        toolbar.addAction(QAction("Inventario", self))
        toolbar.addAction(QAction("Compras", self))
        toolbar.addAction(QAction("Clientes", self))
        toolbar.addAction(QAction("Reportes", self))

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addAction(QAction("Settings", self)) # Placeholder for settings icon

        # Set the terminal view as the central widget
        terminal_widget = TerminalView()
        self.setCentralWidget(terminal_widget)

if __name__ == "__main__":
    create_db_and_tables()
    app = QApplication(sys.argv)

    # Load the stylesheet
    try:
        with open("app/views/styles.qss", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Advertencia: No se encontró 'styles.qss'.")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())