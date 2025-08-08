# app/views/terminal_view.py
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QFormLayout, QComboBox, QGroupBox,
    QSpacerItem, QSizePolicy, QAbstractItemView, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont

class TerminalView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        left_panel = self._create_left_panel()
        right_panel = self._create_right_panel()

        main_layout.addWidget(left_panel, 7)
        main_layout.addWidget(right_panel, 3)

    def _get_icon(self, name):
        return QIcon(f"app/icons/{name}")

    def _create_search_bar(self):
        search_container = QWidget()
        search_container.setObjectName("search_container")
        search_container.setFixedHeight(48)
        
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 0, 5, 0)
        search_layout.setSpacing(10)

        icon_label = QLabel()
        try:
            pixmap = QPixmap("app/icons/search.svg")
            icon_label.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except:
            pass 

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

        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(4)
        self.order_items_table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio", ""])
        self.order_items_table.verticalHeader().setVisible(False)
        self.order_items_table.horizontalHeader().setVisible(False)
        
        header = self.order_items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        
        self.order_items_table.setColumnWidth(1, 70)
        self.order_items_table.setColumnWidth(3, 60)

        self.order_items_table.setShowGrid(False)
        self.order_items_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.order_items_table.setFocusPolicy(Qt.NoFocus)

        self._populate_sample_data(self.order_items_table)
        order_layout.addWidget(self.order_items_table)

        action_buttons_layout = QHBoxLayout()
        clear_button = QPushButton(" Limpiar Todo"); clear_button.setIcon(self._get_icon("trash-2.svg"))
        suspend_button = QPushButton(" Suspender")
        clear_button.setObjectName("bottom_action_button")
        suspend_button.setObjectName("bottom_action_button")

        action_buttons_layout.addWidget(clear_button)
        action_buttons_layout.addWidget(suspend_button)

        layout.addLayout(top_layout)
        layout.addWidget(order_box, 1)
        layout.addLayout(action_buttons_layout)
        return container

    def _create_right_panel(self):
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

        summary_box = QGroupBox("Resumen de Orden")
        summary_layout = QFormLayout(summary_box)
        summary_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        summary_layout.setVerticalSpacing(12)
        summary_layout.setHorizontalSpacing(20)

        subtotal_label = QLabel("Subtotal:"); subtotal_label.setObjectName("summary_label")
        subtotal_value = QLabel("$7.55"); subtotal_value.setObjectName("summary_value"); subtotal_value.setAlignment(Qt.AlignRight)
        taxes_label = QLabel("Impuestos (16%):"); taxes_label.setObjectName("summary_label")
        taxes_value = QLabel("$1.21"); taxes_value.setObjectName("summary_value"); taxes_value.setAlignment(Qt.AlignRight)
        discount_label = QLabel("Descuento:"); discount_label.setObjectName("summary_label")
        discount_value = QLabel("-$0.00"); discount_value.setObjectName("summary_value"); discount_value.setAlignment(Qt.AlignRight)
        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setObjectName("summary_line")
        total_label = QLabel("Total:"); total_label.setObjectName("total_label")
        total_value = QLabel("$8.76"); total_value.setObjectName("total_value"); total_value.setAlignment(Qt.AlignRight)

        summary_layout.addRow(subtotal_label, subtotal_value)
        summary_layout.addRow(taxes_label, taxes_value)
        summary_layout.addRow(discount_label, discount_value)
        summary_layout.addRow(line)
        summary_layout.addRow(total_label, total_value)

        payment_method_box = QGroupBox("Método de Pago")
        payment_method_layout = QHBoxLayout(payment_method_box)
        cash_button = QPushButton(" Efectivo"); cash_button.setObjectName("payment_method_button"); cash_button.setIcon(self._get_icon("dollar-sign.svg")); cash_button.setCheckable(True); cash_button.setChecked(True)
        card_button = QPushButton(" Tarjeta"); card_button.setObjectName("payment_method_button"); card_button.setIcon(self._get_icon("credit-card.svg")); card_button.setCheckable(True)
        self.payment_method_group = QButtonGroup(self); self.payment_method_group.addButton(cash_button); self.payment_method_group.addButton(card_button); self.payment_method_group.setExclusive(True)
        payment_method_layout.addWidget(cash_button); payment_method_layout.addWidget(card_button)

        payment_details_layout = QFormLayout(); payment_details_layout.setContentsMargins(0, 5, 0, 5)
        received_amount_input = QLineEdit("$8.76"); received_amount_input.setFixedHeight(48)
        change_label = QLabel("$0.00"); change_label.setAlignment(Qt.AlignRight)
        payment_details_layout.addRow(QLabel("Monto Recibido:"), received_amount_input)
        payment_details_layout.addRow(QLabel("Cambio:"), change_label)

        process_payment_button = QPushButton("Procesar Pago"); process_payment_button.setObjectName("process_payment_button"); process_payment_button.setFixedHeight(50)

        final_actions_layout = QHBoxLayout(); final_actions_layout.setSpacing(15)
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

    def _populate_sample_data(self, table: QTableWidget):
        sample_items = [
            {"name": "Coca Cola 600ml", "sku": "CC600", "qty": 2, "price": 1.75},
            {"name": "Pan Integral", "sku": "PI001", "qty": 1, "price": 2.25},
            {"name": "Leche Descremada 1L", "sku": "LD1000", "qty": 1, "price": 1.80},
        ]
        table.setRowCount(len(sample_items))

        for row, item in enumerate(sample_items):
            product_widget = QWidget()
            product_layout = QVBoxLayout(product_widget)
            product_layout.setContentsMargins(10, 8, 10, 8); product_layout.setSpacing(2)
            product_name_label = QLabel(item["name"]); product_name_label.setObjectName("product_name_label")
            sku_label = QLabel(f"SKU: {item['sku']}"); sku_label.setObjectName("sku_label")
            product_layout.addWidget(product_name_label); product_layout.addWidget(sku_label)
            table.setCellWidget(row, 0, product_widget)

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

            total_price = item['price'] * item['qty']
            price_item = QTableWidgetItem(f"${total_price:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            font = price_item.font(); font.setBold(True); price_item.setFont(font)
            
            # ▼▼▼ ¡AQUÍ ESTÁ LA LÍNEA CLAVE! ▼▼▼
            # Hacemos que la celda no sea editable.
            price_item.setFlags(price_item.flags() & ~Qt.ItemIsEditable)
            
            table.setItem(row, 2, price_item)
            
            delete_btn_container = QWidget()
            delete_btn_layout = QHBoxLayout(delete_btn_container)
            delete_btn_layout.setContentsMargins(0,0,0,0); delete_btn_layout.setAlignment(Qt.AlignCenter)
            delete_btn = QPushButton(); delete_btn.setIcon(self._get_icon("trash-2.svg")); delete_btn.setObjectName("delete_button"); delete_btn.setFixedSize(32, 32)
            delete_btn_layout.addWidget(delete_btn)
            table.setCellWidget(row, 3, delete_btn_container)

            table.setRowHeight(row, 60)