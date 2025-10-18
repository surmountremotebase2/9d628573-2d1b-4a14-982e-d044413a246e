from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.assets = ["VXUS", "QQQ", "BND", "GDX", "GDXU", "SLVP"]
        self.lookback_period = 50  # Used for SMA calculation

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        rsi_vxus = RSI("VXUS", data["ohlcv"], length=14)
        rsi_qqq = RSI("QQQ", data["ohlcv"], length=14)
        sma_vxus = SMA("VXUS", data["ohlcv"], length=self.lookback_period)[-1]
        sma_qqq = SMA("QQQ", data["ohlcv"], length=self.lookback_period)[-1]
        current_price_vxus = data["ohlcv"][-1]["VXUS"]["close"]
        current_price_qqq = data["ohlcv"][-1]["QQQ"]["close"]

        allocation = {"BND": 0, "GDX": 0, "GDXU": 0, "SLVP": 0, "VXUS": 0, "QQQ": 0}

        # Check for overbought conditions to decide on bond allocation
        if rsi_vxus[-1] > 70 or rsi_qqq[-1] > 70:
            allocation["BND"] = 1  # Move fully into bonds
        # Check for downward trends to move into gold and silver mining ETFs
        elif current_price_vxus < sma_vxus or current_price_qqq < sma_qqq:
            allocation["GDX"] = 0.4
            allocation["GDXU"] = 0.3
            allocation["SLVP"] = 0.3
        else:
            # Default to growth ETFs if no overbought or downward trend is detected
            allocation["VXUS"] = 0.5
            allocation["QQQ"] = 0.5

        return TargetAllocation(allocation)