import function as fn
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ──────────────────────────
# Main menu for admin
# ──────────────────────────
def admin_menu(user):
    while True:
        fn.print_header()
        print(f'''
        ╔══════════════════════════════════════╗
        ║             ADMIN PANEL              ║
        ║  Logged in as: {user['username']:^22}║
        ╠══════════════════════════════════════╣
        ║  [1] View Sales Report               ║
        ║  [2] Show Sales Statistics           ║
        ║  [3] Show Sales Chart                ║
        ║  [4] Manage Menu (Add/Edit/Delete)   ║
        ║  [5] Remove Customer Account         ║
        ║  [0] Logout                          ║
        ║  [999] Exit Application              ║
        ╚══════════════════════════════════════╝''')

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            fn.clearscreen()
            admin_view_sales()
        elif choice == "2":
            fn.clearscreen()
            admin_show_statistics()
        elif choice == "3":
            fn.clearscreen()
            admin_show_chart()
        elif choice == "4":
            fn.clearscreen()
            admin_manage_menu()
        elif choice == "5":
            fn.clearscreen()
            admin_remove_customer()
        elif choice == "0":
            print("Logging out...")
            fn.clearscreen()
            break
        elif choice == "999":
            fn.exit_app()
        else:
            print("\n[!] Invalid choice. Please enter a valid option.")
        fn.clearscreen()


# ──────────────────────────────────────────────
# FEATURE 1 - VIEW SALES REPORT
# ──────────────────────────────────────────────
def admin_view_sales():
    while True:
        fn.print_header()
        print('''
        ╔══════════════════════════════════════╗
        ║          VIEW SALES REPORT           ║
        ╠══════════════════════════════════════╣
        ║  [1] Show all transactions           ║
        ║  [2] Filter by date range            ║
        ║  [3] Filter by menu item             ║
        ║  [4] Filter by customer              ║
        ║  [0] Back                            ║
        ║  [999] Exit Application              ║
        ╚══════════════════════════════════════╝''')
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            fn.clearscreen()
            show_sales_table()
            input("\nPress Enter to go back...")
        elif choice == "2":
            fn.clearscreen()
            filter_by_date()
            input("\nPress Enter to go back...")
        elif choice == "3":
            fn.clearscreen()
            filter_by_menu()
            input("\nPress Enter to go back...")
        elif choice == "4":
            fn.clearscreen()
            filter_by_customer()
            input("\nPress Enter to go back...")
        elif choice == "0":
            fn.clearscreen()
            break
        elif choice == "999":
            fn.exit_app()
        else:
            print("\n[!] Invalid choice. Please try again.")
        fn.clearscreen()

# ──────────────────────────────────────────────
# [1.1] Function to display sales data in a table format
# ──────────────────────────────────────────────

def show_sales_table(query=None, params=None):
    """Fetch and display transactions as a table."""
    mydb = fn.conn_sql()
    cursor = mydb.cursor()

    base_query = """
        SELECT 
            t.id_transaction,
            a.username,
            m.name,
            m.size,
            t.quantity,
            t.total_price,
            t.payment_method,
            t.date
        FROM transactions t
        JOIN accounts a ON t.id_account = a.id_account
        JOIN menu m ON t.id_menu = m.id_menu
    """

    if query:
        base_query += query

    base_query += " ORDER BY t.date DESC"

    if params:
        cursor.execute(base_query, params)
    else:
        cursor.execute(base_query)

    results = cursor.fetchall()
    cursor.close()
    mydb.close()

    if not results:
        print("\n[!] No transactions found.")
        return

    df = pd.DataFrame(results, columns=[
        'ID', 'Customer', 'Menu', 'Size', 'Qty', 'Total Price', 'Payment', 'Date'
    ])
    df['Total Price'] = df['Total Price'].apply(lambda x: f"Rp {x:,.0f}")
    df.index = df.index + 1

    print(f"\n{'='*90}")
    print(f"  SALES REPORT  ({len(df)} transactions found)")
    print(f"{'='*90}")
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    print(f"{'='*90}\n")

# ──────────────────────────────────────────────
# [1.2] Function to filter sales by date range
# ──────────────────────────────────────────────

def filter_by_date():
    print("  ── Filter by Date Range ──")
    print("  Format: YYYY-MM-DD (e.g. 2026-01-01)\n")

    while True:
        start = input("  Start date: ").strip()
        end = input("  End date  : ").strip()
        try:
            pd.to_datetime(start)
            pd.to_datetime(end)
            break
        except ValueError:
            print("\n[!] Invalid date format. Please use YYYY-MM-DD.\n")

    fn.clearscreen()
    show_sales_table(
        query=" WHERE DATE(t.date) BETWEEN %s AND %s",
        params=(start, end)
    )

# ──────────────────────────────────────────────
# [1.3] Function to filter sales by menu item
# ──────────────────────────────────────────────

def filter_by_menu():
    mydb = fn.conn_sql()
    cursor = mydb.cursor()
    cursor.execute("SELECT DISTINCT name FROM menu ORDER BY name")
    menus = cursor.fetchall()
    cursor.close()
    mydb.close()

    print("  ── Filter by Menu Item ──")
    print("  Available menus:\n")
    for i, (name,) in enumerate(menus, 1):
        print(f"  [{i}] {name}")

    while True:
        try:
            choice = int(input("\n  Select menu number: ").strip())
            if 1 <= choice <= len(menus):
                selected = menus[choice - 1][0]
                break
            else:
                print(f"  [!] Please enter a number between 1 and {len(menus)}.")
        except ValueError:
            print("  [!] Invalid input. Please enter a number.")

    fn.clearscreen()
    show_sales_table(
        query=" WHERE m.name = %s",
        params=(selected,)
    )

# ──────────────────────────────────────────────
# [1.4] Function to filter sales by customer
# ──────────────────────────────────────────────
def filter_by_customer():
    mydb = fn.conn_sql()
    cursor = mydb.cursor()
    cursor.execute("SELECT id_account, username FROM accounts WHERE role = 'customer' ORDER BY username")
    customers = cursor.fetchall()
    cursor.close()
    mydb.close()

    print("  ── Filter by Customer ──")
    print("  Available customers:\n")
    for i, (id_acc, username) in enumerate(customers, 1):
        print(f"  [{i}] {username}")

    while True:
        try:
            choice = int(input("\n  Select customer number: ").strip())
            if 1 <= choice <= len(customers):
                selected_id = customers[choice - 1][0]
                break
            else:
                print(f"  [!] Please enter a number between 1 and {len(customers)}.")
        except ValueError:
            print("  [!] Invalid input. Please enter a number.")

    fn.clearscreen()
    show_sales_table(
        query=" WHERE t.id_account = %s",
        params=(selected_id,)
    )

# ──────────────────────────────────────────────
# FEATURE 2 - SHOW SALES STATISTICS
# ──────────────────────────────────────────────

def admin_show_statistics():
    while True:
        fn.print_header()
        print('''
        ╔══════════════════════════════════════╗
        ║          SALES STATISTICS            ║
        ╠══════════════════════════════════════╣
        ║  [1] All time statistics             ║
        ║  [2] Statistics by date range        ║
        ║  [0] Back                            ║
        ║  [999] Exit Application              ║
        ╚══════════════════════════════════════╝''')
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            fn.clearscreen()
            show_statistics()
            input("\nPress Enter to go back...")
        elif choice == "2":
            fn.clearscreen()
            show_statistics_by_date()
            input("\nPress Enter to go back...")
        elif choice == "0":
            fn.clearscreen()
            break    
        elif choice == "999":
            fn.exit_app()
        else:
            print("\n[!] Invalid choice. Please try again.")
        fn.clearscreen()

# ──────────────────────────────────────────────
#[2.1] Function to show overall sales statistics
# ──────────────────────────────────────────────

def show_statistics(label="ALL TIME", date_filter=None):
    mydb = fn.conn_sql()
    
    query = """
        SELECT 
            t.total_price,
            t.quantity,
            t.payment_method,
            m.name,
            m.size,
            t.date
        FROM transactions t
        JOIN menu m ON t.id_menu = m.id_menu
    """

    if date_filter:
        query += date_filter

    df = pd.read_sql(query, mydb)
    mydb.close()

    df['menu_label'] = df['name'] + ' (' + df['size'] + ')'

    print(df.head())

    total_transactions = len(df)
    total_revenue = df['total_price'].sum()
    avg_transaction_value = df['total_price'].mean()
    
    best_seller = df.groupby('menu_label')['quantity'].sum().idxmax()
    best_seller_qty = df.groupby('menu_label')['quantity'].sum().max()

    print(best_seller, best_seller_qty)

    rev_per_menu = df.groupby('menu_label')['total_price'].sum().reset_index()
    print(rev_per_menu.head())
    rev_per_menu.columns = ['Menu', 'Revenue']
    rev_per_menu = rev_per_menu.sort_values('Revenue', ascending=False)

    
    rev_per_payment = df.groupby('payment_method')['total_price'].sum().reset_index()
    rev_per_payment.columns = ['Payment Method', 'Revenue']

    print(f"\n{'='*55}")
    print(f"  SALES STATISTICS — {label}")
    print(f"{'='*55}")
    print(f"  Total Transactions : {total_transactions:,}")
    print(f"  Total Revenue      : Rp {total_revenue:,.0f}")
    print(f"  Avg Order Value    : Rp {avg_transaction_value:,.0f}")
    print(f"  Best Selling Menu  : {best_seller} — {best_seller_qty:,} pcs sold")

    print(f"\n  {'─'*51}")
    print(f"  REVENUE PER MENU ITEM")
    print(f"  {'─'*51}")
    rev_per_menu['Revenue'] = rev_per_menu['Revenue'].apply(lambda x: f"Rp {x:,.0f}")
    rev_per_menu.index = range(1, len(rev_per_menu) + 1)
    print(tabulate(rev_per_menu, headers='keys', tablefmt='psql', showindex=True))

    print(f"\n  {'─'*51}")
    print(f"  REVENUE PER PAYMENT METHOD")
    print(f"  {'─'*51}")
    rev_per_payment['Revenue'] = rev_per_payment['Revenue'].apply(lambda x: f"Rp {x:,.0f}")
    rev_per_payment.index = range(1, len(rev_per_payment) + 1)
    print(tabulate(rev_per_payment, headers='keys', tablefmt='psql', showindex=True))
    print(f"\n{'='*55}\n")

# ──────────────────────────────────────────────
#[2.2] Function to show sales statistics filtered by date range
# ──────────────────────────────────────────────

def show_statistics_by_date():
    print("  ── Statistics by Date Range ──")
    print("  Format: YYYY-MM-DD (e.g. 2026-01-01)\n")

    while True:
        start = input("  Start date: ").strip()
        end   = input("  End date  : ").strip()
        try:
            pd.to_datetime(start)
            pd.to_datetime(end)
            break
        except ValueError:
            print("\n[!] Invalid date format. Please use YYYY-MM-DD.\n")

    fn.clearscreen()
    show_statistics(
        label=f"{start} to {end}",
        date_filter=f" WHERE DATE(t.date) BETWEEN '{start}' AND '{end}'"
    )