# app/views/pages/terminal_view.py
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QFormLayout, QComboBox, QGroupBox,
    QFrame, QButtonGroup, QAbstractItemView, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QFont

class TerminalView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("terminal_page") 
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        left_panel = self._create_left_panel()
        right_panel = self._create_right_panel()

        content_layout.addWidget(left_panel, 7)
        content_layout.addWidget(right_panel, 3)

        main_layout.addLayout(content_layout, 1)

    def _get_icon(self, name):
        return QIcon(f"app/assets/icons/{name}")

    def _create_search_bar(self):
        # Este método se mantiene igual que en la versión anterior
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
        self.search_input.setPlaceholderText("Escanear o escribir código...")
        self.search_input.setObjectName("search_input")

        search_layout.addWidget(icon_label)
        search_layout.addWidget(self.search_input)
        
        return search_container

    def _create_left_panel(self):
        # Este método se mantiene igual
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
        self.order_items_table.setObjectName("order_items_table")
        self.order_items_table.setColumnCount(5)
        self.order_items_table.setHorizontalHeaderLabels(["Producto", "Cant.", "P. Unitario", "P. Total", ""])
        
        self.order_items_table.verticalHeader().setVisible(False)
        header = self.order_items_table.horizontalHeader()
        header.setObjectName("order_header")
        
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.order_items_table.setColumnWidth(4, 50)

        self.order_items_table.setShowGrid(False)
        self.order_items_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.order_items_table.setFocusPolicy(Qt.NoFocus)

        self._populate_sample_data(self.order_items_table)
        order_layout.addWidget(self.order_items_table)

        action_buttons_layout = QHBoxLayout()
        clear_button = QPushButton(" Limpiar Todo"); clear_button.setIcon(self._get_icon("trash-2.svg"))
        suspend_button = QPushButton(" Suspender")
        
        clear_button.setObjectName("dark_button")
        suspend_button.setObjectName("dark_button")

        action_buttons_layout.addStretch()
        action_buttons_layout.addWidget(clear_button)
        action_buttons_layout.addWidget(suspend_button)

        layout.addLayout(top_layout)
        layout.addWidget(order_box, 1)
        layout.addLayout(action_buttons_layout)
        return container

    def _create_right_panel(self):
        """
        CAMBIO: Se asigna un nombre de objeto a las etiquetas de subtítulos
        para poder aplicarles padding desde QSS.
        """
        # dentro de _create_right_panel(self)
        container = QGroupBox("Resumen de Orden")
        container.setObjectName("main_summary_panel")
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(20, 35, 20, 20)

        # --- Total de productos (caja grande) ---
        total_box = QWidget()
        total_box.setObjectName("total_products_box")
        total_lay = QVBoxLayout(total_box)
        total_lay.setContentsMargins(14, 12, 14, 12)

        ttl_caption = QLabel("Total de Productos")
        ttl_caption.setObjectName("summary_subtitle")

        ttl_value = QLabel("3 unidades")  
        ttl_value.setObjectName("summary_big")

        total_lay.addWidget(ttl_caption)
        total_lay.addWidget(ttl_value)
        main_layout.addWidget(total_box)

        # --- Línea a línea: Subtotal / IVA / Descuento ---
        def row(label, value, is_total=False):
            r = QHBoxLayout()
            l = QLabel(label); v = QLabel(value)
            l.setObjectName("summary_row_label")
            v.setObjectName("summary_row_value")
            if is_total:
                l.setObjectName("summary_total_label")
                v.setObjectName("summary_total_value")
            r.addWidget(l); r.addStretch(); r.addWidget(v)
            return r

        main_layout.addLayout(row("Subtotal:", "$82.50"))
        main_layout.addLayout(row("IVA (16%):", "$13.20"))
        main_layout.addLayout(row("Descuento:", "-$0.00"))
        main_layout.addSpacing(4)
        main_layout.addLayout(row("Total:", "$95.70", is_total=True))

        # --- Cliente ---
        client_caption = QLabel("Cliente")
        client_caption.setObjectName("summary_subtitle")
        client_combo = QComboBox()
        client_combo.setObjectName("client_combo")
        client_combo.addItems(["Cliente General"])
        main_layout.addSpacing(8)
        main_layout.addWidget(client_caption)
        main_layout.addWidget(client_combo)

        # --- Método de pago (toggle buttons) ---
        pay_caption = QLabel("Método de Pago")
        pay_caption.setObjectName("summary_subtitle")
        main_layout.addSpacing(6)
        main_layout.addWidget(pay_caption)

        pay_row = QHBoxLayout()
        cash_btn = QPushButton("Efectivo")
        cash_btn.setIcon(self._get_icon("dollar-sign.svg"))
        card_btn = QPushButton("Tarjeta")
        card_btn.setIcon(self._get_icon("credit-card.svg"))
        other_btn = QPushButton("Otro")
        other_btn.setIcon(self._get_icon("credit-card.svg"))
        for b in (cash_btn, card_btn, other_btn):
            b.setCheckable(True)
            b.setObjectName("pay_method_btn")
            b.setMinimumHeight(44)
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        pay_group = QButtonGroup(self)
        pay_group.setExclusive(True)
        pay_group.addButton(cash_btn)
        pay_group.addButton(card_btn)
        pay_group.addButton(other_btn)
        cash_btn.setChecked(True)

        pay_row.addWidget(cash_btn)
        pay_row.addWidget(card_btn)
        pay_row.addWidget(other_btn)
        main_layout.addLayout(pay_row)

        # --- Recibido / Cambio ---
        recv_caption = QLabel("Recibido")
        recv_caption.setObjectName("summary_subtitle")
        recv_input = QLineEdit("100.00")
        recv_input.setObjectName("money_input")
        recv_input.setFixedHeight(40)

        change_caption = QLabel("Cambio a devolver:")
        change_caption.setObjectName("summary_subtitle")
        change_value = QLabel("$4.30")
        change_value.setObjectName("change_value")

        main_layout.addSpacing(8)
        main_layout.addWidget(recv_caption)
        main_layout.addWidget(recv_input)
        main_layout.addSpacing(4)
        main_layout.addWidget(change_caption)
        main_layout.addWidget(change_value)

        # --- Botón primario ---
        pay_btn = QPushButton("  Procesar Pago")
        pay_btn.setObjectName("primary_button")
        pay_btn.setMinimumHeight(46)
        pay_btn.setIcon(QIcon("app/assets/icons/check.svg"))
        main_layout.addSpacing(8)
        main_layout.addWidget(pay_btn)

        return container

    def _populate_sample_data(self, table: QTableWidget):
        # Este método se mantiene igual
        sample_items = [
            {"name": "Coca Cola 500ml Sin Azúcar", "sku": "CC500SA", "qty": 2, "price": 25.00},
            {"name": "Pan Bimbo Blanco Integral Grande", "sku": "PB001", "qty": 1, "price": 32.50},
        ]
        table.setRowCount(len(sample_items))

        for row, item in enumerate(sample_items):
            product_widget = QWidget()
            product_widget.setObjectName("order_cell_container")
            product_layout = QVBoxLayout(product_widget); product_layout.setContentsMargins(10, 8, 10, 8); product_layout.setSpacing(2)
            product_name_label = QLabel(item["name"]); product_name_label.setObjectName("product_name_label")
            sku_label = QLabel(f"SKU: {item['sku']}"); sku_label.setObjectName("sku_label")
            product_layout.addWidget(product_name_label); product_layout.addWidget(sku_label)
            table.setCellWidget(row, 0, product_widget)

            qty_input = QLineEdit(str(item['qty'])); qty_input.setObjectName("quantity_input"); qty_input.setAlignment(Qt.AlignCenter); qty_input.setFixedSize(50, 32)
            qty_container = QWidget()
            qty_container.setObjectName("order_cell_container")
            qty_layout = QHBoxLayout(qty_container)
            qty_layout.setContentsMargins(0,0,0,0)
            qty_layout.setAlignment(Qt.AlignCenter)
            qty_layout.addWidget(qty_input)
            table.setCellWidget(row, 1, qty_container)

            unit_price_item = QTableWidgetItem(f"${item['price']:.2f}"); unit_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter); unit_price_item.setFlags(unit_price_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 2, unit_price_item)

            total_price = item['price'] * item['qty']
            total_price_item = QTableWidgetItem(f"${total_price:.2f}"); total_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            font = total_price_item.font(); font.setBold(True); total_price_item.setFont(font); total_price_item.setFlags(total_price_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 3, total_price_item)
            
            delete_btn_container = QWidget()
            delete_btn_container.setObjectName("order_cell_container")
            delete_btn_layout = QHBoxLayout(delete_btn_container)
            delete_btn_layout.setContentsMargins(0,0,0,0)
            delete_btn_layout.setAlignment(Qt.AlignCenter)
            delete_btn = QPushButton(); delete_btn.setIcon(self._get_icon("trash-2.svg")); delete_btn.setObjectName("delete_button"); delete_btn.setFixedSize(32, 32)
            delete_btn_layout.addWidget(delete_btn)
            table.setCellWidget(row, 4, delete_btn_container)

            table.setRowHeight(row, 60)