import alpaca_trade_api as tradeapi
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
import logging
import insiderapi
import json
from alpaca_trade_api.rest import APIError
import time
import os 
from dotenv import load_dotenv # Load environment variables from .env file

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

try:
    api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY,  base_url=BASE_URL, api_version='v2')
    account = api.get_account()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    def get_config_item(item):
        with open("config.json", "r+") as f:
            config_data = json.loads(f.read())
            f.close()
            return config_data[item]

    def log_bought_stock(stock, assetid):
         with open("assets.json", "r+") as f:
            config_data = json.loads(f.read())
            f.close()
            config_data["buy:" + str(assetid)] = json.dumps(stock)
         with open("assets.json", "w") as f:
            f.write(json.dumps(config_data))
            f.close()

    def buy_stocks():
        for i in range(int(get_config_item("amount_to_buy"))):
            trade = insiderapi.fetch()[i]
            amnt = int(int(get_config_item("money_amount")) / float((trade["cost"])))
            if amnt > 0:
                try:
                    order = api.submit_order(
                        symbol=trade["ticker"],
                        qty=amnt,  # fractional shares
                        side='sell',
                        type='market',
                        time_in_force='day',
                    )
                    print("Bought", order.qty, "shares of the asset:", order.asset_id, trade["ticker"], trade["owner"], trade["relationship"], "Originally created at:", trade["secform"])
                    log_bought_stock(trade, order.asset_id)
                except APIError as ex:
                    print("Exception: " + str(ex))
            else:
                print("Balance is too low for " + str(amnt) + " shares of stock: " + str(trade["ticker"]))

    def fetch_assets():
        assets = api.list_assets(status='active')
        for asset in assets:
            print(asset.id, asset.symbol)
        time.sleep(10)
        main_screen()

    def main_screen():
        if not (bool(get_config_item("autostart"))):
            key = input("""
            ██ ███    ██ ███████ ██ ██████  ███████     ████████ ██████   █████  ██████  ███████ ██████  
            ██ ████   ██ ██      ██ ██   ██ ██             ██    ██   ██ ██   ██ ██   ██ ██      ██   ██ 
            ██ ██ ██  ██ ███████ ██ ██   ██ █████          ██    ██████  ███████ ██   ██ █████   ██████  
            ██ ██  ██ ██      ██ ██ ██   ██ ██             ██    ██   ██ ██   ██ ██   ██ ██      ██   ██ 
            ██ ██   ████ ███████ ██ ██████  ███████        ██    ██   ██ ██   ██ ██████  ███████ ██   ██ 
                                                                                                        
                                                Type 1 to view your assets
                                                Type 2 to autobuy assets
                                                """)
            if key == "1":
                fetch_assets()
            elif key == "2":
                buy_stocks()
            else:
                print("The inputted option is not valid, please try again!")
                main_screen()
        else:
            buy_stocks()

    main_screen()
except Exception as ex:
    print("Exception encountered: " + str(ex))
