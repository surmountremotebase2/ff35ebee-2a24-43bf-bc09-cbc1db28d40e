from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # Focused on Apple stock, but you can include any other tickers
    
    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Using daily data intervals for the strategy
        return "1day"

    def run(self, data):
        # Initialize allocation with no stake, indicating a neutral position initially
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        for ticker in self.tickers:
            # Attempt to obtain MACD for the ticker
            try:
                macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
                macd_line = macd_data['MACD']
                signal_line = macd_data['signal']
                
                # Ensure we have enough data points to make a decision
                if len(macd_line) > 1 and len(signal_line) > 1:
                    # Check if MACD line crossed above the signal line to buy
                    if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
                        allocation_dict[ticker] = 1  # Assign full allocation to this stock
                        log(f"Going long on {ticker}")
                    # Check if MACD line crossed below the signal line to sell/not buy
                    elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
                        allocation_dict[ticker] = 0  # No allocation, indicating selling or avoiding buying
                        log(f"Selling or avoiding {ticker}")
                else:
                    log(f"Not enough data for {ticker} to apply MACD strategy.")
            except Exception as e:
                log(f"An error occurred while processing {ticker}: {e}")
        
        return TargetAllocation(allocation_dict)