import function as fn
import pandas as pd
from tabulate import tabulate

# ──────────────────────────
# Main menu for admin
# ──────────────────────────
def admin_menu(user):
    while True:
        print(r'''
   ___       __  ___       __  ___       __      ___   ___  ___ 
  / _ \___  / /_/ _ \___  / /_/ _ \___  / /_    / _ | / _ \/ _  \
 / // / _ \/ __/ // / _ \/ __/ // / _ \/ __/   / __ |/ ___/ ___/    
/____/\___/\__/____/\___/\__/____/\___/\__/   /_/ |_/_/  /_/ 
              ''')
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
        print('''
        ╔══════════════════════════════════════╗
        ║          VIEW SALES REPORT           ║
        ╠══════════════════════════════════════╣
        ║  [1] Show all transactions           ║
        ║  [2] Filter by date range            ║
        ║  [3] Filter by menu item             ║
        ║  [4] Filter by customer              ║
        ║  [0] Back                            ║
        ╚══════════════════════════════════════╝''')
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            fn.clearscreen()
            show_sales_table()
        elif choice == "2":
            fn.clearscreen()
            filter_by_date()
        elif choice == "3":
            fn.clearscreen()
            filter_by_menu()
        elif choice == "4":
            fn.clearscreen()
            filter_by_customer()
        elif choice == "0":
            fn.clearscreen()
            break
        else:
            print("\n[!] Invalid choice. Please try again.")
        input("\nPress Enter to continue...")
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

