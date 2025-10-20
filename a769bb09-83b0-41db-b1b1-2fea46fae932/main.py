from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA, BB, MACD
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading, SocialSentiment, FinancialStatement, Ratios
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.growth_tickers = ["GDXU", "KORU", "DFEN", "MEXX", "EDC", "JNUG", "SLVP", "GDX"]
        self.stable_tickers = ["VXUS"]
        self.data_list = [SocialSentiment(t) for t in self.growth_tickers]  # Monitoring market sentiment
        self.data_list += [FinancialStatement(t) for t in ["GDX", "SLVP"]]  # Financial health for gold/silver

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        # Combine both lists for the assets property
        return self.growth_tickers + self.stable_tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}

        # Example of checking market sentiment
        positive_sentiment_tickers = [ticker for ticker in self.growth_tickers if data[("social_sentiment", ticker)][-1]['twitterSentiment'] > 0.5]
        
        # Possible condition for switching to stable assets
        if not positive_sentiment_tickers or len(positive_sentiment_tickers) < 3:
            # Market sentiment is not positive, allocate more to stable assets
            allocation_dict = {ticker: 0 for ticker in self.growth_tickers}
            allocation_dict["VXUS"] = 1  # Allocate fully to VXUS in downturn
        else:
            # Evenly distribute allocation among tickers with positive sentiment
            for ticker in self.growth_tickers:
                allocation_dict[ticker] = 1 / len(positive_sentiment_tickers) if ticker in positive_sentiment_tickers else 0

        return TargetAllocation(allocation_dict)