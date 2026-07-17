"""
Calories Tracker Lite
---------------------
Small Flask + SQLite web application for tracking food intake and daily calories.

Design goals:
- Registration for multiple users.
- Local SQLite database file created by the app
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from functools import wraps
import hashlib
from pathlib import Path
import sqlite3
from typing import Any
from User import *
from FemaleUser import *
from MaleUser import *
import os



from flask import Flask, Response, flash, g, redirect, render_template, request, session, url_for

# -----------------------------------------------------------------------------
# Basic application setup
# -----------------------------------------------------------------------------

# APP_DIR points to the folder where this app.py file lives.
# This keeps file paths stable even if the app is launched from PowerShell.
APP_DIR = Path(__file__).resolve().parent

# SQLite stores all data in one local file. If the file does not exist,
# init_db() creates it when the app starts.
DB_PATH = Path(os.environ.get("DB_PATH", "/tmp/calorietracker.db"))

# Flask is the lightweight web framework that handles routes, templates,
# browser requests, and browser responses.
app = Flask(__name__)

# Flask sessions need a secret key. This local project uses a static value for simplicity.
# In a real public app, this should be a private environment variable.
app.secret_key = "local-calorie-tracker-key"

# Fixed local login.
DEMO_USERNAME = "test"
DEMO_PASSWORD = "test"


# -----------------------------------------------------------------------------
# Database helper functions
# -----------------------------------------------------------------------------

def get_db() -> sqlite3.Connection:
    """Return the current request's SQLite database connection.

    Flask's g object stores data for the current request only. This prevents the
    app from opening a new database connection every time a query runs.
    """
    if "db" not in g:
        # Open the local SQLite database file.
        conn = sqlite3.connect(DB_PATH)


        # This lets rows behave like dictionaries, so templates can use row.name
        # instead of remembering column positions like row[0].
        conn.row_factory = sqlite3.Row

        # Save the connection for the rest of this web request.
        g.db = conn

    return g.db


@app.teardown_appcontext
def close_db(_error: Exception | None = None) -> None:
    """Close the SQLite connection at the end of each request.

    This is basic cleanup. It prevents database connections from staying open
    after Flask finishes sending the page back to the browser.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db() -> None:
    """Create the SQLite tables and starter data.

    This function runs when the app starts. It creates tables only if they do
    not already exist, so it is safe to run multiple times.
    """
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")

    # products stores food items and nutrition values per 100 grams.
    # daily_intakes stores each food entry logged for a date.
    # settings stores simple key/value app settings like the calorie goal.
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            calories REAL NOT NULL DEFAULT 0,
            protein REAL NOT NULL DEFAULT 0,
            fat REAL NOT NULL DEFAULT 0,
            carbs REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES Users(username) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS daily_intakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            intake_date TEXT NOT NULL,
            quantity REAL NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS Users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            daily_goal INTEGER NOT NULL DEFAULT 2000
        );
        
        """
    )

    # Add sample food products only if the product table is empty.
    product_count = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]

    if product_count == 0:
        db.executemany(
            "INSERT INTO products (name, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?)",
            [
                ("Chicken Breast", 165, 31, 3.6, 0),
                ("White Rice", 130, 2.7, 0.3, 28),
                ("Egg", 155, 13, 11, 1.1),
                ("Greek Yogurt", 59, 10, 0.4, 3.6),
            ],
        )


    db.commit()
    db.close()


# -----------------------------------------------------------------------------
# Login and shared utility helpers
# -----------------------------------------------------------------------------

def login_required(view):
    """Protect a route so only logged-in users can access it.

    This is a small custom replacement for a full authentication package.
    It checks the Flask session for logged_in = True.
    """
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # If the user is not logged in, send them to the login page.
        if not session.get("logged_in"):
            return redirect(url_for("login"))

        # If logged in, allow the original page function to run.
        return view(*args, **kwargs)

    return wrapped_view


def get_daily_goal() -> int:
    """Read the daily calorie goal from the users table."""
    row = get_db().execute("SELECT daily_goal FROM Users WHERE username = ?",(session["username"],)).fetchone()

    # If the setting is missing or invalid, use a safe default.
    if not row:
        return 2000

    try:
        return int(float(row["daily_goal"]))
    except ValueError:
        return 2000


def set_daily_goal(goal: int) -> None:
    """Save the user's daily calorie goal """
    # Update the daily_goal value in the Users table for the current user.
    get_db().execute(
        "UPDATE Users SET daily_goal = ? WHERE username = ?",(str(goal), session["username"]),
    )
    get_db().commit()


def parse_date(value: str | None, fallback: date) -> date:
    """Convert a form/query date string into a Python date.

    Browser date inputs send dates as YYYY-MM-DD. If the value is missing or
    invalid, the app uses the fallback date instead.
    """
    if not value:
        return fallback

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return fallback


def totals_for_range(start: date, end: date) -> list[dict[str, Any]]:
    """Return calorie and macro totals grouped by date.

    This is used by the dashboard and reports pages. The SQL joins daily_intakes
    to products so the app can calculate nutrition from product values.
    """
    rows = get_db().execute(
        """
        SELECT
            d.intake_date,
            SUM(p.calories * d.quantity / 100.0) AS calories,
            SUM(p.protein * d.quantity / 100.0) AS protein,
            SUM(p.fat * d.quantity / 100.0) AS fat,
            SUM(p.carbs * d.quantity / 100.0) AS carbs
        FROM daily_intakes d
        JOIN products p ON p.id = d.product_id
        WHERE d.intake_date BETWEEN ? AND ? 
            AND d.username = ?
        GROUP BY d.intake_date
        ORDER BY d.intake_date
        """,
        (start.isoformat(), end.isoformat(), session["username"]),
    ).fetchall()

    return [dict(row) for row in rows]


def day_summary(selected_date: date) -> dict[str, Any]:
    """Calculate total calories, protein, fat, and carbs for one day."""
    row = get_db().execute(
        """
        SELECT
            COALESCE(SUM(p.calories * d.quantity / 100.0), 0) AS calories,
            COALESCE(SUM(p.protein * d.quantity / 100.0), 0) AS protein,
            COALESCE(SUM(p.fat * d.quantity / 100.0), 0) AS fat,
            COALESCE(SUM(p.carbs * d.quantity / 100.0), 0) AS carbs
        FROM daily_intakes d
        JOIN products p ON p.id = d.product_id
        WHERE d.intake_date = ? 
            AND d.username = ?
        """,
        (selected_date.isoformat(), session["username"]),
    ).fetchone()

    return dict(row)


# -----------------------------------------------------------------------------
# Web routes
# Each route connects a browser URL to a Python function.
# -----------------------------------------------------------------------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = get_db()
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        existing = get_db().execute("SELECT username FROM Users WHERE username = ?", (username,)).fetchone()

        # Basic data validation
        if not username or not password:
            flash("Plese create a username and password.", "error")
            return redirect(url_for("signup"))
        
        
        elif existing is not None:
            if username == existing[0]:
                flash("Username already exists!", "error")
                return redirect(url_for('signup'))

        # Secure password hashing before saving
        else:
            hashed_password = hashlib.sha512(password.encode()).hexdigest()
            db.execute(
                "INSERT INTO Users (username, password) VALUES (?, ?)",(username, hashed_password),
            )
            db.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


#Method for logging in users. Checks if the username and password match the database and logs in if true.
@app.route("/login", methods=["GET", "POST"])
def login():
    """Show the login form and process login attempts."""
    if request.method == "POST":
        # Read username/password values submitted by the login form.
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        password = hashlib.sha512(password.encode()).hexdigest()
        currentUser = get_db().execute("SELECT username FROM Users WHERE username = ?", (username,)).fetchone()
        currentPassword = get_db().execute("SELECT password FROM Users WHERE username = ?", (username,)).fetchone()
 
        # Checks if user and password are registered and logs in if true.
        if username == currentUser[0] and password == currentPassword[0]:
            session.clear()
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clear the session and return to the login page."""
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    """Show today's totals and a simple seven-day history."""
    today = date.today()

    # Summary of today's logged food.
    summary = day_summary(today)

    # Daily goal is stored in the settings table.
    goal = get_daily_goal()

    # Used by the progress bar on the dashboard.
    percent = min(100, round((summary["calories"] / goal) * 100, 1)) if goal else 0

    # Seven-day totals for a simple recent activity table.
    recent = totals_for_range(today - timedelta(days=6), today)

    return render_template(
        "dashboard.html",
        summary=summary,
        goal=goal,
        percent=percent,
        recent=recent,
        today=today,
    )


@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    """List food products and allow the user to add new products."""
    db = get_db()

    if request.method == "POST":
        # Read the add-product form values.
        name = request.form.get("name", "").strip()

        try:
            # Nutrition values are stored per 100 grams.
            calories = float(request.form.get("calories", 0) or 0)
            protein = float(request.form.get("protein", 0) or 0)
            fat = float(request.form.get("fat", 0) or 0)
            carbs = float(request.form.get("carbs", 0) or 0)
        except ValueError:
            flash("Nutrition values must be numbers.", "error")
            return redirect(url_for("products"))

        if not name:
            flash("Product name is required.", "error")
        else:
            try:
                # Save the new food product to SQLite.
                db.execute(
                    "INSERT INTO products (name, calories, protein, fat, carbs, created_by) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, calories, protein, fat, carbs, session["username"]),
                )
                db.commit()
                flash("Product added.", "success")
            except sqlite3.IntegrityError:
                # Product names are unique, so duplicate names are blocked.
                flash("A product with that name already exists.", "error")

        return redirect(url_for("products"))

    # GET request: show all products alphabetically.
    rows = db.execute("SELECT * FROM products WHERE created_by = ? OR created_by IS NULL ORDER BY name", (session["username"],)).fetchall()
    return render_template("products.html", products=rows)


@app.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id: int):
    """Delete a product by id."""
    get_db().execute("DELETE FROM products WHERE id = ?", (product_id,))
    get_db().commit()
    flash("Product deleted.", "success")
    return redirect(url_for("products"))

@app.route("/products/<int:product_id>/update", methods=["POST"])
@login_required
def update_product(product_id: int):
    """Updates a product by id."""
    get_db().execute("UPDATE products SET  WHERE id = ?", (product_id,))
    get_db().commit()
    flash("Product deleted.", "success")
    return redirect(url_for("products"))


@app.route("/intake", methods=["GET", "POST"])
@login_required
def intake():
    """Show and update food entries for a selected day."""
    selected_date = parse_date(request.values.get("date"), date.today())
    db = get_db()

    if request.method == "POST":
        try:
            # The form sends the selected product id and quantity in grams.
            product_id = int(request.form.get("product_id", "0"))
            quantity = float(request.form.get("quantity", "0"))
        except ValueError:
            flash("Select a product and enter a valid quantity.", "error")
            return redirect(url_for("intake", date=selected_date.isoformat()))

        if product_id <= 0 or quantity <= 0:
            flash("Select a product and enter a quantity above zero.", "error")
        else:
            # Save one logged food entry for the selected date.
            db.execute(
                "INSERT INTO daily_intakes (product_id, intake_date, quantity, username) VALUES (?, ?, ?, ?)",
                (product_id, selected_date.isoformat(), quantity, session["username"]),
            )
            db.commit()
            flash("Food logged.", "success")

        return redirect(url_for("intake", date=selected_date.isoformat()))

    # Data needed to render the Daily Intake page.
    products = db.execute("SELECT * FROM products ORDER BY name").fetchall()

    # This query calculates nutrition for each logged entry.
    entries = db.execute(
        """
        SELECT
            d.id,
            d.quantity,
            p.name,
            p.calories * d.quantity / 100.0 AS calories,
            p.protein * d.quantity / 100.0 AS protein,
            p.fat * d.quantity / 100.0 AS fat,
            p.carbs * d.quantity / 100.0 AS carbs
        FROM daily_intakes d
        JOIN products p ON p.id = d.product_id
        WHERE d.intake_date = ?
        ORDER BY d.created_at DESC
        """,
        (selected_date.isoformat(),),
    ).fetchall()

    summary = day_summary(selected_date)

    return render_template(
        "intake.html",
        products=products,
        entries=entries,
        summary=summary,
        selected_date=selected_date,
    )


@app.route("/intake/<int:intake_id>/delete", methods=["POST"])
@login_required
def delete_intake(intake_id: int):
    """Remove one logged food entry from the selected date."""
    selected_date = parse_date(request.form.get("date"), date.today())
    get_db().execute("DELETE FROM daily_intakes WHERE id = ?", (intake_id,))
    get_db().commit()
    flash("Entry removed.", "success")
    return redirect(url_for("intake", date=selected_date.isoformat()))


@app.route("/reports")
@login_required
def reports():
    """Show totals for week, month, or year."""
    today = date.today()
    period = request.args.get("period", "week")

    # Choose the report date range based on the URL query string.
    if period == "month":
        start = today - timedelta(days=29)
    elif period == "year":
        start = today - timedelta(days=364)
    else:
        start = today - timedelta(days=6)
        period = "week"

    end = today
    rows = totals_for_range(start, end)

    # Add up all daily rows to show period totals.
    totals = {
        "calories": sum(r["calories"] or 0 for r in rows),
        "protein": sum(r["protein"] or 0 for r in rows),
        "fat": sum(r["fat"] or 0 for r in rows),
        "carbs": sum(r["carbs"] or 0 for r in rows),
    }

    return render_template("reports.html", period=period, rows=rows, totals=totals, start=start, end=end)


@app.route("/reports/export")
@login_required
def export_report():
    """Download a simple HTML report for the last seven days."""
    today = date.today()
    rows = totals_for_range(today - timedelta(days=6), today)

    # Build HTML table rows from the report data.
    html_rows = "".join(
        f"<tr><td>{r['intake_date']}</td><td>{r['calories']:.1f}</td>"
        f"<td>{r['protein']:.1f}</td><td>{r['fat']:.1f}</td><td>{r['carbs']:.1f}</td></tr>"
        for r in rows
    )

    html = f"""
    <!doctype html>
    <html><head><meta charset='utf-8'><title>Calories Tracker Report</title></head>
    <body>
      <h1>Calories Tracker - 7 Day Report</h1>
      <table border='1' cellpadding='8' cellspacing='0'>
        <thead><tr><th>Date</th><th>Calories</th><th>Protein</th><th>Fat</th><th>Carbs</th></tr></thead>
        <tbody>{html_rows}</tbody>
      </table>
    </body></html>
    """

    # Response returns downloadable HTML instead of a normal web page.
    return Response(
        html,
        mimetype="text/html",
        headers={"Content-Disposition": "attachment; filename=calorie-report.html"},
    )


@app.route("/calculator", methods=["GET", "POST"])
@login_required
def calculator():
    """Estimate calorie targets using a simple BMR/TDEE calculator."""
    result = None
    user_male = MaleUser(0, 0, 0, 0)
    user_female = FemaleUser(0, 0, 0, 0)
    if request.method == "POST":
        try:
            weight = float(request.form.get("weight", "0"))
            height = float(request.form.get("height", "0"))
            age = int(request.form.get("age", "0"))
            gender = request.form.get("gender", "male")
            activity = float(request.form.get("activity", "1.2"))

            # Basic Mifflin-St Jeor BMR estimate.
            if gender == "female":
                user_female = FemaleUser(age, weight, height, activity)
                user_female.BMIcalculator()
                result = user_female.get_bmi()
            else:
                user_male = MaleUser(age, weight, height, activity)
                user_male.BMIcalculator()
                result = user_male.get_bmi()
            
        except ValueError:
            flash("Enter valid calculator numbers.", "error")
    

    return render_template("calculator.html", result=result)



@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Show and update the daily calorie goal."""
    if request.method == "POST":
        try:
            goal = int(float(request.form.get("daily_goal", "2000")))

            # Very low calorie goals are rejected as invalid input.
            if goal < 500:
                raise ValueError

            set_daily_goal(goal)
            flash("Daily goal saved.", "success")
        except ValueError:
            flash("Enter a valid daily calorie goal.", "error")

        return redirect(url_for("settings"))

    return render_template("settings.html", goal=get_daily_goal())


# This block only runs when starting the app directly with: python app.py


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    


