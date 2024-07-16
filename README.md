# Trading Bot Based on Financial News Sentiment Analysis

This repository contains a trading bot that leverages financial news sentiment analysis to make trading decisions. The bot uses the Alpaca API for trading and the FinBERT model for sentiment analysis of news headlines.

## Usage

1. **Configure your API keys:**

   Create a file named `trading-bot-config.json` in the root directory of the project and add your Alpaca API keys:

   ```json
   {
     "API_KEY": "your_api_key",
     "API_SECRET": "your_api_secret"
   }
   ```

2. **Run the trading bot:**

   ```bash
   python trading-bot.py
   ```

## Configuration

The `trading-bot-config.json` file should contain your Alpaca API credentials:

```json
{
  "API_KEY": "your_api_key",
  "API_SECRET": "your_api_secret"
}
```

## Backtesting

To backtest the strategy, set the start and end dates in the `trading-bot.py` file:

```python
# set start and end date for backtesting
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 6, 30)

# Backtesting
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={},
)
```

Then run the script:

```bash
python trading-bot.py
```

## FinBERT Model

The sentiment analysis is performed using the FinBERT model from the `transformers` library. This model is pretrained on financial text and can classify text into positive, negative, or neutral sentiment.

The `financial-sentiment.py` file contains the implementation for the sentiment analysis.

## Example

To test the sentiment analysis, you can run `financial-sentiment.py` directly:

```bash
python financial-sentiment.py
```

This will output the sentiment and probability for some test headlines.
