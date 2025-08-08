# app/views/terminal_view.py
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QFormLayout, QComboBox, QGroupBox,
    QSpacerItem, QSizePolicy, QAbstractItemView
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class TerminalView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 20)
        main_layout.setSpacing(20)

        left_panel = self._create_left_panel()
        right_panel = self._create_right_panel()

        main_layout.addWidget(left_panel, 7)
        main_layout.addWidget(right_panel, 3)

    def _get_icon(self, name):
        # Helper to get icons from our folder
        return QIcon(f"app/icons/{name}")

    def _create_left_panel(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Escanear código o buscar producto...")
        search_input.setFixedHeight(45)
        options_button = QPushButton("Opciones")
        options_button.setObjectName("secondary_action_button")
        options_button.setFixedHeight(45)

        search_layout.addWidget(search_input)
        search_layout.addWidget(options_button)

        order_box = QGroupBox("Artículos en la Orden")
        order_layout = QVBoxLayout(order_box)

        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(4)
        self.order_items_table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio", ""])
        header = self.order_items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.order_items_table.verticalHeader().setVisible(False)
        self.order_items_table.setShowGrid(False)
        self.order_items_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.order_items_table.setFocusPolicy(Qt.NoFocus)

        self._populate_sample_data(self.order_items_table)
        order_layout.addWidget(self.order_items_table)

        action_buttons_layout = QHBoxLayout()
        clear_button = QPushButton("Limpiar Todo")
        suspend_button = QPushButton("Suspender")
        clear_button.setObjectName("secondary_action_button")
        suspend_button.setObjectName("secondary_action_button")
        clear_button.setFixedHeight(45)
        suspend_button.setFixedHeight(45)
        action_buttons_layout.addStretch()
        action_buttons_layout.addWidget(clear_button)
        action_buttons_layout.addWidget(suspend_button)

        layout.addLayout(search_layout)
        layout.addWidget(order_box)
        layout.addLayout(action_buttons_layout)
        return container

    def _create_right_panel(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        customer_box = QGroupBox("Cliente")
        customer_layout = QVBoxLayout(customer_box)
        customer_combo = QComboBox()
        customer_combo.addItem("Cliente General")
        customer_combo.setFixedHeight(45)
        customer_layout.addWidget(customer_combo)

        summary_box = QGroupBox("Resumen de Orden")
        summary_layout = QFormLayout(summary_box)
        summary_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        summary_layout.setSpacing(10)

        subtotal_label = QLabel("Subtotal:"); subtotal_label.setObjectName("summary_label")
        subtotal_value = QLabel("$7.55"); subtotal_value.setObjectName("summary_value")
        taxes_label = QLabel("Impuestos (16%):"); taxes_label.setObjectName("summary_label")
        taxes_value = QLabel("$1.21"); taxes_value.setObjectName("summary_value")
        discount_label = QLabel("Descuento:"); discount_label.setObjectName("summary_label")
        discount_value = QLabel("-$0.00"); discount_value.setObjectName("summary_value")
        total_label = QLabel("Total:"); total_label.setObjectName("total_label")
        total_value = QLabel("$8.76"); total_value.setObjectName("total_value")

        summary_layout.addRow(subtotal_label, subtotal_value)
        summary_layout.addRow(taxes_label, taxes_value)
        summary_layout.addRow(discount_label, discount_value)
        summary_layout.addRow(QLabel()) # Spacer
        summary_layout.addRow(total_label, total_value)

        payment_method_box = QGroupBox("Método de Pago")
        payment_method_layout = QHBoxLayout(payment_method_box)
        cash_button = QPushButton(" Efectivo"); cash_button.setObjectName("payment_method_button")
        cash_button.setIcon(self._get_icon("dollar-sign.svg")); cash_button.setCheckable(True); cash_button.setChecked(True)
        card_button = QPushButton(" Tarjeta"); card_button.setObjectName("payment_method_button")
        card_button.setIcon(self._get_icon("credit-card.svg")); card_button.setCheckable(True)
        payment_method_layout.addWidget(cash_button); payment_method_layout.addWidget(card_button)

        payment_details_box = QGroupBox()
        payment_details_box.setFlat(True) # No border/title
        payment_details_layout = QFormLayout(payment_details_box)
        payment_details_layout.setContentsMargins(0,0,0,0)
        received_amount_input = QLineEdit("$8.76")
        change_label = QLabel("$0.00")
        payment_details_layout.addRow(QLabel("Monto Recibido:"), received_amount_input)
        payment_details_layout.addRow(QLabel("Cambio:"), change_label)

        process_payment_button = QPushButton("Procesar Pago")
        process_payment_button.setObjectName("process_payment_button")
        process_payment_button.setFixedHeight(50)

        final_actions_layout = QHBoxLayout()
        print_button = QPushButton(" Imprimir"); print_button.setObjectName("secondary_action_button")
        print_button.setIcon(self._get_icon("printer.svg"))
        email_button = QPushButton(" Email"); email_button.setObjectName("secondary_action_button")
        email_button.setIcon(self._get_icon("mail.svg"))
        final_actions_layout.addWidget(print_button); final_actions_layout.addWidget(email_button)

        layout.addWidget(customer_box)
        layout.addWidget(summary_box)
        layout.addWidget(payment_method_box)
        layout.addWidget(payment_details_box)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(process_payment_button)
        layout.addLayout(final_actions_layout)

        return container

    def _populate_sample_data(self, table: QTableWidget):
        sample_items = [
            {"name": "Coca Cola 600ml", "sku": "CC600", "qty": 2, "price": 3.50},
            {"name": "Pan Integral", "sku": "PI001", "qty": 1, "price": 2.25},
            {"name": "Leche Descremada 1L", "sku": "LD1000", "qty": 1, "price": 1.80},
        ]
        table.setRowCount(len(sample_items))

        for row, item in enumerate(sample_items):
            # Product and SKU widget
            product_widget = QWidget()
            product_layout = QVBoxLayout(product_widget)
            product_layout.setContentsMargins(0, 5, 0, 5)
            product_layout.setSpacing(0)
            product_layout.addWidget(QLabel(item["name"]))
            sku_label = QLabel(f"SKU: {item['sku']}")
            sku_label.setStyleSheet("color: #6c757d;")
            product_layout.addWidget(sku_label)
            table.setCellWidget(row, 0, product_widget)

            # Quantity widget
            qty_widget = QWidget()
            qty_layout = QHBoxLayout(qty_widget)
            qty_layout.setContentsMargins(0,0,0,0)
            minus_btn = QPushButton("-"); minus_btn.setFixedSize(25, 25)
            qty_label = QLabel(f"{item['qty']}"); qty_label.setAlignment(Qt.AlignCenter)
            plus_btn = QPushButton("+"); plus_btn.setFixedSize(25, 25)
            qty_layout.addWidget(minus_btn); qty_layout.addWidget(qty_label); qty_layout.addWidget(plus_btn)
            table.setCellWidget(row, 1, qty_widget)

            # Price item
            price_item = QTableWidgetItem(f"${item['price'] * item['qty']:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            table.setItem(row, 2, price_item)
            
            # Delete button
            delete_btn = QPushButton(); delete_btn.setIcon(self._get_icon("trash-2.svg"))
            delete_btn.setFixedSize(30, 30)
            delete_btn.setStyleSheet("border: none;")
            table.setCellWidget(row, 3, delete_btn)

            table.resizeRowToContents(row)