from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Tickers for the traded ETFs
        self.tickers = ["TQQQ", "VXUS", "GDX", "GDXU", "SLVP"]

    @property
    def interval(self):
        # Using daily data for broad market trends
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        # Initialize zero allocation
        allocation_dict = {ticker: 0 for ticker in self.tickers}

        # Simplification: Assuming market downturn based on VXUS performance
        # Using a 50-day SMA as a trend indicator
        vxus_prices = [i['VXUS']['close'] for i in data['ohlcv']]
        vxus_sma50 = SMA("VXUS", data, 50)

        if len(vxus_prices) < 50:
            log("Not enough data for SMA50 calculation.")
            return TargetAllocation(allocation_dict)

        current_price = vxus_prices[-1]
        current_sma50 = vxus_sma50[-1]

        # Strategy Logic:
        # If VXUS is below its 50-day SMA, it may indicate a market downturn.
        # We then switch to Gold and Silver ETFs.
        # Otherwise, we allocate between TQQQ and VXUS based on the long-term growth perspective.
        if current_price < current_sma50:
            log("Market downturn detected, switching to Gold and Silver ETFs")
            allocation_dict["GDX"] = 0.4  # 40% to Gold ETF
            allocation_dict["GDXU"] = 0.3  # 30% to leveraged Gold ETF
            allocation_dict["SLVP"] = 0.3  # 30% to Silver ETF
        else:
            log("Market in normal condition, focusing on TQQQ and VXUS")
            allocation_dict["TQQQ"] = 0.5  # 50% to leveraged NASDAQ ETF
            allocation_dict["VXUS"] = 0.5  # 50% to global stock ETF

        return TargetAllocation(allocation_dict)