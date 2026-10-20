-- =====================================================
--  TASKMATE database (Class XII Computer Science project)
--  Run this in the Aiven Console "SQL shell", or in MySQL
--  Workbench, if you want the tables made before the first
--  run of taskmate.py. The program also creates them itself.
-- =====================================================

CREATE DATABASE IF NOT EXISTS taskmate;
USE taskmate;

CREATE TABLE IF NOT EXISTS users(
    user_id   INT PRIMARY KEY AUTO_INCREMENT,
    name      VARCHAR(50),
    phone     VARCHAR(15),
    location  VARCHAR(50),
    username  VARCHAR(30) UNIQUE,
    password  VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS tasks(
    task_id     INT PRIMARY KEY AUTO_INCREMENT,
    poster_id   INT,
    title       VARCHAR(50),
    category    VARCHAR(30),
    description VARCHAR(200),
    location    VARCHAR(50),
    pay_type    VARCHAR(10),
    amount      FLOAT,
    status      VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS applications(
    app_id    INT PRIMARY KEY AUTO_INCREMENT,
    task_id   INT,
    worker_id INT,
    status    VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS ratings(
    rating_id INT PRIMARY KEY AUTO_INCREMENT,
    task_id   INT,
    stars     INT,
    review    VARCHAR(200)
);

-- ---------- Sample rows for the demonstration ----------
INSERT INTO users(name, phone, location, username, password) VALUES
('Alexey Saji', '9886000001', 'Koramangala', 'alexey', 'abc123'),
('Nandan K',    '9886000002', 'Indiranagar', 'nandan', 'abc123'),
('Rhea Menon',  '9886000003', 'Jayanagar',   'rhea',   'abc123');

INSERT INTO tasks(poster_id, title, category, description, location, pay_type, amount, status) VALUES
(1, 'Fix leaking tap',      'Plumbing',       'Bathroom tap drips all night',      'Koramangala', 'One-Time', 350, 'Available'),
(1, 'Mow the lawn',         'Gardening',      'Front lawn needs cutting',          'Koramangala', 'Hourly',   250, 'Available'),
(3, 'Move two boxes',       'Moving',         'Shift boxes from 3rd floor to 1st', 'Jayanagar',   'One-Time', 400, 'Available'),
(2, 'Clean the kitchen',    'Cleaning',       'Full kitchen deep cleaning',        'Indiranagar', 'One-Time', 600, 'Accepted'),
(2, 'Set up the printer',   'Technical Help', 'Printer is not connecting to Wi-Fi','Indiranagar', 'Hourly',   300, 'Completed');

INSERT INTO applications(task_id, worker_id, status) VALUES
(4, 3, 'Accepted'),
(5, 3, 'Accepted');

INSERT INTO ratings(task_id, stars, review) VALUES
(5, 4, 'Sorted out quickly and explained the settings.');

-- ---------- Useful queries to show in the viva ----------
SELECT task_id, title, category, location, amount
FROM tasks
WHERE status = 'Available';

SELECT t.task_id, t.title, t.amount, u.name AS worker
FROM tasks t, applications a, users u
WHERE t.task_id = a.task_id AND a.worker_id = u.user_id;

SELECT AVG(stars) AS average_stars FROM ratings;
