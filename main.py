import function as fn
# Main Function
def main():
    # Connect to database
    mydb = fn.conn_sql()
    print(r'''
   ___       __  ___       __  ___       __      ___   ___  ___ 
  / _ \___  / /_/ _ \___  / /_/ _ \___  / /_    / _ | / _ \/ _  \
 / // / _ \/ __/ // / _ \/ __/ // / _ \/ __/   / __ |/ ___/ ___/    
/____/\___/\__/____/\___/\__/____/\___/\__/   /_/ |_/_/  /_/    
                                                                
╔══════════════════════════════════════╗
║ [1] Login to existing account        ║
║ [2] Create new account               ║
║ [0] Exit                             ║
╚══════════════════════════════════════╝
          ''')
    
    while True:
        choice = int(input("Enter your choice: ").strip())

        if choice == 1:
            print("\n[Login]")
            username, password = fn.login_menu()
            user = fn.auth_verify(username, password)
            if user:
                fn.route_to_menu(user)

        elif choice == 2:
            print("Create new account")

        elif choice == 0:
            print("Exiting the application...")
            break
        
        else:
            print("Invalid choice. Please enter 1 or 2 and 0 for exit.")

if __name__ == "__main__":
    main()