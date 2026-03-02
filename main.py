import function
# Main Function
def main():
    # Connect to database
    mydb = function.conn_sql()
    print(r'''
   ___       __  ___       __  ___       __      ___   ___  ___ 
  / _ \___  / /_/ _ \___  / /_/ _ \___  / /_    / _ | / _ \/ _  \
 / // / _ \/ __/ // / _ \/ __/ // / _ \/ __/   / __ |/ ___/ ___/
/____/\___/\__/____/\___/\__/____/\___/\__/   /_/ |_/_/  /_/    
                                                                
[1] Login to existing account
[2] Create new account

[Exit]         
          ''')
    
    choice = input("Enter your choice: ")
    if choice == "1":
        print("\n[Login to existing account]")
        username, password = function.login_menu()
        function.auth_verify(username, password)
    elif choice == "2":
        print("Create new account")
    elif choice.lower() == "exit":
        print("Exiting the application.")
        return
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()