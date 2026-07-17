# Code Walkthrough

This file explains the main code structure and how each section works.

## `app.py`

`app.py` is the main application file. It contains the Flask setup, SQLite setup, helper functions, and route functions.

### Application Setup

The top of the file imports the modules needed by the app. It creates a Flask app object and sets the SQLite database path.

### Database Setup

`init_db()` creates four tables:

1. `products` stores food products and nutrition values.
2. `daily_intakes` stores logged food entries by date.
3. `settings` stores the user's daily calorie goal.
4. `users` stores registration info for users to signup and login with

The database is stored locally in `calorietracker.db`.

### Login Helper

`login_required()` protects pages so they cannot be opened unless the user is logged in.


### Dashboard Route

The dashboard route loads today's calorie summary, the daily goal, and the last seven days of totals.

### Products Route

The products route has two jobs:

- `GET`: show the products table.
- `POST`: save a new product from the form.

### Daily Intake Route

The daily intake route lets the user pick a date, log food in grams, and view totals for that date.

### Reports Route

The reports route calculates totals for week, month, or year.

### Export Route

The export route generates a simple HTML file with the last seven days of report data.

### Calculator Route

The calculator route estimates maintenance calories using a basic BMR formula.

### Settings Route

The settings route lets the user save a daily calorie goal.

## Templates

Templates are HTML files with Jinja syntax. Flask fills them with live data from Python.

Example:

```html
{{ goal }}
```

That means Flask will replace `{{ goal }}` with the actual goal value from the database.

## CSS

`static/style.css` controls how the app looks. It handles the sidebar, cards, forms, tables, buttons, flash messages, and mobile layout.

## Startup Scripts

`START_APP.bat` is the easiest Windows launcher. It creates a virtual environment if one does not exist, installs the required Python package, opens the browser, and runs the app.

`RESET_DATABASE.bat` deletes `calorietracker.db`. The next time the app starts, the database and sample data are recreated.
