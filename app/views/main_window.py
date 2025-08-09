# app/views/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QWidget, QSizePolicy, QStatusBar, QLabel,
    QHBoxLayout, QStackedWidget
)
from PySide6.QtGui import QAction, QIcon, QActionGroup
from PySide6.QtCore import QSize, Qt

from app.views.pages.terminal_view import TerminalView
from app.views.pages.inventory_view import InventoryView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HorizonFlows POS")
        self.setGeometry(100, 100, 1440, 900)
        self.setMinimumSize(1280, 800)

        # --- Stack de páginas ---
        self.stack = QStackedWidget(self)
        self.terminal_page = TerminalView(self)
        self.inventory_page = InventoryView(self)

        self.stack.addWidget(self.terminal_page)   # index 0
        self.stack.addWidget(self.inventory_page)  # index 1
        self.setCentralWidget(self.stack)

        # --- Toolbar ---
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # Acciones navegables (exclusivas)
        nav_group = QActionGroup(self)
        nav_group.setExclusive(True)

        self.action_terminal = QAction(QIcon("app/assets/icons/terminal.svg"), "Terminal", self)
        self.action_terminal.setCheckable(True)
        self.action_terminal.setChecked(True)
        self.action_terminal.triggered.connect(lambda: self._switch_to(self.terminal_page))
        nav_group.addAction(self.action_terminal)
        toolbar.addAction(self.action_terminal)

        self.action_inventory = QAction(QIcon("app/assets/icons/inventory.svg"), "Inventario", self)
        self.action_inventory.setCheckable(True)
        self.action_inventory.triggered.connect(lambda: self._switch_to(self.inventory_page))
        nav_group.addAction(self.action_inventory)
        toolbar.addAction(self.action_inventory)

        # (Los demás botones siguen normales; aún no navegan)
        toolbar.addAction(QAction(QIcon("app/assets/icons/shopping-cart.svg"), "Compras", self))
        toolbar.addAction(QAction(QIcon("app/assets/icons/users.svg"), "Clientes", self))
        toolbar.addAction(QAction(QIcon("app/assets/icons/bar-chart.svg"), "Reportes", self))
        toolbar.addAction(QAction(QIcon("app/assets/icons/settings.svg"), "Ajustes", self))

        # --- Footer / Status bar ---
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

        lay.addWidget(left); lay.addStretch()
        lay.addWidget(center); lay.addStretch()
        lay.addWidget(right)

        status.addPermanentWidget(wrapper, 1)
        self.setStatusBar(status)

    # --- Helpers ---
    def _switch_to(self, widget: QWidget):
        """Cambia la página y sincroniza el check del toolbar."""
        self.stack.setCurrentWidget(widget)
        # Mantén el check acorde a la página actual
        if widget is self.terminal_page:
            self.action_terminal.setChecked(True)
        elif widget is self.inventory_page:
            self.action_inventory.setChecked(True)
