# app/views/main_window.py
from PySide6.QtWidgets import QMainWindow, QToolBar, QWidget, QSizePolicy, QStatusBar, QLabel, QHBoxLayout
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize, Qt

# Importa la vista de la página del terminal desde su nueva ubicación
from app.views.pages.terminal_view import TerminalView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HorizonFlows POS")
        self.setGeometry(100, 100, 1440, 900)
        self.setMinimumSize(1280, 800)

        # --- Crear Barra de Herramientas ---
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        
        # Espaciador para empujar los iconos a la derecha
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # --- Acciones de la Barra de Herramientas (con rutas de iconos actualizadas) ---
        action_terminal = QAction(QIcon("app/assets/icons/terminal.svg"), "Terminal", self)
        action_terminal.setCheckable(True)
        action_terminal.setChecked(True)
        toolbar.addAction(action_terminal)
        
        toolbar.addAction(QAction(QIcon("app/assets/icons/inventory.svg"), "Inventario", self))
        toolbar.addAction(QAction(QIcon("app/assets/icons/shopping-cart.svg"), "Compras", self))
        toolbar.addAction(QAction(QIcon("app/assets/icons/users.svg"), "Clientes", self))
        toolbar.addAction(QAction(QIcon("app/assets/icons/bar-chart.svg"), "Reportes", self))
        toolbar.addAction(QAction(QIcon("app/assets/icons/settings.svg"), "Ajustes", self))

        # --- Establecer el Widget Central ---
        # La vista del terminal ahora se carga desde la subcarpeta 'pages'
        terminal_widget = TerminalView()
        self.setCentralWidget(terminal_widget)

        status = QStatusBar(self)
        wrapper = QWidget()
        wrapper.setObjectName("footer")
        lay = QHBoxLayout(wrapper)
        lay.setContentsMargins(16, 6, 16, 6)

        left  = QLabel("Estado: ● Conectado")
        center = QLabel("Última sincronización: 08/01/2025 14:32")
        right = QLabel("Caja: Terminal #1")

        for w in (left, center, right):
            w.setObjectName("footer_label")

        lay.addWidget(left)
        lay.addStretch()
        lay.addWidget(center)
        lay.addStretch()
        lay.addWidget(right)

        status.addPermanentWidget(wrapper, 1)
        self.setStatusBar(status)