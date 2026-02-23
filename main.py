# Library List
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import git

# Connect to SQL Database
def conn_sql():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="user",
            database="dotdotdot_app"
        )
        print("Connected to database")
        return mydb
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Main Function
def main():
    # Connect to database
    mydb = conn_sql()
    print('''
    Welcome to DotDotDot App!
          ''')

if __name__ == "__main__":
    main()