import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import talib
import settings

def get_historical_data(instrument, granularity='D', count=500):
    """
    Fetches historical data for a given instrument from OANDA.
    """
    api = API(access_token=settings.OANDA_API_KEY)
    params = {
        'count': count,
        'granularity': granularity
    }
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    api.request(r)

    data = []
    for candle in r.response['candles']:
        data.append([
            candle['time'],
            candle['volume'],
            candle['mid']['o'],
            candle['mid']['h'],
            candle['mid']['l'],
            candle['mid']['c']
        ])

    df = pd.DataFrame(data, columns=['time', 'volume', 'open', 'high', 'low', 'close'])
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # Ensure numeric types for calculations
    for col in ['volume', 'open', 'high', 'low', 'close']:
        df[col] = pd.to_numeric(df[col])

    return df

def add_ema(df, period=200):
    """
    Calculates the Exponential Moving Average (EMA) and adds it to the DataFrame.
    """
    df[f'ema_{period}'] = talib.EMA(df['close'], timeperiod=period)
    return df

def add_macd(df, fastperiod=12, slowperiod=26, signalperiod=9):
    """
    Calculates the Moving Average Convergence Divergence (MACD) and adds it to the DataFrame.
    """
    df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(
        df['close'],
        fastperiod=fastperiod,
        slowperiod=slowperiod,
        signalperiod=signalperiod
    )
    return df

def add_volume(df):
    """
    Ensures the volume is present in the DataFrame.
    """
    if 'volume' not in df.columns:
        # If volume is not provided by the API, we can't calculate it here.
        # This function serves as a placeholder and for clarity.
        df['volume'] = 0
    return df
