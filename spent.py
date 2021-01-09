import sqlite3 as db
from datetime import datetime
import winsound

def main():
    print("\nEXPENSE TRACKER SYSTEM:\n")
    n=0
    global limit
    limit = int(input("Please set a limit to the tracker: "))
    while True:

        conn = db.connect("spent.db")
        cur = conn.cursor()
        init()
        print("\n1 - To log in your puchase")
        print("2 - To track your previous expense")
        print("3 - To change limit in your Expense Tracker")
        print("4 - To delete all your previous records")
        print("5 - To exit\n")
        n = int(input("Enter your choice: "))

        if n==1:
            print("\nPlease log in your recent purchase here")
            amt = input("Enter amount of the purchased item: ")
            c = input("Specify the category: ")
            msg = input("You can add a detailed description of your recent purchase here: ")
            log(amt, c, msg)
            print("\nYour information is logged in successfully!")

        elif n==2:
            print("\nA - To view your overall expense")
            print("B - To view your expense in a particular category\n")
            ch = input("Enter your choice: ")
            if ch=="A":
                print(view())
            elif ch=="B":
                cat = input("\nSpecify the category: ")
                print(view(cat))
            else:
                print("Invalid error")

        elif n==3:
            lim = input("\nSet the limit to: ")
            setlimit(lim)

        elif n==4:
            deleteall()
            print("All records deleted successfully!")

        elif n==5:
            conn.close()
            print("The Sqlite connection is closed")
            break

        else:
            print("Invalid Error")

def init():
    conn = db.connect("spent.db")
    cur = conn.cursor()
    sql = ''' create table if not exists expenses (amount number, category string,
    message string, date string) '''
    cur.execute(sql)
    conn.commit()

def log(amount, category, message=""):
    date = str(datetime.now())
    conn = db.connect("spent.db")
    cur = conn.cursor()
    sql = ''' insert into expenses values ({},'{}','{}','{}') '''.format(amount,
    category,message,date)
    cur.execute(sql)
    conn.commit()

def setlimit(limit):
    print("Limit is now set to: ",limit)

def view(category=None):
    conn = db.connect("spent.db")
    cur = conn.cursor()
    if category:
        sql = '''
        select * from expenses where category = '{}'
        '''.format(category)
        sql2 = '''
        select sum(amount) from expenses where category = '{}'
        '''.format(category)
    else:
        sql = '''
        select * from expenses
        '''.format(category)
        sql2 = '''
        select sum(amount) from expenses
        '''.format(category)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    try:
        if total_amount >= limit:
            print("You've reached the maximum limit!")
            print("Total: ",total_amount)
            duration = 1000
            freq=400
            winsound.Beep(freq, duration)
        elif total_amount < limit:
            for i in results:
                print(i)
    except:
        print("There no records present in the tracker currently.")
    return total_amount

def deleteall():
    conn = db.connect("spent.db")
    cur = conn.cursor()
    sql = 'delete from expenses'
    cur.execute(sql)
    conn.commit()

main()
