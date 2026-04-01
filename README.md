# ☕ DotDotDot App — Café Management System
> Capstone Module 1 — Python + MySQL Terminal Application

![Python](https://img.shields.io/badge/Python-3.x-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

---

## 📌 Overview

DotDotDot App is a **role-based café management terminal application** built with Python and MySQL. The app is designed to manage daily café operations including sales reporting, data analytics, menu management, and order tracking.

This project was built as part of the Purwadhika Bootcamp Capstone Module 1. While the core admin features are fully functional and cover all capstone requirements, the app is intentionally designed to be **scalable and extendable** for future development.

---

## 👥 Role System

The app supports 3 roles, each with their own panel and features:

| Role | Description |
|---|---|
| `admin` | Full access — sales reports, statistics, charts, menu management |
| `store_manager` | Stock management (in development) |
| `customer` | View menu, place orders, view order history (in development) |

---

## ✅ Features

### 🔐 Authentication
- Login with username & password
- Role-based routing to the correct panel
- Create new customer account with duplicate username check

### 📊 Admin Panel — Feature 1: View Sales Report
- View all transactions in a formatted table
- Filter by date range
- Filter by menu item
- Filter by customer

### 📈 Admin Panel — Feature 2: Sales Statistics
- Data preview (first 10 rows) using `pd.read_sql()`
- Calculate average of any numeric column (user selects)
- All time statistics — total revenue, avg order value, best seller, revenue per menu, revenue per payment method
- Statistics filtered by custom date range

### 📉 Admin Panel — Feature 3: Sales Chart
- Interactive dashboard built with `matplotlib` and `gridspec`
- 4 summary cards (total transactions, total revenue, avg order value, best seller)
- Bar chart — revenue per menu item
- Pie chart — revenue by payment method
- Line chart — revenue over time
- Histogram — order value distribution
- Supports all time and custom date range views

### 🍽️ Admin Panel — Feature 4: Manage Menu
- View current menu table
- Add new menu item
- Edit menu price (by ID — safe, no index shifting)
- Delete menu item (by ID — with confirmation warning)

---

## 🗄️ Database Structure

Database name: `dotdotdot_app`

### `accounts`
| Column | Type | Description |
|---|---|---|
| id_account | INT, AUTO_INCREMENT, PK | Unique account ID |
| username | VARCHAR(50) | Login username |
| password | VARCHAR(50) | Login password |
| role | VARCHAR(20) | admin / store_manager / customer |

### `menu`
| Column | Type | Description |
|---|---|---|
| id_menu | INT, AUTO_INCREMENT, PK | Unique menu ID |
| name | VARCHAR(100) | Menu name |
| category | VARCHAR(50) | e.g. coffee, matcha |
| size | VARCHAR(20) | e.g. 250ml, 500ml, 1000ml |
| price | DECIMAL(10,2) | Price in IDR |

### `stock`
| Column | Type | Description |
|---|---|---|
| id_stock | INT, AUTO_INCREMENT, PK | Unique stock ID |
| id_menu | INT | References menu item |
| quantity | INT | Current stock quantity |

> ⚠️ `stock` intentionally has no FOREIGN KEY to `menu` — this allows admin to delete menu items without needing to zero out stock first.

### `transactions`
| Column | Type | Description |
|---|---|---|
| id_transaction | INT, AUTO_INCREMENT, PK | Unique transaction ID |
| id_account | INT | Customer who ordered |
| id_menu | INT | Menu item ordered |
| quantity | INT | Quantity ordered |
| total_price | DECIMAL(10,2) | Total price |
| payment_method | VARCHAR(50) | cash / transfer |
| date | DATETIME | Transaction timestamp |

---

## 📸 Screenshots

> _Add screenshots of your terminal output and chart dashboard here_

```
Example:
- Admin Panel menu
- Sales Report table
- Statistics output
- Sales Dashboard chart
```

---

## 🚀 Future Development

This app is built with scalability in mind. The following features are planned for future versions:

### Store Manager Panel
- [ ] View current stock levels
- [ ] Update stock quantity
- [ ] Stock statistics and low stock alerts

### Customer Panel
- [ ] Browse menu with prices
- [ ] Place orders directly from terminal
- [ ] View personal order history

### Admin Panel
- [ ] Remove customer accounts
- [ ] Edit menu item name and category (currently only price)
- [ ] Export sales report to CSV

### General
- [ ] Password hashing for security
- [ ] Input validation improvements
- [ ] Pagination for large tables

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python 3.x | Core application language |
| MySQL 8.x | Database |
| mysql-connector-python | Database connection |
| pandas | Data manipulation and analysis |
| matplotlib | Data visualization (charts & dashboard) |
| tabulate | Terminal table formatting |
| os / sys | Screen clearing and app exit |

---

## ⚙️ How to Run

1. Import the database:
```bash
mysql -u root -p < dotdotdot_app.sql
```

2. Install required libraries:
```bash
pip install mysql-connector-python pandas matplotlib tabulate
```

3. Run the app:
```bash
python main.py
```

4. Login with default admin account:
```
Username : admin
Password : admin123
```

---

## 👨‍💻 Author

**Alghi** — Purwadhika Bootcamp, Capstone Module 1

> _"This app is a work in progress — but every feature that exists works correctly and is built to be extended."_
