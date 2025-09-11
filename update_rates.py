
# import requests
# from bs4 import BeautifulSoup
# import psycopg2
# import os
# from datetime import datetime

# DATABASE_URL = os.environ.get("DATABASE_URL")

# def fetch_gold_rate():
#     url = "https://www.angelone.in/gold-rates-today/gold-rate-in-ahmedabad"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, "html.parser")
#     gold_element = soup.find("div", {"class": "_7_GedP"})
#     rate_text = gold_element.get_text(strip=True)
#     rate_for_10g = float(rate_text.replace(",", "").replace("₹", "").strip())
#     return rate_for_10g / 10

# def update_database():
#     rate = fetch_gold_rate()
#     conn = psycopg2.connect(DATABASE_URL)
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO gold_rates (id, rate, updated_at)
#         VALUES (1, %s, %s)
#         ON CONFLICT (id) DO UPDATE
#         SET rate = EXCLUDED.rate,
#             updated_at = EXCLUDED.updated_at
#     """, (rate, datetime.now()))
#     conn.commit()
#     cur.close()
#     conn.close()
#     print(f"✅ Updated gold_rate → {rate}")

# if __name__ == "__main__":
#     update_database()


# update_rates.py
import requests
import re
import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

def fetch_gold_rate():
    url = "https://bcast.arhambullion.in:7768/VOTSBroadcastStreaming/Services/xml/GetLiveRateByTemplateID/arham"
    response = requests.get(url, verify=False, timeout=10)  # disable SSL verify if needed
    data = response.text

    # Find the row containing "GOLD 999 IMP"
    for line in data.splitlines():
        if "GOLD 999 IMP" in line:
            parts = line.split()
            # `parts[8]` is the value you tested
            return float(parts[8])

    raise ValueError("Could not find GOLD 999 IMP value in response")

def save_rate_to_db(rate):
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    cur.execute("INSERT INTO gold_rates (rate) VALUES (%s)", (rate,))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    rate = fetch_gold_rate()
    save_rate_to_db(rate)
    print(f"✅ Saved new GOLD 999 IMP rate: {rate}")
