import function as fn

# ──────────────────────────────────────────────
# STORE MANAGER MENU
# ──────────────────────────────────────────────
def store_manager_menu(user):
    while True:
        print(r'''
   ___       __  ___       __  ___       __      ___   ___  ___ 
  / _ \___  / /_/ _ \___  / /_/ _ \___  / /_    / _ | / _ \/ _  \
 / // / _ \/ __/ // / _ \/ __/ // / _ \/ __/   / __ |/ ___/ ___/    
/____/\___/\__/____/\___/\__/____/\___/\__/   /_/ |_/_/  /_/ 
              ''')
        print(f'''
              
╔══════════════════════════════════════╗
║          STORE MANAGER PANEL         ║
║  Logged in as: {user['username']:^22}║
╠══════════════════════════════════════╣
║  [1] View Current Stock              ║
║  [2] Update Stock                    ║
║  [3] Show Stock Statistics           ║
║  [0] Logout                          ║
╚══════════════════════════════════════╝''')

        choice = input("Enter your choice: ").strip()
        break