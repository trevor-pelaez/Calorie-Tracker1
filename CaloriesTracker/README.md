# Calorie Tracker Lite

Calorie Tracker Lite is a lightweight calorie tracking web application. It lets a user log in with a created account, manage food products, record daily food intake, review calorie/macronutrient totals, and export a simple HTML report.

The project is intentionally simple to install and run. It uses a local SQLite database file instead of a separate database server.

## Technology Stack

- **Python**: programming language used for the application logic.
- **Flask**: lightweight Python web framework used for pages, routes, forms, sessions, and browser responses.
- **SQLite**: local file-based database used to store products, intake entries, and settings.
- **HTML/CSS/Jinja templates**: page structure, styling, and dynamic page rendering.

## What the App Does

The application supports the core workflow of a calorie tracker:

1. Log in with an account.
2. Add food products with nutrition values per 100 grams.
3. Log daily food intake by date and quantity.
4. View daily calorie, protein, fat, and carbohydrate totals.
5. Review weekly, monthly, or yearly summaries.
6. Export a simple HTML report.

## What Flask Does

Flask receives browser requests and connects each URL to a Python function in `app.py`.

Example:

- The browser opens `/products`.
- Flask runs the `products()` route function.
- The function loads product records from SQLite.
- Flask renders `templates/products.html` and sends the page back to the browser.

## What SQLite Does

SQLite stores the application data in one local file:

```text
calorietracker.db
```

The database file is created automatically when the app starts. No MySQL installation, server port, root password, or migration setup is required.

## Login

The app uses one fixed local login:

```text
Username: test
Password: test
```

There is no public registration system. This keeps the project focused on calorie tracking instead of account management. Login is handled with Flask sessions, which remember that the user is logged in while the browser session is active.

## Food/Product Tracking

The Products page lets the user add food items. Each product stores nutrition values per 100 grams:

- calories
- protein
- fat
- carbs

These records are saved in the `products` table.

## Daily Calorie Tracking

The Daily Intake page lets the user select a date, choose a food product, and enter the amount eaten in grams.

Each entry is saved in the `daily_intakes` table. The app calculates totals by multiplying each product's nutrition values by the quantity eaten.

Example:

```text
White Rice = 130 calories per 100g
Logged amount = 200g
Calories = 130 * 200 / 100 = 260
```

## Reports and Statistics

The Reports page summarizes calorie and macronutrient totals for:

- week
- month
- year

The app groups daily intake entries by date and adds calories, protein, fat, and carbs for the selected period.

## Main Files

```text
app.py                    Main Flask application, routes, SQLite logic, and calculations
requirements.txt          Python dependency list
START_APP.bat             One-click Windows startup script
RESET_DATABASE.bat        Deletes the local SQLite database file
START_APP.ps1             PowerShell startup script
static/style.css          CSS styling
templates/                HTML/Jinja page templates
docs/wireframe.svg        Basic project wireframe
docs/wireframe.png        PNG version of the wireframe
calorietracker.db         SQLite database file created automatically when the app runs
```

## Easiest Way to Run on Windows

Double-click:

```text
START_APP.bat
```

That script creates a virtual environment if needed, installs Flask, opens the browser, and starts the app.

## Manual Run Instructions

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open this in a browser:

```text
http://127.0.0.1:5000
```

Login with:

```text
test / test
```

## Application Architecture

```text
Browser → Flask Routes → SQLite Database → HTML Templates → Browser
```

## Lightweight Design

This version does not use:

- ASP.NET
- MySQL
- Entity Framework
- migrations
- external database server
- registration system

The result is a small project that is easier to install, run, test, and explain.
