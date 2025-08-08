# app/views/pages/terminal_view.py
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QFormLayout, QComboBox, QGroupBox,
    QFrame, QButtonGroup, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

class TerminalView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # El layout principal ahora es vertical para poder añadir el footer abajo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Layout para el contenido principal (paneles izquierdo y derecho)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        left_panel = self._create_left_panel()
        right_panel = self._create_right_panel()

        content_layout.addWidget(left_panel, 7)
        content_layout.addWidget(right_panel, 3)

        # Footer
        footer = self._create_footer()

        main_layout.addLayout(content_layout, 1) # El '1' hace que el contenido se expanda
        main_layout.addWidget(footer)


    def _get_icon(self, name):
        return QIcon(f"app/assets/icons/{name}")

    def _create_search_bar(self):
        search_container = QWidget()
        search_container.setObjectName("search_container")
        search_container.setFixedHeight(48)
        
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 0, 5, 0)
        search_layout.setSpacing(10)

        icon_label = QLabel()
        pixmap = QPixmap("app/assets/icons/search.svg")
        icon_label.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Escanear código o buscar producto...")
        self.search_input.setObjectName("search_input")

        search_layout.addWidget(icon_label)
        search_layout.addWidget(self.search_input)
        
        return search_container

    def _create_left_panel(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        top_layout = QHBoxLayout()
        search_widget = self._create_search_bar()
        
        options_button = QPushButton("Opciones")
        options_button.setObjectName("options_button")
        options_button.setFixedHeight(48)

        top_layout.addWidget(search_widget, 1)
        top_layout.addWidget(options_button)
        
        order_box = QGroupBox("Artículos en la Orden")
        order_layout = QVBoxLayout(order_box)

        # --- AJUSTES DE LA TABLA ---
        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(5) # Ahora son 5 columnas
        self.order_items_table.setHorizontalHeaderLabels(["Producto", "Cant.", "P. Unitario", "P. Total", ""])
        
        self.order_items_table.verticalHeader().setVisible(False)
        header = self.order_items_table.horizontalHeader()
        header.setObjectName("order_header") # Para darle estilo con QSS
        
        # Modos de tamaño de las columnas para un mejor ajuste
        header.setSectionResizeMode(0, QHeaderView.Stretch)           # Producto: se estira
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # Cantidad: se ajusta al contenido
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # P. Unitario: se ajusta al contenido
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # P. Total: se ajusta al contenido
        header.setSectionResizeMode(4, QHeaderView.Fixed)             # Borrar: tamaño fijo

        self.order_items_table.setColumnWidth(4, 50) # Ancho para el botón de borrar

        self.order_items_table.setShowGrid(False)
        self.order_items_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.order_items_table.setFocusPolicy(Qt.NoFocus)

        self._populate_sample_data(self.order_items_table)
        order_layout.addWidget(self.order_items_table)

        action_buttons_layout = QHBoxLayout()
        clear_button = QPushButton(" Limpiar Todo")
        clear_button.setIcon(self._get_icon("trash-2.svg"))
        suspend_button = QPushButton(" Suspender") # Puedes añadir un ícono si lo deseas
        
        # Asignamos el nombre de objeto para aplicar el estilo oscuro desde QSS
        clear_button.setObjectName("dark_button")
        suspend_button.setObjectName("dark_button")

        action_buttons_layout.addStretch()
        action_buttons_layout.addWidget(clear_button)
        action_buttons_layout.addWidget(suspend_button)
        action_buttons_layout.addStretch()

        layout.addLayout(top_layout)
        layout.addWidget(order_box, 1)
        layout.addLayout(action_buttons_layout)
        return container

    def _create_right_panel(self):
        # El panel derecho se mantiene como en la versión anterior
        # ... (código del panel derecho sin cambios)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        customer_box = QGroupBox("Cliente")
        customer_layout = QVBoxLayout(customer_box)
        customer_combo = QComboBox()
        customer_combo.addItem("Cliente General")
        customer_combo.setFixedHeight(48)
        customer_layout.addWidget(customer_combo)

        # --- RESUMEN DE ORDEN MEJORADO ---
        summary_box = QGroupBox("Resumen de Orden")
        summary_layout = QVBoxLayout(summary_box)
        summary_layout.setSpacing(10)

        # Total de Productos
        total_items_layout = QHBoxLayout()
        self.total_items_label = QLabel("Total de Productos")
        self.total_items_label.setObjectName("summary_label_bold")
        self.total_items_value = QLabel("3 unidades") # Ejemplo, esto debe ser dinámico
        self.total_items_value.setObjectName("summary_label_bold")
        self.total_items_value.setAlignment(Qt.AlignRight)
        total_items_layout.addWidget(self.total_items_label)
        total_items_layout.addWidget(self.total_items_value)
        summary_layout.addLayout(total_items_layout)
        
        line_top = QFrame(); line_top.setFrameShape(QFrame.HLine); line_top.setObjectName("summary_line")
        summary_layout.addWidget(line_top)

        # Formulario para subtotal, impuestos, etc.
        details_layout = QFormLayout()
        details_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        details_layout.setSpacing(8)
        
        details_layout.addRow(QLabel("Subtotal:"), QLabel("$75.50"))
        details_layout.addRow(QLabel("Impuestos (16%):"), QLabel("$12.08"))
        details_layout.addRow(QLabel("Descuento:"), QLabel("-$0.00"))
        summary_layout.addLayout(details_layout)

        line_bottom = QFrame(); line_bottom.setFrameShape(QFrame.HLine); line_bottom.setObjectName("summary_line")
        summary_layout.addWidget(line_bottom)
        
        # Total final
        total_layout = QHBoxLayout()
        total_label = QLabel("Total:")
        total_label.setObjectName("total_label")
        total_value = QLabel("$87.58") # Ejemplo, dinámico
        total_value.setObjectName("total_value")
        total_value.setAlignment(Qt.AlignRight)
        total_layout.addWidget(total_label)
        total_layout.addWidget(total_value)
        summary_layout.addLayout(total_layout)

        payment_method_box = QGroupBox("Método de Pago")
        payment_method_layout = QHBoxLayout(payment_method_box)
        cash_button = QPushButton(" Efectivo"); cash_button.setObjectName("payment_method_button"); cash_button.setIcon(self._get_icon("dollar-sign.svg")); cash_button.setCheckable(True); cash_button.setChecked(True)
        card_button = QPushButton(" Tarjeta"); card_button.setObjectName("payment_method_button"); card_button.setIcon(self._get_icon("credit-card.svg")); card_button.setCheckable(True)
        self.payment_method_group = QButtonGroup(self); self.payment_method_group.addButton(cash_button); self.payment_method_group.addButton(card_button); self.payment_method_group.setExclusive(True)
        payment_method_layout.addWidget(cash_button); payment_method_layout.addWidget(card_button)

        payment_details_layout = QFormLayout()
        payment_details_layout.setContentsMargins(0, 5, 0, 5)
        received_amount_input = QLineEdit("$87.58"); received_amount_input.setFixedHeight(48)
        change_label = QLabel("$0.00"); change_label.setAlignment(Qt.AlignRight)
        payment_details_layout.addRow(QLabel("Monto Recibido:"), received_amount_input)
        payment_details_layout.addRow(QLabel("Cambio:"), change_label)

        process_payment_button = QPushButton("Procesar Pago"); process_payment_button.setObjectName("process_payment_button"); process_payment_button.setFixedHeight(50)

        final_actions_layout = QHBoxLayout()
        final_actions_layout.setSpacing(15)
        print_button = QPushButton(" Imprimir"); print_button.setObjectName("final_action_button"); print_button.setIcon(self._get_icon("printer.svg"))
        email_button = QPushButton(" Email"); email_button.setObjectName("final_action_button"); email_button.setIcon(self._get_icon("mail.svg"))
        final_actions_layout.addStretch(); final_actions_layout.addWidget(print_button); final_actions_layout.addWidget(email_button); final_actions_layout.addStretch()

        layout.addWidget(customer_box)
        layout.addWidget(summary_box)
        layout.addWidget(payment_method_box)
        layout.addLayout(payment_details_layout)
        layout.addStretch()
        layout.addWidget(process_payment_button)
        layout.addLayout(final_actions_layout)
        return container

    def _create_footer(self):
        footer_widget = QWidget()
        footer_widget.setObjectName("footer")
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(20, 10, 20, 10)

        # Información del footer
        user_label = QLabel("<b>Usuario:</b> David Ortega")
        cash_register_label = QLabel("<b>Caja:</b> Terminal #1")
        status_label = QLabel("<b>Estado:</b> Conectado")
        
        user_label.setObjectName("footer_label")
        cash_register_label.setObjectName("footer_label")
        status_label.setObjectName("footer_label")

        footer_layout.addWidget(user_label)
        footer_layout.addStretch()
        footer_layout.addWidget(cash_register_label)
        footer_layout.addStretch()
        footer_layout.addWidget(status_label)
        
        return footer_widget
        
    def _populate_sample_data(self, table: QTableWidget):
        sample_items = [
            {"name": "Coca Cola 500ml Sin Azúcar", "sku": "CC500SA", "qty": 2, "price": 12.50},
            {"name": "Pan Bimbo Blanco Integral Grande", "sku": "PB001", "qty": 1, "price": 32.50},
            {"name": "Leche Descremada Lala 1L", "sku": "LD1000", "qty": 1, "price": 18.00},
        ]
        table.setRowCount(len(sample_items))

        for row, item in enumerate(sample_items):
            # Columna 0: Widget de Producto (Nombre y SKU)
            product_widget = QWidget()
            product_layout = QVBoxLayout(product_widget)
            product_layout.setContentsMargins(10, 8, 10, 8)
            product_layout.setSpacing(2)
            product_name_label = QLabel(item["name"])
            product_name_label.setObjectName("product_name_label")
            sku_label = QLabel(f"SKU: {item['sku']}")
            sku_label.setObjectName("sku_label")
            product_layout.addWidget(product_name_label)
            product_layout.addWidget(sku_label)
            table.setCellWidget(row, 0, product_widget)

            # Columna 1: Widget de Cantidad
            qty_input = QLineEdit(str(item['qty']))
            qty_input.setObjectName("quantity_input")
            qty_input.setAlignment(Qt.AlignCenter)
            qty_input.setFixedSize(50, 32)
            qty_container = QWidget()
            qty_layout = QHBoxLayout(qty_container)
            qty_layout.setContentsMargins(0,0,0,0)
            qty_layout.setAlignment(Qt.AlignCenter)
            qty_layout.addWidget(qty_input)
            table.setCellWidget(row, 1, qty_container)

            # Columna 2: Precio Unitario
            unit_price_item = QTableWidgetItem(f"${item['price']:.2f}")
            unit_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            unit_price_item.setFlags(unit_price_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 2, unit_price_item)

            # Columna 3: Precio Total
            total_price = item['price'] * item['qty']
            total_price_item = QTableWidgetItem(f"${total_price:.2f}")
            total_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            font = total_price_item.font()
            font.setBold(True)
            total_price_item.setFont(font)
            total_price_item.setFlags(total_price_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 3, total_price_item)
            
            # Columna 4: Botón de Borrar
            delete_btn_container = QWidget()
            delete_btn_layout = QHBoxLayout(delete_btn_container)
            delete_btn_layout.setContentsMargins(0,0,0,0)
            delete_btn_layout.setAlignment(Qt.AlignCenter)
            delete_btn = QPushButton()
            delete_btn.setIcon(self._get_icon("trash-2.svg"))
            delete_btn.setObjectName("delete_button")
            delete_btn.setFixedSize(32, 32)
            delete_btn_layout.addWidget(delete_btn)
            table.setCellWidget(row, 4, delete_btn_container)

            table.setRowHeight(row, 60)