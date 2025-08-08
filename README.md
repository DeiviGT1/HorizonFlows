# HorizonFlows POS

HorizonFlows es un sistema de Punto de Venta (POS) de escritorio, robusto y eficiente, diseñado para la gestión integral de negocios de compra y venta de productos, como licorerías, tiendas de abarrotes y más. A diferencia de las soluciones web, HorizonFlows es una aplicación nativa construida con **Python** y **PySide6**, lo que garantiza un rendimiento óptimo y una experiencia de usuario fluida.

## 🚀 Características Principales

Este sistema está diseñado para ser una solución completa y escalable.

- **Gestión de Ventas:** Registra transacciones de forma rápida y eficiente. El sistema maneja múltiples métodos de pago, como efectivo y tarjeta.
- **Gestión de Inventario:** Control total sobre los productos, incluyendo stock, precios de compra y venta, y organización por categorías.
- **Gestión de Clientes:** Mantén una base de datos de tus clientes para un servicio más personalizado.
- **Autenticación y Roles de Usuario:** Sistema de seguridad con diferentes roles (cajero, gerente, administrador) para controlar el acceso a las distintas funcionalidades del sistema.
- **Panel de Control (Dashboard):** Visualiza información clave de tu negocio para tomar mejores decisiones.
- **Soporte Multitenant:** Diseñado con la capacidad de dar servicio a múltiples "inquilinos" o sucursales desde una sola instancia, ideal para franquicias o cadenas.
- **Generación de Reportes en PDF:** Crea reportes profesionales de ventas, inventario y más, directamente en formato PDF.

## 🛠️ Stack Tecnológico

El proyecto está construido con tecnologías modernas y confiables, enfocadas en la estabilidad y la escalabilidad.

- **Backend y Lógica de Aplicación:** Python
- **Interfaz Gráfica de Usuario (GUI):** PySide6
- **Base de Datos:** PostgreSQL
- **ORM:** SQLModel, para una interacción moderna y sencilla con la base de datos.

## 🗂️ Estructura del Proyecto y Modelos de Datos

La base del sistema reside en un conjunto de modelos de datos bien estructurados que aseguran la integridad y la relación de la información.

```
HorizonFlows-desktop/
├── app/
│   ├── core/
│   │   └── database.py  # Configuración y conexión con la base de datos
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # Modelos de Usuario, Turno
│   │   ├── product.py       # Modelos de Producto, Categoría
│   │   ├── sales.py         # Modelos de Venta, Línea de Venta, Pago
│   │   ├── customer.py      # Modelo de Cliente
│   │   ├── inventory.py     # Modelos de Órdenes de Compra y Recepciones
│   │   ├── finance.py       # Modelos de Gastos y Actividad de Caja
│   │   └── vendor.py        # Modelo de Proveedor
│   └── ...
└── main.py              # Punto de entrada de la aplicación
```

## 🏁 Cómo Empezar

Para poner en marcha el sistema, sigue estos pasos.

### Prerrequisitos

- Tener instalado Python 3.
- Tener una instancia de PostgreSQL en ejecución.
- Crear una base de datos en PostgreSQL (por ejemplo, `pos_tienda`).

### Instalación

1.  **Clona el repositorio:**

    ```bash
    git clone [URL-DEL-REPOSITORIO]
    cd HorizonFlows-desktop
    ```

2.  **Crea y activa un entorno virtual:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    ```

3.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura la base de datos:**
    Asegúrate de que los datos de conexión en el archivo `app/core/database.py` sean correctos.

### Ejecución

Una vez configurado todo, puedes iniciar la aplicación. El sistema creará automáticamente las tablas necesarias en la base de datos la primera vez que se ejecute.

```bash
python main.py
```

Al ejecutarlo, se abrirá la ventana principal de la aplicación, lista para usarse.
