from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, ROC
from pandas import DataFrame

class GrowthToProtectiveStrategy(Strategy):
    def __init__(self):
        self.assets = ["GROWTH_STOCKS", "VXUS", "GDX", "GDXU", "SLVP", "BONDS"]
        # Assuming 'GROWTH_STOCKS' is a placeholder for a selection of growth stocks.
        self.interval = "1day"

    @property
    def data(self):
        # This list should include any additional datasets you might need,
        # though for simplicity, it's left empty in this example.
        return []

    def run(self, data):
        # Assuming data contains daily OHLCV data for each asset
        allocations = {asset: 0 for asset in self.assets}
        market_trend = self.calculate_market_trend(data["ohlcv"])
        momentum = self.calculate_momentum(data["ohlcv"])

        if market_trend == "upward" and momentum > 0:
            allocations["GROWTH_STOCKS"] = 1.0  # All-in on growth stocks
        elif market_trend == "downward" and momentum <= 0:
            # Allocate defensively: 20% VXUS, 20% GDX, 20% GDXU, 20% SLVP, 20% BONDS
            allocations = {asset: 0.2 for asset in self.assets if asset != "GROWTH_STOCKS"}
        # If the trend or momentum is inconclusive, maintain a diversified stance
        else:
            allocations["GROWTH_STOCKS"] = 0.2
            allocations["VXUS"] = 0.16
            allocations["GDX"] = 0.16
            allocations["GDXU"] = 0.16
            allocations["SLVP"] = 0.16
            allocations["BONDS"] = 0.16

        return TargetAllocation(allocations)

    def calculate_market_trend(self, ohlc_data):
        emas = {ticker: EMA(ticker, ohlc_data, length=50) for ticker in self.assets}
        trends = {}
        for ticker, ticker_emas in emas.items():
            if len(ticker_emas) > 2:
                trends[ticker] = "upward" if ticker_emas[-1] > ticker_emas[-2] else "downward"

        # Simplistic approach to determine the overall market trend based on the majority
        trend_counts = DataFrame(list(trends.values())).value_counts()
        if trend_counts.get("upward", 0) > trend_counts.get("downward", 0):
            return "upward"
        else:
            return "downward"

    def calculate_momentum(self, ohlc_data, length=20):
        rocs = {ticker: ROC(ticker, ohlc_data, length=length)[-1] for ticker in self.assets}
        # Return the average ROC as a simple proxy for market momentum
        return sum(rocs.values()) / len(rocs.values())