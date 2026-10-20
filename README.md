# TaskMate

A local task-finding and service management system built for the **Class XII Computer Science project**.

A person who needs small work done posts a task. A person who can do it browses the
tasks, accepts one, finishes it, and the owner rates the work. Everything is stored in a
MySQL database and the whole program is written in simple Python.

**Built by:** Alexey & Nandan, Class XII C, Naipunnya
**Tech used:** Python 3, MySQL (Aiven cloud database), `mysql-connector-python`

---

## Table of contents

1. [Why this project](#why-this-project)
2. [Features](#features)
3. [Database design](#database-design)
4. [How the program works](#how-the-program-works)
5. [How to run it](#how-to-run-it)
6. [Sample session](#sample-session)
7. [Class XII concepts used](#class-xii-concepts-used)
8. [Files in this repository](#files-in-this-repository)

---

## Why this project

Local help (a plumber, a gardener, someone to move furniture) is mostly found by word of
mouth. Small tasks stay unclaimed, and nobody keeps a record of who did the work or how
well it was done. TaskMate keeps a simple record of tasks, who claimed them, and how the
work was rated.

---

## Features

| # | Feature | What it does |
|---|---------|--------------|
| 1 | Register | New user gives name, phone, location, username and password |
| 2 | Login | Username and password are checked against the database |
| 3 | Post a task | Title, category, description, location and payment (one-time or hourly) |
| 4 | View available tasks | Only tasks with status `Available` are listed |
| 5 | Search tasks | Filter by category, location, payment type or maximum amount |
| 6 | Accept a task | Task becomes `Accepted` and the worker is recorded. You cannot accept your own task |
| 7 | My posted tasks | Shows the tasks the logged-in user posted |
| 8 | My accepted tasks | Shows the tasks the logged-in user accepted |
| 9 | Update status | Owner marks the task `Completed`, `Cancelled` or `Available` again |
| 10 | Rate a completed task | Owner gives 1 to 5 stars and a review, only for their own completed task |

---

## Database design

Database name: `taskmate` (or the database Aiven gives you).

### users

| Column | Type | Meaning |
|--------|------|---------|
| user_id | INT, primary key, auto increment | Unique id of the user |
| name | VARCHAR(50) | Full name |
| phone | VARCHAR(15) | Contact number |
| location | VARCHAR(50) | Area they stay in |
| username | VARCHAR(30), unique | Used for login |
| password | VARCHAR(30) | Used for login |

### tasks

| Column | Type | Meaning |
|--------|------|---------|
| task_id | INT, primary key, auto increment | Unique id of the task |
| poster_id | INT | `user_id` of the person who posted it |
| title | VARCHAR(50) | Short name of the work |
| category | VARCHAR(30) | Plumbing, Gardening, Cleaning, Moving, Technical Help |
| description | VARCHAR(200) | Details of the work |
| location | VARCHAR(50) | Where the work is |
| pay_type | VARCHAR(10) | `One-Time` or `Hourly` |
| amount | FLOAT | Money offered (Rs) |
| status | VARCHAR(15) | `Available`, `Accepted`, `Completed` or `Cancelled` |

### applications

| Column | Type | Meaning |
|--------|------|---------|
| app_id | INT, primary key, auto increment | Unique id of the application |
| task_id | INT | Task that was accepted |
| worker_id | INT | `user_id` of the person who accepted it |
| status | VARCHAR(15) | Status of this application |

### ratings

| Column | Type | Meaning |
|--------|------|---------|
| rating_id | INT, primary key, auto increment | Unique id of the rating |
| task_id | INT | The rated task |
| stars | INT | 1 to 5 |
| review | VARCHAR(200) | Short written feedback |

The full `CREATE TABLE` statements are in [`schema.sql`](schema.sql), and the same
statements also run automatically inside `setup()` when the program starts.

---

## How the program works

1. `main()` runs `setup()`, which creates the database and the four tables if they are
   not already there.
2. The welcome menu asks for **Register**, **Login** or **Exit**.
3. After login, `login()` returns the `user_id` of that person. This value is passed to
   every function in the user menu, so the program always knows who is using it.
4. `user_menu()` is a `while True` loop. It prints the options and calls the matching
   function, then loops back until the user chooses **Logout**.
5. Every write to the database ends with `con.commit()`, and the connection is closed at
   the end of the program.

Status flow of one task:

```text
Available  -->  Accepted  -->  Completed
     ^                            |
     +------- (owner reopens) ----+
                                  |
                              Cancelled (owner cancels)
```

---

## How to run it

### 1. Install the Python connector

```bash
pip install mysql-connector-python
```

### 2. Run

```bash
python taskmate.py
```

The program connects to the Aiven cloud database (details are already filled in) and
asks for the database password when it starts. The password is never stored in the
code, so this repository is safe to keep public. Tables are created on the first run.

---

## Sample session

```text
****** WELCOME TO TASKMATE ******
1. Register
2. Login
3. Exit
Enter choice: 2

--- LOGIN ---
Username: alexey
Password: ****
Welcome, Alexey

====== TASKMATE MENU ======
1. Post a task
2. View available tasks
...
Enter choice: 1

--- POST A TASK ---
Task title: Fix leaking tap
Category: Plumbing
Description: Bathroom tap drips all night
Location: Koramangala
Payment type: 1. One-Time   2. Hourly
Choose 1 or 2: 1
Total amount (Rs): 350
Task posted successfully!
```

---

## Class XII concepts used

- **Functions** with and without arguments and return values — `register()`, `login()`,
  `post_task(uid)`, `show(rows)`
- **Conditional statements** — `if` / `elif` / `else` in the menus and in the checks
  before accepting, updating and rating a task
- **Loops** — `while True` menus and a `for` loop inside `show()`
- **Exception handling** — `try` / `except` for duplicate usernames and for wrong input
  (`ValueError`)
- **MySQL through `mysql.connector`** — `connect()`, `cursor()`, `execute()`,
  `fetchone()`, `fetchall()`, `rowcount`, `commit()`, `close()`
- **SQL used** — `CREATE DATABASE`, `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`,
  `WHERE`, `ORDER BY`, and a join of `tasks` and `applications` in `my_accepted()`

---

## Files in this repository

| File | What it is |
|------|------------|
| `taskmate.py` | The complete program — all functions, menus and database queries |
| `schema.sql` | Only the SQL: table creation and some sample rows |
| `requirements.txt` | The Python library the project needs |
| `README.md` | This write-up |
| `.gitignore` | Keeps Python cache files out of GitHub |
