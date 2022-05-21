from datetime import datetime

from tinkoff.invest import CandleInterval, Client, InstrumentIdType
from api_token import api_token

import pandas as pd


def get_candles_by_ticker(ticker, from_date, to_date):
    with Client(api_token) as client:
        figi = client.instruments.share_by(id_type=InstrumentIdType(2), class_code="SPBXM", id=ticker).instrument.figi
        prices = []
        for candle in client.get_all_candles(
            figi=figi,
            from_=from_date,
            to=to_date,
            interval=CandleInterval.CANDLE_INTERVAL_HOUR
        ):
            price = [
                candle.open.units + candle.open.nano / 1e9,
                candle.close.units + candle.close.nano / 1e9,
                candle.low.units + candle.low.nano / 1e9,
                candle.high.units + candle.high.nano / 1e9,
                candle.volume
            ]
            prices.append(price)
        
        return prices

def candles_to_csv(ticker, from_date, to_date):
    prices = get_candles_by_ticker(ticker, from_date, to_date)

    df = pd.DataFrame(prices, columns=['open', 'close', 'low', 'high', 'volume'])
    df.to_csv('candles/%s_candles.csv' % ticker)

if __name__ == "__main__":
    ticker = "AMD"
    prices = candles_to_csv(ticker, datetime(2021, 1, 1), datetime(2022, 1, 1))