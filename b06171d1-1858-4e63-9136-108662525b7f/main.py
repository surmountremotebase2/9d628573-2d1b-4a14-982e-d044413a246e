from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers for both sets of assets
        self.growth_tickers = ["TQQQ", "KORU"]
        self.safe_tickers = ["GDX", "GDXJ", "SLVP"]
        self.bond_ticker = ["BND"]  # An example bond ETF
        # Choose an example ticker for market trends observation (e.g., SPY for S&P 500)
        self.market_trend_ticker = "SPY"

    @property
    def assets(self):
        # Combine all assets
        return self.growth_tickers + self.safe_tickers + self.bond_ticker

    @property
    def interval(self):
        # Daily interval for trend analysis
        return "1day"

    def run(self, data):
        # Initialize allocations with 0 and update based on the trend
        allocation_dict = {ticker: 0 for ticker in self.assets}
        
        # Calculate short term and long term SMAs for the market trend ticker
        short_term_sma = SMA(self.market_trend_ticker, data, 10)
        long_term_sma = SMA(self.market_trend_ticker, data, 50)

        if short_term_sma[-1] > long_term_sma[-1]:
            # Bullish trend, allocate to growth assets
            allocation_per_ticker = 1 / len(self.growth_tickers)
            for ticker in self.growth_tickers:
                allocation_dict[ticker] = allocation_per_ticker
        else:
            # Bearish or uncertain trend, allocate to safe-haven assets equally
            allocation_to_safe_assets = 0.5 / len(self.safe_tickers)  # Split a part for precious metals
            for ticker in self.safe_tickers:
                allocation_dict[ticker] = allocation_to_safe_assets
            allocation_dict[self.bond_ticker[0]] = 0.5  # Allocate the remaining half to bonds

        return TargetAllocation(allocation_dict)