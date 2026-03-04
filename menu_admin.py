import function as fn

# ──────────────────────────────────────────────
# ADMIN MENU
# ──────────────────────────────────────────────
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

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            print("\n[View Sales Report]")
            # Call function to view sales report
        elif choice == "2":
            print("\n[Show Sales Statistics]")
            # Call function to show sales statistics
        elif choice == "3":
            print("\n[Show Sales Chart]")
            # Call function to show sales chart
        elif choice == "4":
            print("\n[Manage Menu (Add/Edit/Delete)]")
            # Call function to manage menu
        elif choice == "5":
            print("\n[Remove Customer Account]")
            # Call function to remove customer account
        elif choice == "0":
            print("Logging out...")
            fn.clearscreen()
            break
        elif choice == "999":
            fn.exit_app()
        else:
            print("\n[Invalid choice. Please enter a valid option.]")
        fn.clearscreen()