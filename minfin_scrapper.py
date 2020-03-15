import requests
import math
from typing import Tuple

from lxml import html


BLACK_MARKET_KNOWN_CURRENCIES_URL = "https://minfin.com.ua/ua/currency/auction/{currency}/buy/lvov/?presort=rating&sort=time&order=desc"
CURRENCY_VALUE_XPATH = "//div[contains(@class, 'au-mid-buysell')]/text()"


class CurrencyScrapper:
    def get_usd_currency(self) -> Tuple[float, float]:
        resp = requests.get(
            BLACK_MARKET_KNOWN_CURRENCIES_URL.format(**{"currency": "usd"})
        )
        parsed_elemts = html.fromstring(resp.content).xpath(CURRENCY_VALUE_XPATH)
        buy_price = parsed_elemts[1].replace("грн", "").strip().replace(",", ".")
        sell_price = parsed_elemts[3].replace("грн", "").strip().replace(",", ".")
        return float(buy_price), float(sell_price)

