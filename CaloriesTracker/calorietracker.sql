--
-- File generated with Letos v4.0.0 on Sat Jul 18 04:06:42 2026
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: daily_intakes
CREATE TABLE IF NOT EXISTS "daily_intakes" (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL, intake_date TEXT NOT NULL, quantity REAL NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, username TEXT REFERENCES Users (username), FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE);
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (1, 5, '2026-06-28', 20.0, '2026-06-29 03:15:35', NULL);
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (2, 1, '2026-06-28', 100.0, '2026-06-29 03:16:47', NULL);
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (3, 6, '2026-06-28', 2000.0, '2026-06-29 03:19:59', NULL);
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (5, 8, '2026-06-29', 10.0, '2026-06-29 17:22:12', NULL);
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (6, 1, '2026-06-29', 10.0, '2026-06-29 17:22:30', NULL);
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (7, 7, '2026-06-29', 900.0, '2026-06-29 17:22:40', NULL);
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (8, 1, '2026-07-05', 10.0, '2026-07-06 02:19:50', NULL);
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (9, 9, '2026-07-06', 50.0, '2026-07-07 00:27:44', 'test1');
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (10, 1, '2026-07-06', 200.0, '2026-07-07 00:27:51', 'test1');
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (11, 9, '2026-07-07', 100.0, '2026-07-07 05:16:22', 'test1');
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (12, 8, '2026-07-07', 50.0, '2026-07-07 05:18:49', 'test1');
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (13, 7, '2026-07-06', 1000.0, '2026-07-07 05:22:22', 'test1');
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (14, 1, '2026-07-07', 500.0, '2026-07-07 05:23:38', 'test1');
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (15, 7, '2026-07-07', 1500.0, '2026-07-07 05:23:55', 'test1');
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (16, 12, '2026-07-12', 50.0, '2026-07-12 15:25:07', 'test1');
INSERT INTO daily_intakes (id, product_id, intake_date, quantity, created_at, username) VALUES (17, 10, '2026-07-16', 1.0, '2026-07-16 22:02:20', 'Jacqp');

-- Table: products
CREATE TABLE IF NOT EXISTS "products" (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, calories REAL NOT NULL DEFAULT 0, protein REAL NOT NULL DEFAULT 0, fat REAL NOT NULL DEFAULT 0, carbs REAL NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, created_by TEXT REFERENCES Users (username) ON DELETE CASCADE);
INSERT INTO products (id, name, calories, protein, fat, carbs, created_at, created_by) VALUES (1, 'Chicken Breast', 165.0, 31.0, 3.6, 0.0, '2026-06-29 03:08:51', NULL);
INSERT INTO products (id, name, calories, protein, fat, carbs, created_at, created_by) VALUES (3, 'Egg', 155.0, 13.0, 11.0, 1.1, '2026-06-29 03:08:51', NULL);
INSERT INTO products (id, name, calories, protein, fat, carbs, created_at, created_by) VALUES (7, 'Steak', 100.0, 25.0, 36.0, 999.0, '2026-06-29 05:31:49', NULL);
INSERT INTO products (id, name, calories, protein, fat, carbs, created_at, created_by) VALUES (8, 'Cupcake', 250.0, 0.0, 600.0, 9882.0, '2026-06-29 17:21:17', NULL);
INSERT INTO products (id, name, calories, protein, fat, carbs, created_at, created_by) VALUES (10, 'Brownie', 466.0, 6.2, 29.1, 50.2, '2026-07-07 05:29:42', 'test1');
INSERT INTO products (id, name, calories, protein, fat, carbs, created_at, created_by) VALUES (11, 'Noodles', 100.0, 5.0, 5.0, 5.0, '2026-07-07 06:12:47', 'test1');
INSERT INTO products (id, name, calories, protein, fat, carbs, created_at, created_by) VALUES (12, 'Cake', 400.0, 10.0, 10.0, 30.0, '2026-07-12 15:24:50', 'test1');

-- Table: settings
CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
INSERT INTO settings (key, value) VALUES ('daily_goal', '2000');

-- Table: Users
CREATE TABLE IF NOT EXISTS "Users" (username TEXT PRIMARY KEY UNIQUE NOT NULL, password TEXT NOT NULL, daily_goal TEXT NOT NULL DEFAULT (2000));
INSERT INTO Users (username, password, daily_goal) VALUES ('test', 'test', '2000');
INSERT INTO Users (username, password, daily_goal) VALUES ('newuser', 'd404559f602eab6fd602ac7680dacbfaadd13630335e951f097af3900e9de176b6db28512f2e000b9d04fba5133e8b1c6e8df59db3a8ab9d60be4b97cc9e81db', '2000');
INSERT INTO Users (username, password, daily_goal) VALUES ('test1', 'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff', '2500');
INSERT INTO Users (username, password, daily_goal) VALUES ('test2', 'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff', '2000');
INSERT INTO Users (username, password, daily_goal) VALUES ('newuser2', 'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff', '2000');
INSERT INTO Users (username, password, daily_goal) VALUES ('Jacqp', 'c979f225d8d0ab83bb2575fcb5de303337e192a044b3f4236493607f2e04706618a7f9e2ffe4d696ac7dbcacca003df985fe84264b316ad49dd589d3ed37b9d3', '2000');
INSERT INTO Users (username, password, daily_goal) VALUES ('caplucky94', '4b5237d0489e7e5b2926496ec7cc2bfb02a9f04823fce32e2e0ddb04e9570ce456a06fcffca99f0b066e63e5e00ba4e7550e4275937088c3f853f614536d5246', '2000');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
