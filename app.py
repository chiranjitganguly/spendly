import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, verify_user

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        flash("All fields are required.")
        return render_template("register.html")

    if "@" not in email:
        flash("Enter a valid email address.")
        return render_template("register.html")

    if len(password) < 8:
        flash("Password must be at least 8 characters.")
        return render_template("register.html")

    if password != confirm_password:
        flash("Passwords do not match.")
        return render_template("register.html")

    try:
        create_user(name, email, password)
    except sqlite3.IntegrityError:
        flash("An account with that email already exists.")
        return render_template("register.html")

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Email and password are required.")
        return render_template("login.html")

    user = verify_user(email, password)
    if user is None:
        flash("Invalid email or password.")
        return render_template("login.html")

    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "initials": "PS",
        "member_since": "January 2024",
    }
    stats = {
        "total_spent": "₹42,850",
        "transaction_count": 27,
        "top_category": "Food & Dining",
    }
    transactions = [
        {"date": "Apr 28, 2025", "description": "Zomato order",           "category": "Food & Dining", "amount": "₹340"},
        {"date": "Apr 25, 2025", "description": "Metro card recharge",    "category": "Transport",     "amount": "₹500"},
        {"date": "Apr 22, 2025", "description": "BookMyShow",             "category": "Entertainment", "amount": "₹850"},
        {"date": "Apr 19, 2025", "description": "Big Basket groceries",   "category": "Groceries",     "amount": "₹1,240"},
        {"date": "Apr 15, 2025", "description": "Electricity bill",       "category": "Utilities",     "amount": "₹2,100"},
    ]
    categories = [
        {"name": "Food & Dining", "amount": "₹14,200", "pct": 33},
        {"name": "Groceries",     "amount": "₹9,800",  "pct": 23},
        {"name": "Utilities",     "amount": "₹7,500",  "pct": 18},
        {"name": "Transport",     "amount": "₹5,350",  "pct": 12},
        {"name": "Entertainment", "amount": "₹6,000",  "pct": 14},
    ]
    return render_template("profile.html", user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
