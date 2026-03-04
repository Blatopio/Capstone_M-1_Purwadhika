import function as fn
# Main Function
def main():
    #clear screen
    fn.clearscreen()
    # Connect to database
    mydb = fn.conn_sql()
    
    while True:
        print(r'''
   ___       __  ___       __  ___       __      ___   ___  ___ 
  / _ \___  / /_/ _ \___  / /_/ _ \___  / /_    / _ | / _ \/ _  \
 / // / _ \/ __/ // / _ \/ __/ // / _ \/ __/   / __ |/ ___/ ___/    
/____/\___/\__/____/\___/\__/____/\___/\__/   /_/ |_/_/  /_/    
                                                                
          ''')
        print('''
╔══════════════════════════════════════╗
║ [1] Login to existing account        ║
║ [2] Create new account               ║
║ [0] Exit                             ║
╚══════════════════════════════════════╝''')
        choice = int(input("\nEnter your choice: ").strip())
        fn.clearscreen()
        if choice == 1:
            print("\n[Login]")
            username, password = fn.login_menu()
            user = fn.auth_verify(username, password)
            if user:
                fn.clearscreen()
                fn.route_to_menu(user)

        elif choice == 2:
            print("Create new account")

        elif choice == 0:
            print("Exiting the application...")
            break
        
        else:
            print("\n[Invalid choice. Please enter 1 or 2 and 0 for exit.]")
    fn.clearscreen()        

if __name__ == "__main__":
    main()