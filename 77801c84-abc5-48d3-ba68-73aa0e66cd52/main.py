from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import Asset, SectorsPERatio
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define tickers for growth stocks/ETFs and safe assets
        self.growth_assets = ["AAPL", "SPY", "QQQ", "TSLA"]
        self.safe_assets = ["GLD", "SLV", "TLT"]
        
        # Data list to include S&P 500 P/E ratio as a market sentiment indicator
        self.data_list = [SectorsPERatio("S&P 500")]

    @property
    def interval(self):
        return "1day"
    
    @property
    def assets(self):
        # Combining both asset lists since we might switch between them
        return self.growth_assets + self.safe_assets

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        
        # Calculate the moving average of the S&P 500 P/E ratio to determine market condition
        pe_data = data[("sectors_pe_ratio", "S&P 500")]
        pe_values = [x['pe'] for x in pe_data[-20:]]  # Using last 20 days of P/E ratios
        current_pe = pe_values[-1]
        avg_pe = sum(pe_values) / len(pe_values)
        
        # If current P/E is significantly higher than the average, it might indicate overvaluation or heightened market risk
        if current_pe > avg_pe * 1.1:
            # Market seems overvalued; switch to safe assets
            log("Switching to safe assets")
            for asset in self.safe_assets:
                allocation_dict[asset] = 1 / len(self.safe_assets)
            for asset in self.growth_assets:
                allocation_dict[asset] = 0  # No allocation to growth assets
        else:
            # Market seems normal or undervalued; focus on growth assets
            log("Focusing on growth assets")
            for asset in self.growth_assets:
                allocation_dict[asset] = 1 / len(self.growth_assets)
            for asset in self.safe_assets:
                allocation_dict[asset] = 0  # No allocation to safe assets
        
        return TargetAllocation(allocation_dict)