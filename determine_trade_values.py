"""
Parse the trades and determine value exchanged between parties.
"""
import dateutil.parser

XLM_PRICE_FILE = "xlm_prices.csv"
TRADES_FILE = "trades.csv"

prices = {}

with open(XLM_PRICE_FILE) as price_file:
    parsed_header = False
    for line in price_file.readlines():
        if not parsed_header:
            parsed_header = True
            continue

        parts = line.strip().split(",")
        prices[parts[0]] = float(parts[2])


with open("trade_values.csv", "w") as trade_values_file:
    trade_values_file.write("value\n")
    with open(TRADES_FILE) as trades_file:
        parsed_header = False
        for line in trades_file.readlines():
            if not parsed_header:
                parsed_header = True
                continue

            parts = line.strip().split(",")
            base_asset_code = parts[1]
            counter_asset_code = parts[3]
            if base_asset_code != "XLM" and counter_asset_code != "XLM":
                continue

            trade_time = dateutil.parser.isoparse(parts[0])
            trade_day = trade_time.strftime("%Y-%m-%d")
            xlm_traded = float(parts[2]) if base_asset_code == "XLM" else float(parts[4])
            trade_value = xlm_traded * prices[trade_day]
            trade_values_file.write("%f\n" % trade_value)
