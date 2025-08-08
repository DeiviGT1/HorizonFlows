# main.py
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.core.database import create_db_and_tables
from app.views.main_window import MainWindow

STYLES_DIR = Path(__file__).resolve().parent / "assets" / "styles"

def load_styles(app: QApplication) -> None:
    """Carga todos los .qss del directorio en orden predecible."""
    qss_chunks = []
    # Orden recomendado: base primero, luego páginas
    for name in ("base.qss", "terminal.qss"):
        qss_path = STYLES_DIR / name
        if qss_path.exists():
            qss_chunks.append(qss_path.read_text(encoding="utf-8"))
    # Si quieres cargar cualquier otro .qss adicional que haya en la carpeta:
    for extra in sorted(STYLES_DIR.glob("*.qss")):
        if extra.name not in {"base.qss", "terminal.qss"}:
            qss_chunks.append(extra.read_text(encoding="utf-8"))
    app.setStyleSheet("\n\n".join(qss_chunks))

def main() -> int:
    # 1) DB
    create_db_and_tables()

    # 2) Qt App
    app = QApplication(sys.argv)
    app.setOrganizationName("HorizonFlows")
    app.setApplicationName("HorizonFlows POS")

    # 3) Estilos
    try:
        load_styles(app)
    except Exception as e:
        # No tumbes la app por estilos
        print(f"[WARN] No se pudieron cargar estilos: {e}")

    # 4) Ventana principal
    window = MainWindow()
    window.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
