# Library List
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector

# Connect to SQL Database
def conn_sql():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="user",
            database="dotdotdot_app"
        )
        # print("*Connected to database...*", flush=True)
        return mydb
    except mysql.connector.Error as err:
        print(f"Error: {err}")

#Menu
def login_menu():
    #get user input for login
    username = input('\nUsername: ')
    password = input('Password: ')
    print(f"\nAttempting login for user: {username}")
    return username, password

def auth_verify(username, password):
    #verify login credentials
    mydb = conn_sql()
    cursor = mydb.cursor()
    query = "SELECT * FROM accounts WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    # print(f"Login query executed. Result: {result}")
    if result:
        print("Login successful!")
        auth = True
        return True
    else:
        print("Invalid username or password.")
        return False

    while auth:
# Main Function
def main():
    # Connect to database
    mydb = conn_sql()
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
        username, password = login_menu()
        auth_verify(username, password)
    elif choice == "2":
        print("Create new account")
    elif choice.lower() == "exit":
        print("Exiting the application.")
        return
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()