"""
Scrape orders published on the Stellar blockchain.
"""
import os
from time import sleep

import requests

if not os.path.exists("current_url.txt"):
    print("current_url.txt does not exist!")
    exit(1)

current_url = None
with open("current_url.txt") as url_file:
    current_url = url_file.read().strip()

print("URL: %s" % current_url)

if not os.path.exists("trades.csv"):
    with open("trades.csv", "w") as trades_file:
        trades_file.write("time,base_asset_code,base_amount,counter_asset_code,counter_amount,base_account,counter_account\n")

while True:
    print("Performing request to %s" % current_url)
    response = requests.get(current_url)
    if response.status_code != 200:
        print("Error while performing request: %s" % response.text)
        exit(1)

    json_response = response.json()

    # Parse trades
    with open("trades.csv", "a") as trades_file:
        for trade in json_response["_embedded"]["records"]:
            base_asset_type = trade["base_asset_type"]
            counter_asset_type = trade["counter_asset_type"]
            base_amount = trade["base_amount"]
            counter_amount = trade["counter_amount"]

            if base_asset_type == "native":
                base_asset_code = "XLM"
            else:
                base_asset_code = trade["base_asset_code"]

            if counter_asset_type == "native":
                counter_asset_code = "XLM"
            else:
                counter_asset_code = trade["counter_asset_code"]

            trades_file.write("%s,%s,%s,%s,%s,%s,%s\n" % (trade["ledger_close_time"], base_asset_code, base_amount, counter_asset_code, counter_amount, trade["base_account"], trade["counter_account"]))

    # Get the next URL
    next_url = json_response["_links"]["next"]["href"]
    with open("current_url.txt", "w") as url_file:
        url_file.write(next_url)
        current_url = next_url

    sleep(1)
