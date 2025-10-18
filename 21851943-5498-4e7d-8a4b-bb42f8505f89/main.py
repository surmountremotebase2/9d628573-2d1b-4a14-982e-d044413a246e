from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define tickers for the ETFs we're interested in
        self.tech_etfs = ["TQQQ", "QQQM"]  # High-growth tech ETFs
        self.metal_etfs = ["GDX", "GDXJ", "SLVP"]  # Precious metals ETFs for hedging

    @property
    def interval(self):
        # Use daily data to assess longer-term trends
        return "1day"

    @property
    def assets(self):
        # Combine all ETFs we're tracking
        return self.tech_etfs + self.metal_etfs

    def run(self, data):
        # Allocate funds based on the current trend
        allocation = {}

        # Calculate the 50-day and 200-day EMA for each ETF
        for etf in self.assets:
            short_ema = EMA(etf, data["ohlcv"], length=50)
            long_ema = EMA(etf, data["ohlcv"], length=200)

            if short_ema[-1] > long_ema[-1]:
                # If the 50-day EMA is above the 200-day EMA, the trend is considered bullish
                if etf in self.tech_etfs:
                    allocation[etf] = 0.5 / len(self.tech_etfs)  # Allocate half of the portfolio to tech ETFs, evenly split
                else:
                    allocation[etf] = 0  # Do not allocate to metal ETFs in a bullish trend
            else:
                # If the 50-day EMA is below the 200-day EMA, the trend is considered bearish
                if etf in self.metal_etfs:
                    allocation[etf] = 0.5 / len(self.metal_etfs)  # Allocate half of the portfolio to metal ETFs, evenly split
                else:
                    allocation[etf] = 0  # Do not allocate to tech ETFs in a bearish trend

        return TargetAllocation(allocation)