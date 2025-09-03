
# from flask import Flask, render_template, request
# import json
# import os

# app = Flask(__name__)

# # Load config.json
# CONFIG_FILE = "config.json"
# if not os.path.exists(CONFIG_FILE):
#     raise FileNotFoundError(f"{CONFIG_FILE} not found! Please create it.")

# with open(CONFIG_FILE, "r") as f:
#     config = json.load(f)

# # GOLD_RATE is now required to be present in config.json
# GOLD_RATE = config.get("gold_rate")
# if GOLD_RATE is None:
#     # Ask for manual input if not present
#     GOLD_RATE = float(input("Enter current gold rate per gram: "))
#     config["gold_rate"] = GOLD_RATE
#     with open(CONFIG_FILE, "w") as f:
#         json.dump(config, f, indent=4)

# # Diamond rates options (update later if needed)
# DIAMOND_RATES = {
#     "Family": 55000,
#     "Friends": 60000,
#     "Reference": 70000,
#     "Other": 75000,
#     "Manual": None  # will allow manual entry
# }

# LABOUR_CHARGE = 1500

# PURITY_MULTIPLIERS = {
#     "24K": 1.0,
#     "22K": 0.916,
#     "18K": 0.75,
#     "14K": 0.583
# }


# @app.route("/", methods=["GET", "POST"])
# def index():
#     total_price = None
#     gold_rate_per_gram = None
#     purity_selected = None
#     diamond_rate_selected = None
#     diamond_rate_manual = None

#     if request.method == "POST":
#         try:
#             weight = float(request.form.get("weight", 0))
#             purity_selected = request.form.get("purity", "24K")
#             diamond_carat = float(request.form.get("diamond_carat", 0))

#             # Handle diamond rate selection
#             diamond_rate_key = request.form.get("diamond_rate_option")
#             if diamond_rate_key == "Manual":
#                 diamond_rate_manual = float(request.form.get("diamond_rate_manual", 0))
#                 diamond_rate_selected = diamond_rate_manual
#             else:
#                 diamond_rate_selected = DIAMOND_RATES.get(diamond_rate_key, 0)

#             gold_rate_per_gram = GOLD_RATE * PURITY_MULTIPLIERS.get(purity_selected, 1.0)
#             gold_price = weight * gold_rate_per_gram
#             diamond_price = diamond_carat * diamond_rate_selected
#             total_price = gold_price + diamond_price + (LABOUR_CHARGE * weight)

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


# if __name__ == "__main__":
#     app.run(
#         host="0.0.0.0",                     # bind to all interfaces
#         port=int(os.environ.get("PORT", 5000)),  # use Render’s PORT or fallback 5000 locally
#         debug=True
#     )


from flask import Flask, render_template, request
import json
import os
import subprocess

app = Flask(__name__)

CONFIG_FILE = "config.json"
SECRET_KEY = "mysecret123"  # 🔒 keep safe

# Helper function to load config
def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found! Please create it.")
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


# Load gold rate on startup
config = load_config()
GOLD_RATE = config.get("gold_rate")
if GOLD_RATE is None:
    GOLD_RATE = float(input("Enter current gold rate per gram: "))
    config["gold_rate"] = GOLD_RATE
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


# Constants
DIAMOND_RATES = {
    "Family": 55000,
    "Friends": 60000,
    "Reference": 70000,
    "Other": 75000,
    "Manual": None
}
LABOUR_CHARGE = 1500
PURITY_MULTIPLIERS = {
    "24K": 1.0,
    "22K": 0.916,
    "18K": 0.75,
    "14K": 0.583
}


@app.route("/", methods=["GET", "POST"])
def index():
    total_price = None
    gold_rate_per_gram = None
    purity_selected = None
    diamond_rate_selected = None
    diamond_rate_manual = None

    if request.method == "POST":
        try:
            weight = float(request.form.get("weight", 0))
            purity_selected = request.form.get("purity", "24K")
            diamond_carat = float(request.form.get("diamond_carat", 0))

            diamond_rate_key = request.form.get("diamond_rate_option")
            if diamond_rate_key == "Manual":
                diamond_rate_manual = float(request.form.get("diamond_rate_manual", 0))
                diamond_rate_selected = diamond_rate_manual
            else:
                diamond_rate_selected = DIAMOND_RATES.get(diamond_rate_key, 0)

            gold_rate_per_gram = GOLD_RATE * PURITY_MULTIPLIERS.get(purity_selected, 1.0)
            gold_price = weight * gold_rate_per_gram
            diamond_price = diamond_carat * diamond_rate_selected
            total_price = gold_price + diamond_price + (LABOUR_CHARGE * weight)

        except Exception as e:
            total_price = f"Error: {str(e)}"

    return render_template(
        "index.html",
        purity_multipliers=PURITY_MULTIPLIERS,
        total_price=total_price,
        gold_rate=gold_rate_per_gram,
        purity=purity_selected,
        diamond_rates=DIAMOND_RATES,
        diamond_rate_selected=diamond_rate_selected
    )


# 🔹 New route to trigger update_rates.py (for cron-job.org)
@app.route("/update-rates")
def update_rates():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return "Unauthorized", 403

    try:
        # Run the update_rates.py script
        subprocess.run(["python", "update_rates.py"], check=True)

        # Reload config
        global GOLD_RATE
        config = load_config()
        GOLD_RATE = config.get("gold_rate", GOLD_RATE)

        return f"✅ Gold rate updated to ₹{GOLD_RATE}/gram", 200
    except Exception as e:
        return f"❌ Error updating rate: {e}", 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
