import pandas as pd
import sqlite3


DATABASE_PATH = "./data/sales_by_area.db"


conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()

# c.execute('''CREATE TABLE passengers (PassengerId int, Name text, Sex text, Age text, SipSp int, Parch int)''')
# passengers = pd.read_csv('./data/passengers.csv')
# passengers.to_sql('passengers', conn, if_exists='fail', index=False)

# survivors = pd.read_csv('./data/survivors.csv')
# survivors.to_sql('survivors', conn, if_exists='fail', index=False)

# tickets = pd.read_csv('./data/tickets.csv')
# tickets.to_sql('tickets', conn, if_exists='fail', index=False)

introduction = pd.read_csv('./data/hackathon ai - Sheet1.csv')
introduction.to_sql('sales_by_area', conn, if_exists='fail', index=False)


def run_query(query):
    con = sqlite3.connect(DATABASE_PATH)
    try:
        response = pd.read_sql_query(query, con)
        return response
    finally:
        con.close()


# print(run_query("SELECT * FROM passengers LIMIT 2"))
# print(run_query("SELECT * FROM survivors LIMIT 2"))
# print(run_query("SELECT * FROM tickets LIMIT 2"))
print(run_query("SELECT * FROM sales_by_area LIMIT 2"))