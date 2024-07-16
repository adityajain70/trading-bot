from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
from financial_sentiment import estimate_sentiment
import json

# get api keys
with open('./trading-bot-config.json') as f:
    config = json.load(f)
    
API_KEY = config['API_KEY']
API_SECRET = config['API_SECRET']
BASE_URL = 'https://paper-api.alpaca.markets'

ALPACA_CREDS = {
    'API_KEY': API_KEY,
    'API_SECRET': API_SECRET,
    'PAPER': True,
}


class MLTrader(Strategy):
    def initialize(self, symbol = 'SPY', cash_at_risk = 0.5): # adjust cash_at_risk for amount of risk 
        self.symbol = symbol
        self.sleeptime = '12H'
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    # returns order to place
    def position_sizing(self):
        # get current cash available
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = cash * self.cash_at_risk // last_price
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        two_days_prior_date = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), two_days_prior_date.strftime('%Y-%m-%d')

    # gets news and sentiment
    def get_news_and_setiment(self):
        today, two_days_prior_date = self.get_dates()
        news = self.api.get_news(symbol = self.symbol, start = two_days_prior_date, end = today)
        # unpack headline
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news)

        return probability, sentiment

    # runs every time new information is received
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_news_and_setiment()

        if cash > last_price:
            # positive sentiment news
            if sentiment == 'positive' and probability > 0.9:
                if self.last_trade == 'sell':
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    'buy',
                    type='bracket',
                    take_profit_price = last_price * 1.25, # define when to take gains
                    stop_loss_price = last_price * 0.95 # define when to stop any losses
                )

                self.submit_order(order)
                self.last_trade = 'buy'
            # negative sentiment news
            elif sentiment == 'negative' and probability > 0.9:
                if self.last_trade == 'buy':
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    'sell',
                    type='bracket',
                    take_profit_price = last_price * 0.75, # define when to take gains
                    stop_loss_price = last_price * 1.05 # define when to stop any losses
                )

                self.submit_order(order)
                self.last_trade = 'sell'

# set start and end date for backtesting
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 6, 30)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='strat', broker=broker, parameters={'symbol':'SPY', 
                                                             'cash_at_risk': 0.5})

# backtesting
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={},
)
