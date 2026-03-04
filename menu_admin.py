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
╚══════════════════════════════════════╝''')

        choice = input("Enter your choice: ").strip()
        break