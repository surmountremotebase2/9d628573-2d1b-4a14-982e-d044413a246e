from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, RSI
from surmount.data import Asset  # Assuming you can use a general Asset object for simplicity
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define tickers for both high growth (leveraged) and safe (gold, silver, bonds) ETFs
        self.high_growth_etfs = ["TQQQ", "GDXU"]  # Example leveraged ETFs for bullish markets
        self.safe_etfs = ["GLD", "SLV", "TLT"]  # Example gold, silver, and bond ETFs for bearish markets
        
        # You can further expand or adjust the ETFs based on your investment preferences and research

    @property
    def interval(self):
        # Choose an interval that suits the investment strategy's evaluation frequency
        return "1day"

    @property
    def assets(self):
        # Combine both ETF lists for the assets property
        return self.high_growth_etfs + self.safe_etfs

    def run(self, data):
        # This method decides which set of ETFs to allocate based on market conditions
        
        # Example market trend determination logic using a Simple Moving Average (SMA)
        sma_short = SMA("SPY", data, 50)  # Short-term trend
        sma_long = SMA("SPY", data, 200)  # Long-term trend
        
        if not sma_short or not sma_long:
            log("Insufficient data for SMA calculation.")
            return TargetAllocation({})  # Return empty allocation on error
        
        # Determine market condition
        bullish_market = sma_short[-1] > sma_long[-1] # Assuming a bullish condition when the short-term SMA is above long-term SMA

        allocation = {}
        if bullish_market:
            # Allocate evenly among high-growth ETFs
            for etf in self.high_growth_etfs:
                allocation[etf] = 1 / len(self.high_growth_etfs)
        else:
            # Allocate evenly among safe ETFs
            for etf in self.safe_etfs:
                allocation[etf] = 1 / len(self.safe_etfs)

        return TargetAllocation(allocation)