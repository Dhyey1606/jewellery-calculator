# import requests
# from bs4 import BeautifulSoup
# import json

# CONFIG_FILE = "config.json"

# def fetch_gold_rate():
#     url = "https://www.angelone.in/gold-rates-today/gold-rate-in-ahmedabad"
#     headers = {"User-Agent": "Mozilla/5.0"}  # disguise as browser
#     response = requests.get(url, headers=headers)

#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch page: {response.status_code}")

#     soup = BeautifulSoup(response.text, "html.parser")

#     # Inspect page manually and update selector accordingly
#     # Example: if the rate is inside <span id="goldRate">
#     gold_element = soup.find("div", {"class": "_7_GedP"})
#     if not gold_element:
#         raise Exception("Could not find gold rate element on page")

#     rate_text = gold_element.get_text(strip=True)
#     rate = float(rate_text.replace(",", "").replace("₹", "").strip())
#     return rate

# def update_config():
#     try:
#         rate = fetch_gold_rate()
#         with open(CONFIG_FILE, "r") as f:
#             config = json.load(f)
#         config["gold_rate"] = rate
#         with open(CONFIG_FILE, "w") as f:
#             json.dump(config, f, indent=4)
#         print(f"Updated gold_rate in config.json → {rate}")
#     except Exception as e:
#         print(f"Error updating gold rate: {e}")

# if __name__ == "__main__":
#     update_config()

    
import requests
from bs4 import BeautifulSoup
import json

CONFIG_FILE = "config.json"

def fetch_gold_rate():
    url = "https://www.angelone.in/gold-rates-today/gold-rate-in-ahmedabad"
    headers = {"User-Agent": "Mozilla/5.0"}  # disguise as browser
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    gold_element = soup.find("div", {"class": "_7_GedP"})
    if not gold_element:
        raise Exception("Could not find gold rate element on page")

    rate_text = gold_element.get_text(strip=True)
    rate_for_10g = float(rate_text.replace(",", "").replace("₹", "").strip())
    rate_per_gram = rate_for_10g / 10  # convert to per gram
    return rate_per_gram

def update_config():
    try:
        rate = fetch_gold_rate()
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        config["gold_rate"] = rate
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        print(f"Updated gold_rate in config.json → {rate} per gram")
    except Exception as e:
        print(f"Error updating gold rate: {e}")

if __name__ == "__main__":
    update_config()
