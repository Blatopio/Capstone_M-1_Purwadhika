#---------------
# Library List
#---------------
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import os
import sys

#---------------
# Exit Application
#---------------
def exit_app():
    print("Exiting the application...")
    sys.exit()

#---------------
# Print Header
#---------------
def print_header():
    print(r'''
   ___       __  ___       __  ___       __      ___   ___  ___ 
  / _ \___  / /_/ _ \___  / /_/ _ \___  / /_    / _ | / _ \/ _  \
 / // / _ \/ __/ // / _ \/ __/ // / _ \/ __/   / __ |/ ___/ ___/    
/____/\___/\__/____/\___/\__/____/\___/\__/   /_/ |_/_/  /_/    
                                                                
          ''')

#---------------
# Clear Screen
#---------------
def clearscreen():
    # 'nt' is the name for Windows OS, 'posix' for Linux/macOS
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

#---------------
# Connect to SQL Database
#---------------
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

#---------------
# Login
# ---------------
def login_menu():
    #get user input for login
    username = input('\nUsername: ')
    password = input('Password: ')
    print(f"\nAttempting login for user: {username}\n")
    return username, password

def auth_verify(username, password):
    #verify login credentials
    mydb = conn_sql()
    cursor = mydb.cursor()
    query = "SELECT id_account, username, role FROM accounts WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    
    if result:
        id_account, username, role = result
        print(f"\nLogin successful! Welcome, {username}!")
        return {"id_account": id_account, "username": username, "role": role}
    else:
        print("Invalid username or password!, Please try again or make a new account.")
        
#---------------
# Routing menu based on role
#---------------
def route_to_menu(user):
    """Routes the logged-in user to the correct menu based on their role."""
    from menu_admin import admin_menu
    from menu_strmanager import store_manager_menu
    from menu_customer import customer_menu

    role = user['role']
    if role == 'admin':
        admin_menu(user)
    elif role == 'store_manager':
        store_manager_menu(user)
    elif role == 'customer':
        customer_menu(user)
    else:
        print(f"\n[!] Unknown role '{role}'. Access denied.")