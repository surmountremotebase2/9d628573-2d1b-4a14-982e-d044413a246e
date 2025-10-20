from surmount.base_class import Strategy, TargetAllocation
from surmount.data import (
    Asset,
    CboeVolatilityIndexVix
)
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Tracking high momentum assets, VIX for market volatility
        self.tickers = ["TSLA", "AAPL", "NVDA", "AMD"]  # Example tech stocks known for high volatility and potential returns
        self.data_list = [CboeVolatilityIndexVix()]

    @property
    def interval(self):
        return "1day"  # Daily analysis

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        vix = data[("cboe_volatility_index_vix",)][-1]["value"]  # Get the latest VIX value
        
        # Lower allocations as VIX increases, suggesting higher market risk
        risk_modulation = max(0, 1 - vix / 40)  # Example modulation, assuming VIX higher than 40 is high risk

        for ticker in self.tickers:
            ohlcv = data["ohlcv"][ticker]
            macd = MACD(ticker, ohlcv, fast=12, slow=26)
            rsi = RSI(ticker, ohlcv, length=14)

            # Simplistic momentum investment when MACD positive and RSI not overbought
            if macd["MACD"][-1] > 0 and rsi[-1] < 70:
                allocation_dict[ticker] = risk_modulation * (1 / len(self.tickers))  # Evenly distribute available capital among tickers
            else:
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)