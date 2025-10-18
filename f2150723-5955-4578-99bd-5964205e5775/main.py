from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Define the tickers of interest
        self.tickers = ["TQQQ", "VXUS", "GDX", "GDXU", "SLVP", "BOND"]
    
    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Using daily data for trend analysis
        return "1day"

    def run(self, data):
        # Initial allocation dictionary: keys are tickers, values are allocations
        allocation_dict = {ticker: 0 for ticker in self.tickers}

        # Iterate through each asset to calculate MACD and RSI for trend and momentum
        for ticker in self.tickers:
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            rsi_data = RSI(ticker, data["ohlcv"], length=14)
            
            # Check if data for MACD and RSI calculation is present
            if macd_data is not None and rsi_data is not None:
                macd_hist = macd_data.get("histogram")[-1]
                rsi_last = rsi_data[-1]
                
                # Decision conditions based on MACD histogram and RSI values
                if macd_hist > 0 and rsi_last < 70:
                    # Growth-focused condition: prioritize TQQQ for aggressive growth, VXUS for diversification
                    if ticker == "TQQQ":
                        allocation_dict[ticker] = 0.4  # 40% to TQQQ
                    elif ticker == "VXUS":
                        allocation_dict[ticker] = 0.3  # 30% to VXUS
                elif macd_hist < 0 or rsi_last > 70:
                    # Safety and value condition: prioritize gold, silver, and bonds
                    if ticker in ["GDX", "GDXU", "SLVP"]:
                        allocation_dict[ticker] = 0.1  # 10% each to gold and silver assets
                    elif ticker == "BOND":
                        allocation_dict[ticker] = 0.4  # 40% to bonds for safety

        # Ensure the sum of allocations does not exceed 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1.0:
            # Scale down allocations proportionally if total exceeds 100%
            allocation_dict = {ticker: (alloc / total_allocation) for ticker, alloc in allocation_dict.items()}

        return TargetAllocation(allocation_dict)