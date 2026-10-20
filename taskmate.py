# ==========================================================
#  TASKMATE - A Local Task-Finding and Service Management System
#  Class XII Computer Science Project (Python + MySQL)
#  By: Alexey & Nandan, XII C, Naipunnya
# ==========================================================
#  Before running:
#    1. Install the connector:   pip install mysql-connector-python
#    2. Fill in your database details in the DB block below.
#    3. Run:   python taskmate.py
#  The program creates the tables by itself on the first run.
# ==========================================================

import mysql.connector

# ---------- Aiven (cloud) database details ----------
# The password is NOT written here, so this file is safe to put on GitHub.
# The program asks for it when it starts.
DB = {
    "host": "mysql-369426a7-alexeysaji-2ca2.k.aivencloud.com",
    "port": 28697,
    "user": "avnadmin",
    "database": "defaultdb",
}
DB["password"] = input("Enter Aiven password: ")

# ---------- Connect to MySQL ----------
try:
    con = mysql.connector.connect(**DB)
    cur = con.cursor()
except mysql.connector.Error as e:
    print("Could not connect to MySQL:", e)
    print("Check the password, and that the Aiven service is switched on.")
    raise SystemExit

# ---------- Create tables (only first time) ----------
def setup():
    try:
        cur.execute("CREATE DATABASE IF NOT EXISTS taskmate")
        cur.execute("USE taskmate")
    except:
        pass          # on Aiven the database already exists, so just skip

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   user_id INT PRIMARY KEY AUTO_INCREMENT,
                   name VARCHAR(50),
                   phone VARCHAR(15),
                   location VARCHAR(50),
                   username VARCHAR(30) UNIQUE,
                   password VARCHAR(30))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
                   task_id INT PRIMARY KEY AUTO_INCREMENT,
                   poster_id INT,
                   title VARCHAR(50),
                   category VARCHAR(30),
                   description VARCHAR(200),
                   location VARCHAR(50),
                   pay_type VARCHAR(10),
                   amount FLOAT,
                   status VARCHAR(15))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS applications(
                   app_id INT PRIMARY KEY AUTO_INCREMENT,
                   task_id INT,
                   worker_id INT,
                   status VARCHAR(15))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS ratings(
                   rating_id INT PRIMARY KEY AUTO_INCREMENT,
                   task_id INT,
                   stars INT,
                   review VARCHAR(200))""")
    con.commit()


# ---------- 1. Register a new user ----------
def register():
    print("\n--- REGISTER ---")
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    location = input("Enter location: ")
    username = input("Choose username: ")
    password = input("Choose password: ")
    try:
        q = "INSERT INTO users(name,phone,location,username,password) VALUES(%s,%s,%s,%s,%s)"
        cur.execute(q, (name, phone, location, username, password))
        con.commit()
        print("Registered successfully! Please login.")
    except:
        print("That username is already taken.")


# ---------- 2. Login ----------
def login():
    print("\n--- LOGIN ---")
    username = input("Username: ")
    password = input("Password: ")
    q = "SELECT user_id, name FROM users WHERE username=%s AND password=%s"
    cur.execute(q, (username, password))
    row = cur.fetchone()
    if row == None:
        print("Wrong username or password.")
        return 0
    else:
        print("Welcome,", row[1])
        return row[0]          # return the user's id


# ---------- 3. Post a new task ----------
def post_task(uid):
    print("\n--- POST A TASK ---")
    title = input("Task title: ")
    print("Categories: Plumbing, Gardening, Cleaning, Moving, Technical Help")
    category = input("Category: ")
    desc = input("Description: ")
    location = input("Location: ")
    print("Payment type: 1. One-Time   2. Hourly")
    ch = input("Choose 1 or 2: ")
    if ch == "2":
        pay_type = "Hourly"
        amount = float(input("Rate per hour (Rs): "))
    else:
        pay_type = "One-Time"
        amount = float(input("Total amount (Rs): "))
    q = """INSERT INTO tasks(poster_id,title,category,description,location,pay_type,amount,status)
           VALUES(%s,%s,%s,%s,%s,%s,%s,'Available')"""
    cur.execute(q, (uid, title, category, desc, location, pay_type, amount))
    con.commit()
    print("Task posted successfully!")


# ---------- Helper: print a list of tasks ----------
def show(rows):
    if len(rows) == 0:
        print("No tasks found.")
        return
    print("\nID | Title | Category | Location | Payment | Amount | Status")
    print("-" * 65)
    for r in rows:
        print(r[0], "|", r[1], "|", r[2], "|", r[3], "|", r[4], "|", r[5], "|", r[6])


# ---------- 4. View all available tasks ----------
def view_tasks():
    q = "SELECT task_id,title,category,location,pay_type,amount,status FROM tasks WHERE status='Available'"
    cur.execute(q)
    show(cur.fetchall())


# ---------- 5. Search / filter tasks ----------
def search_tasks():
    print("\nSearch by: 1. Category  2. Location  3. Payment type  4. Maximum amount")
    ch = input("Choice: ")
    base = "SELECT task_id,title,category,location,pay_type,amount,status FROM tasks WHERE status='Available' AND "
    if ch == "1":
        cur.execute(base + "category=%s", (input("Category: "),))
    elif ch == "2":
        cur.execute(base + "location=%s", (input("Location: "),))
    elif ch == "3":
        cur.execute(base + "pay_type=%s", (input("One-Time or Hourly: "),))
    elif ch == "4":
        cur.execute(base + "amount<=%s", (float(input("Maximum amount: ")),))
    else:
        print("Invalid choice.")
        return
    show(cur.fetchall())


# ---------- 6. Accept a task ----------
def accept_task(uid):
    view_tasks()
    tid = int(input("\nEnter Task ID to accept: "))
    cur.execute("SELECT poster_id, status FROM tasks WHERE task_id=%s", (tid,))
    row = cur.fetchone()
    if row == None:
        print("No such task.")
    elif row[0] == uid:
        print("You cannot accept your own task.")
    elif row[1] != "Available":
        print("This task is not available.")
    else:
        cur.execute("UPDATE tasks SET status='Accepted' WHERE task_id=%s", (tid,))
        cur.execute("INSERT INTO applications(task_id,worker_id,status) VALUES(%s,%s,'Accepted')", (tid, uid))
        con.commit()
        print("Task accepted!")


# ---------- 7. View my posted tasks ----------
def my_posted(uid):
    q = "SELECT task_id,title,category,location,pay_type,amount,status FROM tasks WHERE poster_id=%s"
    cur.execute(q, (uid,))
    show(cur.fetchall())


# ---------- 8. View tasks I accepted ----------
def my_accepted(uid):
    q = """SELECT t.task_id,t.title,t.category,t.location,t.pay_type,t.amount,t.status
           FROM tasks t, applications a
           WHERE t.task_id=a.task_id AND a.worker_id=%s"""
    cur.execute(q, (uid,))
    show(cur.fetchall())


# ---------- 9. Update status of my task ----------
def update_status(uid):
    my_posted(uid)
    tid = int(input("\nEnter Task ID to update: "))
    print("New status: 1. Completed  2. Cancelled  3. Available")
    ch = input("Choice: ")
    if ch == "1":
        status = "Completed"
    elif ch == "2":
        status = "Cancelled"
    elif ch == "3":
        status = "Available"
    else:
        print("Invalid choice.")
        return
    cur.execute("UPDATE tasks SET status=%s WHERE task_id=%s AND poster_id=%s", (status, tid, uid))
    con.commit()
    if cur.rowcount == 0:
        print("You can only update your own tasks.")
    else:
        print("Status updated to", status)


# ---------- 10. Rate a completed task ----------
def rate_task(uid):
    tid = int(input("Enter Task ID of your completed task: "))
    cur.execute("SELECT status FROM tasks WHERE task_id=%s AND poster_id=%s", (tid, uid))
    row = cur.fetchone()
    if row == None or row[0] != "Completed":
        print("You can rate only your own completed tasks.")
        return
    stars = int(input("Stars (1 to 5): "))
    if stars < 1 or stars > 5:
        print("Stars must be between 1 and 5.")
        return
    review = input("Review: ")
    cur.execute("INSERT INTO ratings(task_id,stars,review) VALUES(%s,%s,%s)", (tid, stars, review))
    con.commit()
    print("Thank you for the rating!")


# ---------- Menu after login ----------
def user_menu(uid):
    while True:
        print("\n====== TASKMATE MENU ======")
        print("1. Post a task")
        print("2. View available tasks")
        print("3. Search tasks")
        print("4. Accept a task")
        print("5. My posted tasks")
        print("6. My accepted tasks")
        print("7. Update task status")
        print("8. Rate a completed task")
        print("9. Logout")
        ch = input("Enter choice: ")
        try:
            if ch == "1":
                post_task(uid)
            elif ch == "2":
                view_tasks()
            elif ch == "3":
                search_tasks()
            elif ch == "4":
                accept_task(uid)
            elif ch == "5":
                my_posted(uid)
            elif ch == "6":
                my_accepted(uid)
            elif ch == "7":
                update_status(uid)
            elif ch == "8":
                rate_task(uid)
            elif ch == "9":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")


# ---------- Main menu ----------
def main():
    setup()
    while True:
        print("\n****** WELCOME TO TASKMATE ******")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        ch = input("Enter choice: ")
        if ch == "1":
            register()
        elif ch == "2":
            uid = login()
            if uid != 0:
                user_menu(uid)
        elif ch == "3":
            print("Thank you for using TaskMate!")
            break
        else:
            print("Invalid choice.")


main()
con.close()
