# main.py
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.core.database import create_db_and_tables
from app.views.main_window import MainWindow

# OJO: main.py está en la raíz. Los estilos están en app/assets/styles
STYLES_DIR = (Path(__file__).resolve().parent / "app" / "assets" / "styles")

def load_styles(app: QApplication) -> None:
    chunks = []

    def read(path: Path):
        try:
            return path.read_text(encoding="utf-8")
        except Exception:
            return ""

    # 1) base global
    base = STYLES_DIR / "base.qss"
    if base.exists():
        chunks.append(read(base))

    # 2) components (opcionales, todos)
    comp_dir = STYLES_DIR / "components"
    if comp_dir.exists():
        for p in sorted(comp_dir.glob("*.qss")):
            chunks.append(read(p))

    # 3) pages (todos; se auto-encapsulan por objectName)
    pages_dir = STYLES_DIR / "pages"
    if pages_dir.exists():
        for p in sorted(pages_dir.glob("*.qss")):
            chunks.append(read(p))

    app.setStyleSheet("\n\n".join(chunks))

def main() -> int:
    create_db_and_tables()
    app = QApplication(sys.argv)
    app.setOrganizationName("HorizonFlows")
    app.setApplicationName("HorizonFlows POS")

    try:
        load_styles(app)
    except Exception as e:
        print(f"[WARN] Estilos no cargados: {e}")

    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
