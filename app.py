
# from flask import Flask, render_template, request
# import os
# import subprocess
# import sqlite3
# import sys
# from db import init_db, get_connection

# # init db on app start
# init_db()

# app = Flask(__name__)
# SECRET_KEY = "mysecret123"  # 🔒 keep safe
# DB_FILE = "gold_rates.db"

# # Fetch latest gold rate from DB
# def get_latest_gold_rate():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT rate FROM gold_rates ORDER BY updated_at DESC LIMIT 1")
#     row = cur.fetchone()
#     conn.close()
#     return float(row[0]) if row else None


# # Constants
# DIAMOND_RATES = {
#     "Family": 65000,
#     "Friends": 70000,
#     "Reference": 75000,
#     "Other": 80000,
#     "Manual": None
# }
# LABOUR_CHARGE = 1500
# PURITY_MULTIPLIERS = {
#     "24K": 1.0,
#     "22K": 0.916,
#     "18K": 0.76,
#     "14K": 0.60
# }


# @app.route("/", methods=["GET", "POST"])
# def index():
#     total_price = None
#     gold_rate_per_gram = None
#     purity_selected = None
#     diamond_rate_selected = None
#     diamond_rate_manual = None

#     GOLD_RATE = get_latest_gold_rate()

#     if request.method == "POST" and GOLD_RATE:
#         try:
#             weight = float(request.form.get("weight", 0))
#             purity_selected = request.form.get("purity", "24K")
#             diamond_carat = float(request.form.get("diamond_carat", 0))

#             diamond_rate_key = request.form.get("diamond_rate_option")
#             if diamond_rate_key == "Manual":
#                 diamond_rate_manual = float(request.form.get("diamond_rate_manual", 0))
#                 diamond_rate_selected = diamond_rate_manual
#             else:
#                 diamond_rate_selected = DIAMOND_RATES.get(diamond_rate_key, 0)

#             # Round to 2 decimals at calculation stage
#             gold_rate_per_gram = round(GOLD_RATE * PURITY_MULTIPLIERS.get(purity_selected, 1.0), 2)
#             gold_price = round(weight * gold_rate_per_gram, 2)
#             diamond_price = round(diamond_carat * diamond_rate_selected, 2)
#             total_price = round(gold_price + diamond_price + (LABOUR_CHARGE * weight), 2)

#         except Exception as e:
#             total_price = f"Error: {str(e)}"

#     return render_template(
#         "index.html",
#         purity_multipliers=PURITY_MULTIPLIERS,
#         total_price=total_price,
#         gold_rate=gold_rate_per_gram,
#         purity=purity_selected,
#         diamond_rates=DIAMOND_RATES,
#         diamond_rate_selected=diamond_rate_selected
#     )


# # 🔹 Cron trigger
# @app.route("/update-rates")
# def update_rates():
#     key = request.args.get("key")
#     if key != SECRET_KEY:
#         return "Unauthorized", 403

#     try:
#         subprocess.run([sys.executable, "update_rates.py"], check=True)
#         new_rate = get_latest_gold_rate()
#         return f"✅ Gold rate updated to ₹{new_rate:.2f}/gram", 200
#     except Exception as e:
#         return f"❌ Error updating rate: {e}", 500


# @app.route("/debug-db")
# def debug_db():
#     try:
#         import psycopg2
#         conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM gold_rates ORDER BY updated_at DESC LIMIT 5;")
#         rows = cur.fetchall()
#         cur.close()
#         conn.close()
#         return {"rows": rows}
#     except Exception as e:
#         return {"error": str(e)}


# if __name__ == "__main__":
#     app.run(
#         host="0.0.0.0",
#         port=int(os.environ.get("PORT", 5000)),
#         debug=True
#     )


from flask import Flask, render_template, request
import os
import subprocess
import sqlite3
import sys
from db import init_db, get_connection

# init db on app start
init_db()

app = Flask(__name__)
SECRET_KEY = "mysecret123"  # 🔒 keep safe
DB_FILE = "gold_rates.db"

# Fetch latest gold rate from DB
def get_latest_gold_rate():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT rate FROM gold_rates ORDER BY updated_at DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return float(row[0]) if row else None


# Constants
DIAMOND_RATES = {
    "Family": 65000,
    "Friends": 70000,
    "Reference": 75000,
    "Other": 80000,
    "Manual": None
}
LABOUR_CHARGE = 1500
PURITY_MULTIPLIERS = {
    "24K": 1.0,
    "22K": 0.916,
    "18K": 0.76,
    "14K": 0.60
}


@app.route("/", methods=["GET", "POST"])
def index():
    total_price = None
    gold_rate_per_gram = None
    purity_selected = request.form.get("purity") if request.method == "POST" else None
    diamond_rate_option = request.form.get("diamond_rate_option") if request.method == "POST" else None
    diamond_rate_used = None
    diamond_carat = 0
    weight = 0

    latest_gold_rate = get_latest_gold_rate()

    if request.method == "POST" and latest_gold_rate:
        try:
            weight = float(request.form.get("weight", 0))
            purity_selected = request.form.get("purity", "24K")
            diamond_carat = float(request.form.get("diamond_carat", 0))

            # Diamond rate selection
            if diamond_rate_option == "Manual":
                diamond_rate_used = float(request.form.get("diamond_rate_manual", 0))
            else:
                diamond_rate_used = DIAMOND_RATES.get(diamond_rate_option, 0)

            # Calculate prices
            gold_rate_per_gram = round(latest_gold_rate * PURITY_MULTIPLIERS.get(purity_selected, 1.0), 2)
            gold_price = round(weight * gold_rate_per_gram, 2)
            diamond_price = round(diamond_carat * diamond_rate_used, 2)
            labour_price = round(LABOUR_CHARGE * weight, 2)

            total_price = round(gold_price + diamond_price + labour_price, 2)

        except Exception as e:
            total_price = None
            print("❌ Error in calculation:", e)

    return render_template(
        "index.html",
        purity_multipliers=PURITY_MULTIPLIERS,
        total_price=total_price,
        latest_gold_rate=latest_gold_rate,
        gold_rate=gold_rate_per_gram,
        purity=purity_selected,
        diamond_rates=DIAMOND_RATES,
        diamond_rate_option=diamond_rate_option,
        diamond_rate=diamond_rate_used,
        diamond_carat=diamond_carat,
        labour_charge=LABOUR_CHARGE,
        weight=weight
    )


# 🔹 Cron trigger
@app.route("/update-rates")
def update_rates():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return "Unauthorized", 403

    try:
        subprocess.run([sys.executable, "update_rates.py"], check=True)
        new_rate = get_latest_gold_rate()
        return f"✅ Gold rate updated to ₹{new_rate:.2f}/gram", 200
    except Exception as e:
        return f"❌ Error updating rate: {e}", 500


@app.route("/debug-db")
def debug_db():
    try:
        import psycopg2
        conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_rates ORDER BY updated_at DESC LIMIT 5;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"rows": rows}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
