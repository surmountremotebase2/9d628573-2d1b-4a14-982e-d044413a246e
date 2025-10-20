from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Tickers for Tech ETFs (TQQQ, QQQM) and Gold/Silver ETFs (GDX, GDXU, SLVP)
        self.tickers = ["TQQQ", "QQQM", "GDX", "GDXU", "SLVP"]

    @property
    def interval(self):
        # Using daily data for analysis
        return "1day"

    @property
    def assets(self):
        # Assets to consider for trading
        return self.tickers

    def run(self, data):
        # Initialize allocation dictionary
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        # Calculate RSI for a generic decision-making reference (14-day RSI)
        rsi_values = {ticker: RSI(ticker, data["ohlcv"], 14) for ticker in self.tickers}
        
        # Strategy to increase gold/silver allocation if RSI > 70 for tech ETFs or decrease otherwise
        overbought_tech = any(rsi[-1] > 70 for ticker, rsi in rsi_values.items() if ticker in ["TQQQ", "QQQM"])
        
        if overbought_tech:
            # Strategy favors precious metals when tech is overbought
            allocation_dict["GDX"] = 0.3  # 30% to GDX
            allocation_dict["GDXU"] = 0.2 # 20% to GDXU
            allocation_dict["SLVP"] = 0.2  # 20% to SLVP
            allocation_dict["TQQQ"] = 0.15 # 15% to TQQQ
            allocation_dict["QQQM"] = 0.15 # 15% to QQQM
        else:
            # Favors tech when not overbought
            allocation_dict["TQQQ"] = 0.4  # 40% to TQQQ
            allocation_dict["QQQM"] = 0.4  # 40% to QQQM
            allocation_dict["GDX"] = 0.1   # 10% to GDX
            allocation_dict["GDXU"] = 0.05 # 5% to GDXU
            allocation_dict["SLVP"] = 0.05 # 5% to SLVP

        return TargetAllocation(allocation_dict)