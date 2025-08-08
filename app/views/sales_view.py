# app/views/sales_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class SalesView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title_label = QLabel("Punto de Venta")
        font = title_label.font()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)

        # 1. Creamos el botón
        self.process_sale_button = QPushButton("Procesar Venta")

        # 2. Conectamos la señal 'clicked' del botón a un nuevo método
        self.process_sale_button.clicked.connect(self.handle_process_sale)

        # Añadimos los widgets al layout
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.process_sale_button)
        layout.addStretch()

        self.setLayout(layout)

    # 3. Creamos el método que se ejecutará al hacer clic
    def handle_process_sale(self):
        """
        Esta función se llamará cada vez que se presione el botón.
        Por ahora, solo imprimirá un mensaje en la consola.
        """
        print("¡El botón 'Procesar Venta' fue presionado!")
        # Aquí es donde, en el futuro, añadirías la lógica para:
        # - Leer los productos del carrito de compras.
        # - Calcular el total.
        # - Guardar la venta en la base de datos (modelos Sale, SaleLine).
        # - Actualizar el stock del inventario.