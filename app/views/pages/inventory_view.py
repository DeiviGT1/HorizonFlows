from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap


class InventoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("inventory_page")

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(16)

        # === Header ===
        header = QHBoxLayout()
        title = QLabel("Inventario")
        title.setObjectName("inv_title")

        add_btn = QPushButton("+ Añadir Producto")
        add_btn.setObjectName("inv_primary_button")
        add_btn.setMinimumHeight(40)
        add_btn.setIcon(self._icon("plus.svg"))
        add_btn.setIconSize(QSize(18, 18))

        header.addWidget(title)
        header.addStretch()
        header.addWidget(add_btn)
        root.addLayout(header)

        # === Panel de Filtros ===
        filters_box = QGroupBox()
        filters_box.setObjectName("inventory_filters_box")
        filters_col = QVBoxLayout(filters_box)
        filters_col.setContentsMargins(16, 16, 16, 16)
        filters_col.setSpacing(12)

        # Fila de controles (buscador + combos)
        controls = QHBoxLayout()
        controls.setSpacing(12)

        # --- Buscador ---
        search_box = QWidget()
        search_lay = QVBoxLayout(search_box)
        search_lay.setContentsMargins(0, 0, 0, 0)
        search_lay.setSpacing(6)

        search_label = QLabel("Nombre o Código")
        search_label.setObjectName("inv_field_label")  # mismo estilo que los demás
        search_lay.addWidget(search_label)

        search_wrap = QWidget()
        search_wrap.setObjectName("inv_search_container")
        search_wrap.setFixedHeight(48)
        swl = QHBoxLayout(search_wrap)
        swl.setContentsMargins(12, 0, 12, 0)
        swl.setSpacing(8)

        search_icon = QLabel()
        search_icon.setPixmap(self._pix("search.svg", 18))
        self.search_input = QLineEdit()
        self.search_input.setObjectName("inv_search_input")
        self.search_input.setPlaceholderText("Buscar por nombre o código...")

        swl.addWidget(search_icon)
        swl.addWidget(self.search_input)

        search_lay.addWidget(search_wrap)


        # Categoría
        cat_box = self._labeled_combo("Categoría", ["Todas las categorías", "Electrónicos", "Ropa", "Hogar", "Deportes"])
        self.category_combo = cat_box.findChild(QComboBox)

        # Estado de stock
        stock_box = self._labeled_combo("Estado de Stock", ["Todos los estados", "Con stock", "Bajo", "Sin stock"])
        self.stock_combo = stock_box.findChild(QComboBox)

        controls.addWidget(search_box, 2)
        controls.addWidget(cat_box, 1)
        controls.addWidget(stock_box, 1)
        filters_col.addLayout(controls)

        root.addWidget(filters_box)

        # === Botones Importar / Exportar (debajo del panel de filtros) ===
        actions_row = QHBoxLayout()
        actions_row.addStretch()
        self.import_btn = QPushButton("  Importar")
        self.import_btn.setObjectName("inv_secondary_button")
        self.import_btn.setIcon(self._icon("download.svg"))
        self.export_btn = QPushButton("  Exportar")
        self.export_btn.setObjectName("inv_secondary_button")
        self.export_btn.setIcon(self._icon("upload.svg"))
        for b in (self.import_btn, self.export_btn):
            b.setMinimumHeight(40)
        actions_row.addWidget(self.import_btn)
        actions_row.addWidget(self.export_btn)
        root.addLayout(actions_row)

        # === Tabla ===
        table_box = QGroupBox("Productos en Inventario")
        table_box.setObjectName("inventory_table_box")
        tbl_layout = QVBoxLayout(table_box)
        tbl_layout.setContentsMargins(16, 12, 16, 12)
        tbl_layout.setSpacing(12)

        head_line = QHBoxLayout()
        head_line.addStretch()
        self.count_label = QLabel("247 productos encontrados")
        self.count_label.setObjectName("inv_count_label")
        head_line.addWidget(self.count_label)
        tbl_layout.addLayout(head_line)

        self.table = QTableWidget(0, 8)
        self.table.setObjectName("inventory_table")
        self.table.setHorizontalHeaderLabels([
            "", "Imagen", "Nombre del Producto", "SKU", "Categoría", "Stock Actual", "Precio de Venta", "Acciones"
        ])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setVisible(False)

        hdr = self.table.horizontalHeader()
        hdr.setStretchLastSection(False)
        hdr.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hdr.setSectionResizeMode(0, QHeaderView.Fixed)          # checkbox
        hdr.setSectionResizeMode(1, QHeaderView.Fixed)          # imagen
        hdr.setSectionResizeMode(2, QHeaderView.Stretch)        # nombre
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(7, QHeaderView.Fixed)          # acciones

        # ANCHOS QUE MATCHEAN EL MOCKUP
        self.table.setColumnWidth(0, 40)    # checkbox
        self.table.setColumnWidth(1, 72)    # imagen + padding
        self.table.setColumnWidth(7, 92)    # acciones (2 íconos)

        tbl_layout.addWidget(self.table)
        root.addWidget(table_box, 1)

        # === Paginación ===
        bottom_bar = QHBoxLayout()
        self.results_hint = QLabel("Mostrando 1 a 10 de 247 resultados")
        self.results_hint.setObjectName("inv_results_hint")

        bottom_bar.addWidget(self.results_hint)
        bottom_bar.addStretch()

        self.page_prev = self._page_btn("‹")
        self.page_1 = self._page_btn("1", current=True)
        self.page_2 = self._page_btn("2")
        self.page_3 = self._page_btn("3")
        self.page_last = self._page_btn("…")
        self.page_next = self._page_btn("›")

        for b in (self.page_prev, self.page_1, self.page_2, self.page_3, self.page_last, self.page_next):
            bottom_bar.addWidget(b)

        root.addLayout(bottom_bar)

        # Data de ejemplo
        self._populate_sample()

    # ---- Helpers ----
    def _labeled_combo(self, label_text: str, items: list[str]) -> QWidget:
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        lbl = QLabel(label_text)
        lbl.setObjectName("inv_field_label")
        combo = QComboBox()
        combo.setFixedHeight(48)
        combo.addItems(items)
        lay.addWidget(lbl)
        lay.addWidget(combo)
        return box

    def _page_btn(self, text: str, current: bool = False) -> QPushButton:
        b = QPushButton(text)
        b.setObjectName("page_button_current" if current else "page_button")
        b.setMinimumHeight(32)
        b.setMinimumWidth(36)
        return b

    def _icon(self, name: str) -> QIcon:
        return QIcon(f"app/assets/icons/{name}")

    def _pix(self, name: str, size: int) -> QPixmap:
        pm = QPixmap(f"app/assets/icons/{name}")
        return pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def _populate_sample(self):
        sample = [
            ("Smartphone Samsung Galaxy A54", "SM-A545F", "Electrónicos", 25, 299.99),
            ("Camiseta Nike Dri-FIT", "NK-DF001", "Ropa", 5, 29.99),
            ("Cafetera Espresso Delonghi", "DL-ESP200", "Hogar", 0, 159.99),
            ("Balón de Fútbol Adidas", "AD-FB500", "Deportes", 15, 39.99),
            ("Auriculares Sony WH-1000XM4", "SN-WH1000", "Electrónicos", 3, 349.99),
        ]
        self.table.setRowCount(len(sample))
        for r, (name, sku, cat, stock, price) in enumerate(sample):
            # Col 0: checkbox (perfectly centered)
            cb = QCheckBox()
            cb.setText("")  # avoid extra width from label spacing
            cb.setTristate(False)
            cb.setObjectName("inv_row_checkbox")
            cb.setStyleSheet("margin:0px; padding:0px;")

            cb_container = QWidget()
            cb_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            cb_container.setStyleSheet("background: transparent;")
            cb_container.setAttribute(Qt.WA_TranslucentBackground)

            cb_layout = QHBoxLayout(cb_container)
            cb_layout.setContentsMargins(0, 0, 0, 0)

            # Center using per-widget alignment + stretches (most reliable across platforms)
            cb_layout.addStretch()
            cb_layout.addWidget(cb, 0, Qt.AlignCenter)
            cb_layout.addStretch()

            self.table.setCellWidget(r, 0, cb_container)

            # Col 1: imagen 40x28 centrada, con fondo pill
            img_wrap = QWidget()
            hl = QHBoxLayout(img_wrap)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setAlignment(Qt.AlignCenter)
            img = QLabel("IMG")
            img.setObjectName("inv_img_placeholder")
            img.setFixedSize(40, 28)
            img.setAlignment(Qt.AlignCenter)
            hl.addWidget(img)
            self.table.setCellWidget(r, 1, img_wrap)

            # Col 2: nombre (permite 2 líneas)
            name_lbl = QLabel(name)
            name_lbl.setObjectName("inv_name_cell")
            name_lbl.setWordWrap(True)
            self.table.setCellWidget(r, 2, name_lbl)

            # Col 3: SKU
            sku_item = QTableWidgetItem(sku)
            sku_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(r, 3, sku_item)

            # Col 4: categoría
            cat_item = QTableWidgetItem(cat)
            cat_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(r, 4, cat_item)

            # Col 5: stock (badge)
            stock_lbl = QLabel(f"{stock} unidades")
            stock_lbl.setObjectName("inv_stock_badge")
            stock_wrap = QWidget()
            stock_wrap.setObjectName("inv_stock_wrap")  # <-- nuevo objectName
            swl = QHBoxLayout(stock_wrap)
            swl.setContentsMargins(0, 0, 0, 0)
            swl.setAlignment(Qt.AlignCenter)
            swl.addWidget(stock_lbl)
            self.table.setCellWidget(r, 5, stock_wrap)

            # Col 6: precio
            price_item = QTableWidgetItem(f"${price:,.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            f = price_item.font(); f.setBold(True); price_item.setFont(f)
            self.table.setItem(r, 6, price_item)

            # Col 7: acciones
            act_wrap = QWidget()
            act_wrap.setObjectName("inv_actions_wrap")  # <-- nuevo objectName
            al = QHBoxLayout(act_wrap)
            al.setContentsMargins(0, 0, 0, 0)
            al.setSpacing(6)
            al.setAlignment(Qt.AlignCenter)

            edit_btn = QPushButton()
            edit_btn.setObjectName("inv_row_icon_button")
            edit_btn.setIcon(self._icon("edit-2.svg"))
            edit_btn.setToolTip("Editar")

            del_btn = QPushButton()
            del_btn.setObjectName("inv_row_icon_button")
            del_btn.setIcon(self._icon("trash-2.svg"))
            del_btn.setToolTip("Eliminar")

            for b in (edit_btn, del_btn):
                b.setCursor(Qt.PointingHandCursor)
                b.setFixedSize(28, 28)

            al.addWidget(edit_btn)
            al.addWidget(del_btn)
            self.table.setCellWidget(r, 7, act_wrap)

            # Altura de fila como en el mockup
            self.table.setRowHeight(r, 64)
