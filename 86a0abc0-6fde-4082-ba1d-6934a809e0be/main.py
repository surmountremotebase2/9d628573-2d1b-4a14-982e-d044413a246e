from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import ConsumerConfidence, CboeVolatilityIndexVix
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers for the ETFs and bonds
        self.tickers = ["TQQQ", "VXUS", "GDX", "GDXU", "SLVP", "BOND"]
        self.data_list = [ConsumerConfidence(), CboeVolatilityIndexVix()]

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    @property
    def interval(self):
        # Using daily data for trend analysis
        return "1day"

    def run(self, data):
        # Initialize allocation with zero holdings in all assets
        allocation_dict = {ticker: 0 for ticker in self.tickers}

        consumer_confidence = data[("consumer_confidence",)] if ("consumer_confidence",) in data else None
        vix = data[("cboe_volatility_index_vix",)] if ("cboe_volatility_index_vix",) in data else None

        # Market sentiment check
        is_bullish = consumer_confidence and consumer_confidence[-1]["value"] > 100
        is_bearish_vix = vix and vix[-1]["value"] > 20  # VIX above 20 often indicates higher market volatility

        # Strategy decision making
        if is_bullish and not is_bearish_vix:
            allocation_dict["TQQQ"] = 0.6  # Leveraging on bullish market conditions
            allocation_dict["VXUS"] = 0.4  # Diversification with international stocks
        elif is_bearish_vix:
            # Switching to more stable investments during high volatility
            allocation_dict["GDX"] = 0.25  # Investing in gold miners as a hedge
            allocation_dict["GDXU"] = 0.25  # Additional leverage on gold miners
            allocation_dict["SLVP"] = 0.25  # Investing in silver miners
            allocation_dict["BOND"] = 0.25  # Bonds for minimizing drawdowns
        else:
            allocation_dict["VXUS"] = 0.5  # Diverting to international stocks
            allocation_dict["BOND"] = 0.5  # Holding bonds for safety

        return TargetAllocation(allocation_dict)