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
        ║  [1] Calculate average by column     ║
        ║  [2] All time statistics             ║
        ║  [3] Statistics by date range        ║
        ║  [0] Back                            ║
        ║  [999] Exit Application              ║
        ╚══════════════════════════════════════╝''')
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            fn.clearscreen()
            calculate_average()
            input("\nPress Enter to go back...")
        elif choice == "2":
            fn.clearscreen()
            show_statistics()
            input("\nPress Enter to go back...")
        elif choice == "3":
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
#[2.1] Function to Calculate average by column
# ──────────────────────────────────────────────

def calculate_average():
    mydb = fn.conn_sql()

    query = """
        SELECT 
            t.total_price,
            t.quantity,
            t.payment_method,
            m.name,
            m.size
        FROM transactions t
        JOIN menu m ON t.id_menu = m.id_menu
    """

    df = pd.read_sql(query, mydb)
    mydb.close()

    
    print(f"\n{'='*70}")
    print(f"  DATA PREVIEW (first 10 rows)")
    print(f"{'='*70}")
    print(tabulate(df.head(10), headers='keys', tablefmt='psql', showindex=False))
    print(f"{'='*70}\n")

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    print("  Available columns for average calculation:\n")
    for i, col in enumerate(numeric_cols, 1):
        print(f"  [{i}] {col}")

    while True:
        try:
            choice = int(input("\n  Select column number: ").strip())
            if 1 <= choice <= len(numeric_cols):
                selected_col = numeric_cols[choice - 1]
                break
            else:
                print(f"  [!] Please enter a number between 1 and {len(numeric_cols)}.")
        except ValueError:
            print("  [!] Invalid input. Please enter a number.")

    avg = df[selected_col].mean()

    print(f"\n{'='*55}")
    print(f"  AVERAGE CALCULATION")
    print(f"{'='*55}")
    if selected_col == 'total_price':
        print(f"  Column         : {selected_col}")
        print(f"  Average Value  : Rp {avg:,.0f}")
    else:
        print(f"  Column         : {selected_col}")
        print(f"  Average Value  : {avg:.2f}")
    print(f"{'='*55}\n")

# ──────────────────────────────────────────────
#[2.2] Function to show overall sales statistics
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

    total_transactions = len(df)
    total_revenue = df['total_price'].sum()
    avg_transaction_value = df['total_price'].mean()
    
    best_seller = df.groupby('menu_label')['quantity'].sum().idxmax()
    best_seller_qty = df.groupby('menu_label')['quantity'].sum().max()

    rev_per_menu = df.groupby('menu_label')['total_price'].sum().reset_index()
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
#[2.3] Function to show sales statistics filtered by date range
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

# ──────────────────────────────────────────────
# FEATURE 3 - SHOW SALES CHART
# ──────────────────────────────────────────────

def admin_show_chart():
    while True:
        fn.print_header()
        print('''
        ╔══════════════════════════════════════╗
        ║           SALES CHART                ║
        ╠══════════════════════════════════════╣
        ║  [1] All time chart                  ║
        ║  [2] Chart by date range             ║
        ║  [0] Back                            ║
        ║  [999] Exit Application              ║
        ╚══════════════════════════════════════╝''')
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            fn.clearscreen()
            show_chart()
            input("\nPress Enter to go back...")
        elif choice == "2":
            fn.clearscreen()
            show_chart_by_date()
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
#[3.1] Function to show sales chart (overall and by date range)
# ──────────────────────────────────────────────

def show_chart(label="ALL TIME", date_filter=None):
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

    df["date"]       = pd.to_datetime(df["date"])
    df["month"]      = df["date"].dt.to_period("M").astype(str)
    df["menu_label"] = df["name"].str.replace("Coffee ", "") + "\n(" + df["size"] + ")"
    print(df)

    rev_menu  = df.groupby("menu_label")["total_price"].sum().reset_index()
    rev_menu  = rev_menu.sort_values("total_price", ascending=False)
    rev_pay   = df.groupby("payment_method")["total_price"].sum().reset_index()
    rev_month = df.groupby("month")["total_price"].sum().reset_index()
    best      = df.groupby("menu_label")["quantity"].sum().idxmax()

    # Colors
    CARD_COLORS = ["#4361EE", "#F72585", "#4CC9F0", "#7209B7"]
    BAR_COLORS  = ["#4361EE", "#4895EF", "#4CC9F0",
                   "#F72585", "#B5179E", "#7209B7",
                   "#3A0CA3", "#480CA8", "#560BAD"]
    PIE_COLORS  = ["#4361EE", "#F72585"]
    BG_CHART    = "#FAFAFA"

    # Figure
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor("#FFFFFF")
    gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.6, wspace=0.4)

    # Cards
    card_data = [
        ("Total Transactions", f"{len(df):,}",                           CARD_COLORS[0]),
        ("Total Revenue",      f"Rp {df['total_price'].sum()/1e6:.2f}M", CARD_COLORS[1]),
        ("Avg Order Value",    f"Rp {df['total_price'].mean():,.0f}",     CARD_COLORS[2]),
        ("Best Seller",        best.replace("\n", " "),                   CARD_COLORS[3]),
    ]
    for i, (title, val, color) in enumerate(card_data):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor("#F0F4FF")
        ax.plot([0.05, 0.95], [0.92, 0.92], color=color, linewidth=4,
                transform=ax.transAxes, solid_capstyle='round')
        ax.text(0.5, 0.58, val, ha='center', va='center',
                fontsize=13, fontweight='bold', color=color,
                transform=ax.transAxes)
        ax.text(0.5, 0.2, title, ha='center', va='center',
                fontsize=8, color='#555555', transform=ax.transAxes)
        for spine in ax.spines.values():
            spine.set_edgecolor('#DDDDDD')
            spine.set_linewidth(1)
        ax.set_xticks([])
        ax.set_yticks([])

    # Bar chart
    ax1 = fig.add_subplot(gs[1, :2])
    ax1.set_facecolor(BG_CHART)
    bars = ax1.bar(rev_menu["menu_label"], rev_menu["total_price"],
                   color=BAR_COLORS[:len(rev_menu)], edgecolor='white', linewidth=0.5)
    ax1.set_title("Revenue per Menu Item", fontsize=11, fontweight='bold', color='#333333', pad=10)
    ax1.tick_params(colors='#555555', labelsize=7)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"Rp {x/1e6:.1f}M"))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('#DDDDDD')
    ax1.spines['bottom'].set_color('#DDDDDD')
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 30000,
                 f"Rp {h/1e6:.1f}M", ha='center', va='bottom',
                 fontsize=6.5, color='#333333')

    # Pie chart
    ax2 = fig.add_subplot(gs[1, 2:])
    ax2.set_facecolor(BG_CHART)
    wedges, texts, autotexts = ax2.pie(
        rev_pay["total_price"],
        labels=rev_pay["payment_method"],
        autopct='%1.1f%%',
        colors=PIE_COLORS,
        startangle=90,
        wedgeprops=dict(edgecolor='white', linewidth=2),
        textprops={'fontsize': 9, 'color': '#333333'}
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
    ax2.set_title("Revenue by Payment Method", fontsize=11, fontweight='bold', color='#333333', pad=10)

    # Line chart
    ax3 = fig.add_subplot(gs[2, :2])
    ax3.set_facecolor(BG_CHART)
    ax3.plot(rev_month["month"], rev_month["total_price"],
             marker='o', color="#F72585", linewidth=2.5,
             markersize=6, markerfacecolor='white', markeredgewidth=2)
    ax3.fill_between(range(len(rev_month)), rev_month["total_price"],
                     alpha=0.1, color="#F72585")
    ax3.set_title("Revenue Over Time", fontsize=11, fontweight='bold', color='#333333', pad=10)
    ax3.tick_params(colors='#555555', labelsize=8, axis='x', rotation=30)
    ax3.tick_params(colors='#555555', labelsize=8, axis='y')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"Rp {x/1e6:.1f}M"))
    ax3.set_xticks(range(len(rev_month)))
    ax3.set_xticklabels(rev_month["month"])
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color('#DDDDDD')
    ax3.spines['bottom'].set_color('#DDDDDD')

    # Histogram
    ax4 = fig.add_subplot(gs[2, 2:])
    ax4.set_facecolor(BG_CHART)
    import numpy as np
    n, bins, patches = ax4.hist(df["total_price"], bins=20,
                                edgecolor='white', linewidth=0.5)
    for patch, color in zip(patches, plt.cm.cool(np.linspace(0.2, 0.9, len(patches)))):
        patch.set_facecolor(color)
    ax4.set_title("Order Value Distribution", fontsize=11, fontweight='bold', color='#333333', pad=10)
    ax4.tick_params(colors='#555555', labelsize=8)
    ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"Rp {int(x/1000)}k"))
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.spines['left'].set_color('#DDDDDD')
    ax4.spines['bottom'].set_color('#DDDDDD')

    # ── Title & show ──
    fig.suptitle(f"DotDotDot Café — Sales Dashboard ({label})",
                 fontsize=16, fontweight='bold', color='#222222', y=0.98)
    print("\n  [!] Chart is opening in a new window...")
    plt.show()

# ──────────────────────────────────────────────
#[3.2] Function to show sales chart filtered by date range
# ──────────────────────────────────────────────

def show_chart_by_date():
    print("  ── Chart by Date Range ──")
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
    show_chart(
        label=f"{start} to {end}",
        date_filter=f" WHERE DATE(t.date) BETWEEN '{start}' AND '{end}'"
    )

# ──────────────────────────────────────────────
# FEATURE 4 - MANAGE MENU (ADD/EDIT/DELETE)
# ──────────────────────────────────────────────

def admin_manage_menu():
    while True:
        fn.print_header()
        print('''
        ╔══════════════════════════════════════╗
        ║           MANAGE MENU                ║
        ╠══════════════════════════════════════╣
        ║  [1] Add new menu item               ║
        ║  [2] Edit menu price                 ║
        ║  [3] Delete menu item                ║
        ║  [0] Back                            ║
        ║  [999] Exit Application              ║
        ╚══════════════════════════════════════╝''')
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            fn.clearscreen()
            add_menu_item()
            input("\nPress Enter to go back...")
        elif choice == "2":
            fn.clearscreen()
            edit_menu_price()
            input("\nPress Enter to go back...")
        elif choice == "3":
            fn.clearscreen()
            delete_menu_item()
            input("\nPress Enter to go back...")
        elif choice == "0":
            fn.clearscreen()
            break
        elif choice == "999":
            fn.exit_app()
        else:
            print("\n[!] Invalid choice. Please try again.")
        fn.clearscreen()

        