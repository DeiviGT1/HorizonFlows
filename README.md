# HorizonFlows POS

HorizonFlows is a robust and efficient desktop Point of Sale (POS) system, designed for the comprehensive management of businesses that buy and sell products, such as liquor stores, grocery stores, and more. Unlike web-based solutions, HorizonFlows is a native application built with **Python** and **PySide6**, ensuring optimal performance and a smooth user experience.

## 🚀 Key Features

This system is designed to be a complete and scalable solution.

- **Sales Management:** Quickly and efficiently record transactions. The system handles multiple payment methods, such as cash and card.
- **Inventory Management:** Full control over products, including stock, purchase and sale prices, and organization by categories.
- **Customer Management:** Maintain a customer database for more personalized service.
- **Authentication and User Roles:** A security system with different roles (cashier, manager, admin) to control access to various system functionalities.
- **Control Panel (Dashboard):** Visualize key business information to make better decisions.
- **Multitenant Support:** Designed with the ability to serve multiple "tenants" or branches from a single instance, ideal for franchises or chains.
- **PDF Report Generation:** Create professional sales, inventory, and other reports directly in PDF format.

## 🛠️ Tech Stack

The project is built with modern and reliable technologies focused on stability and scalability.

- **Backend and Application Logic:** Python
- **Graphical User Interface (GUI):** PySide6
- **Database:** PostgreSQL
- **ORM:** SQLModel, for a modern and simple interaction with the database.

## 🗂️ Project Structure and Data Models

The system's foundation lies in a set of well-structured data models that ensure data integrity and relationships.

```
HorizonFlows-desktop/
├── app/
│   ├── core/
│   │   └── database.py  # Database configuration and connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User, Shift Models
│   │   ├── product.py       # Product, Category Models
│   │   ├── sales.py         # Sale, Sale Line, Payment Models
│   │   ├── customer.py      # Customer Model
│   │   ├── inventory.py     # Purchase Order and Receipt Models
│   │   ├── finance.py       # Expense and Cash Drawer Activity Models
│   │   └── vendor.py        # Vendor Model
│   └── ...
└── main.py              # Application entry point
```

## 🏁 Getting Started

To get the system up and running, follow these steps.

### Prerequisites

- Python 3 installed.
- A running instance of PostgreSQL.
- Create a database in PostgreSQL (e.g., `pos_tienda`).

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [REPOSITORY-URL]
    cd HorizonFlows-desktop
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the database:**
    Make sure the connection details in the `app/core/database.py` file are correct.

### Execution

Once everything is set up, you can start the application. The system will automatically create the necessary tables in the database on the first run.

```bash
python main.py
```

When you run it, the main application window will open, ready to use.