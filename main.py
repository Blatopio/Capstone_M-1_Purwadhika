import function as fn
# Main Function
def main():
    #clear screen
    fn.clearscreen()
    # Connect to database
    mydb = fn.conn_sql()
    
    while True:
        fn.print_header()
        print('''
            ╔══════════════════════════════════════╗
            ║ [1] Login to existing account        ║
            ║ [2] Create new account               ║
            ║ [0] Exit                             ║
            ╚══════════════════════════════════════╝''')
        choice = input("\nEnter your choice: ").strip()
        fn.clearscreen()
        if choice == "1":
            print("\n[Login]")
            username, password = fn.login_menu()
            user = fn.auth_verify(username, password)
            if user:
                fn.clearscreen()
                fn.route_to_menu(user)

        elif choice == "2":
            print("Create new account")

        elif choice == "0":
            fn.exit_app()
        
        else:
            print("\n[Invalid choice. Please enter 1 or 2 and 0 for exit.]")
    fn.clearscreen()        

if __name__ == "__main__":
    main()