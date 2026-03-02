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
    result = cursor.fetchall()
    print(f"Login query executed. Result: {result}")
    if result:
        print("Login successful!")
        auth = True
        while auth:
            print("\n[1] View Profile")
            print("[2] Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                print("Viewing profile...")
            elif choice == "2":
                print("Logging out...")
                auth = False
    else:
        print("Invalid username or password.")
        

