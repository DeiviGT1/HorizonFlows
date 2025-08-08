# app/views/products_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class ProductsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Título de la vista
        title_label = QLabel("Gestión de Productos")
        font = title_label.font()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)

        # Botón de ejemplo para esta vista
        self.add_product_button = QPushButton("Añadir Nuevo Producto")
        self.add_product_button.clicked.connect(self.handle_add_product)

        # Añadir widgets al layout
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.add_product_button)
        layout.addStretch()

        self.setLayout(layout)

    def handle_add_product(self):
        """
        Esta función se llamará cuando se presione el botón de añadir producto.
        """
        print("¡Botón 'Añadir Nuevo Producto' presionado!")
        # Aquí iría la lógica para abrir un formulario y crear un producto.