from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Defining tickers for the strategy
        self.tech_tickers = ['TQQQ', 'QQQM']
        self.gold_silver_tickers = ['GDX', 'GDXU', 'SLVP']
        self.core_ticker = 'VXUS'
    
    @property
    def assets(self):
        # Assets to be included in the strategy
        return self.tech_tickers + self.gold_silver_tickers + [self.core_ticker]

    @property
    def interval(self):
        # Using daily data for trend analysis
        return "1day"
    
    def run(self, data):
        # Initial allocation dictionary
        allocation_dict = {i: 0 for i in self.assets}
        # Core holding in VXUS at 20%
        allocation_dict['VXUS'] = 0.20
        
        # Example of a simple moving average crossover detection for down market trend 
        # Implementing trend detection for TQQQ as an example
        for ticker in self.tech_tickers:
            short_sma = SMA(ticker, data, length=50)[-1]  # Short-term SMA
            long_sma = SMA(ticker, data, length=200)[-1]  # Long-term SMA

            if short_sma and long_sma:
                if short_sma < long_sma:
                    # Down trend detected, allocate to gold and silver tickers
                    log(f"Down trend detected for {ticker}, reallocating to gold and silver.")
                    for gt in self.gold_silver_tickers:
                        allocation_dict[gt] = 0.20 / len(self.gold_silver_tickers)  # Evenly distributing remaining 20% among gold and silver assets
                    break  # Assuming we switch strategy for the first downtrend detected
        
        # If no downtrend is detected for both tech tickers, distribute the remaining 80% evenly
        if not any(allocation_dict[gt] > 0 for gt in self.gold_silver_tickers):
            rem_allocation = 0.80 / len(self.tech_tickers)  # Remaining allocation for tech tickers
            for ticker in self.tech_tickers:
                allocation_dict[ticker] = rem_allocation
        
        return TargetAllocation(allocation_dict)