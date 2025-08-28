import pandas as pd
from indicators import get_historical_data, add_ema, add_macd, add_volume

def main():
    """
    Main function to fetch data and calculate indicators.
    """
    instrument = 'EUR_USD'
    granularity = 'D'

    # Fetch historical data
    data = get_historical_data(instrument, granularity)

    # Add indicators
    data = add_ema(data, period=200)
    data = add_macd(data)
    data = add_volume(data)

    # Display the data with indicators
    print(f"Data for {instrument} with indicators:")
    print(data.tail())

if __name__ == '__main__':
    # Set pandas display options for better viewing
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    main()
