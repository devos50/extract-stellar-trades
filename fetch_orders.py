"""
Scrape orders published on the Stellar blockchain, in descending order.
"""
import os
from time import sleep

import requests

if not os.path.exists("current_url.txt"):
    print("current_url.txt does not exist!")
    exit(1)

addresses = {}
next_identity = 1

if os.path.exists("identities.csv"):
    with open("identities.csv") as identities_file:
        parsed_header = False
        for line in identities_file.readlines():
            if not parsed_header:
                parsed_header = True
                continue

            parts = line.strip().split(",")
            address_id = int(parts[0])
            addresses[parts[1]] = address_id
            if address_id >= next_identity:
                next_identity = address_id + 1

    print("Loaded %d identities..." % (next_identity - 1))

current_url = None
with open("current_url.txt") as url_file:
    current_url = url_file.read().strip()

print("URL: %s" % current_url)

if not os.path.exists("offers.csv"):
    with open("offers.csv", "w") as trades_file:
        trades_file.write("type,time,creator,selling_asset_type,buying_asset_type,amount,price,offer_id\n")

while True:
    print("Performing request to %s" % current_url)
    response = requests.get(current_url)
    if response.status_code != 200:
        print("Error while performing request: %s" % response.text)
        exit(1)

    json_response = response.json()
    with open("offers.csv", "a") as offers_file:
        num_offers = 0
        for operation in json_response["_embedded"]["records"]:
            if operation["type"] != "manage_buy_offer" and operation["type"] != "manage_sell_offer":
                continue

            selling_asset_type = operation["selling_asset_type"]
            buying_asset_type = operation["buying_asset_type"]

            if selling_asset_type == "native":
                selling_asset_code = "XLM"
            else:
                selling_asset_code = operation["selling_asset_code"]

            if buying_asset_type == "native":
                buying_asset_code = "XLM"
            else:
                buying_asset_code = operation["buying_asset_code"]

            amount = float(operation["amount"])
            price = float(operation["price"])
            creator_address = operation["source_account"]
            offer_id = int(operation["offer_id"])

            if creator_address not in addresses:
                addresses[creator_address] = next_identity
                with open("identities.csv", "a") as identities_file:
                    identities_file.write("%d,%s\n" % (next_identity, creator_address))
                    next_identity += 1

            order_type = "buy" if operation["type"] == "manage_buy_offer" else "sell"

            offers_file.write("%s,%s,%d,%s,%s,%f,%f,%d\n" % (order_type, operation["created_at"],
                                                             addresses[creator_address], selling_asset_type,
                                                             buying_asset_type, amount, price, offer_id))
            num_offers += 1

        print("Offers in this batch: %d" % num_offers)

    # Get the next URL
    next_url = json_response["_links"]["next"]["href"]
    with open("current_url.txt", "w") as url_file:
        url_file.write(next_url)
        current_url = next_url

    sleep(1)
