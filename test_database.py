# test_database.py

from sqlmodel import Session, select
from app.core.database import engine, create_db_and_tables
from app.models.product import Product
# Si tu modelo de producto necesita un 'company_id', también necesitarás el modelo 'Business'.
# from app.models.business import Business 

def run_test():
    """
    Ejecuta una prueba simple para verificar la conexión a la base de datos
    y la creación de un objeto.
    """
    print("--- INICIANDO PRUEBA DE BASE DE DATOS ---")

    # Primero, asegúrate de que las tablas estén creadas.
    create_db_and_tables()

    # Inicia una nueva sesión con la base de datos
    with Session(engine) as session:
        print("\n[PASO 1: Creando un producto de prueba]")

        # (Opcional) Si la tabla 'Product' depende de 'Business',
        # primero necesitas crear una empresa.
        # test_business = Business(name="Tienda de Prueba")
        # session.add(test_business)
        # session.commit()
        # session.refresh(test_business)
        # print(f"Empresa de prueba creada con ID: {test_business.id}")

        # Crea una instancia de tu modelo Product
        test_product = Product(
            # company_id=test_business.id, # Si es necesario
            sku="TEST-001",
            name="Café de Prueba",
            type="good",
            unit_price=2.50,
            tax_rate=0.08
        )

        # Añade el producto a la sesión y guárdalo en la base de datos
        session.add(test_product)
        session.commit()
        session.refresh(test_product) # Refresca el objeto para obtener el ID asignado por la BD

        print(f"✅ Producto guardado con éxito. ID asignado: {test_product.id}")

        # --- Verificación ---
        print("\n[PASO 2: Verificando que el producto existe en la base de datos]")

        # Busca el producto que acabamos de crear
        product_in_db = session.get(Product, test_product.id)

        if product_in_db:
            print(f"✅ ¡ÉXITO! Se encontró el producto en la base de datos.")
            print(f"   -> Nombre: {product_in_db.name}")
            print(f"   -> Precio: ${product_in_db.unit_price}")
        else:
            print("❌ ¡FALLO! No se pudo encontrar el producto después de crearlo.")

    print("\n--- PRUEBA FINALIZADA ---")


if __name__ == "__main__":
    run_test()