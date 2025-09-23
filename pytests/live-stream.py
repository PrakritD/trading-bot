import asyncio
from alpaca.data.live import StockDataStream
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY  = os.getenv("ALPACA_KEY_ID")
SECRET   = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_ENV")       # paper or live
# DATA_URL = os.getenv("APCA_API_DATA_URL")       # market d

async def main():
    stream = StockDataStream(API_KEY, SECRET, url_override=BASE_URL)

    async def on_bar(bar):
        print("BAR", bar.symbol, bar.close, bar.timestamp)

    async def on_trade_update(update):
        print("TRADE UPDATE", update)

    # subscribe to minute bars
    stream.subscribe_bars(on_bar, "AAPL")

    # run until cancelled
    await stream.run()

if __name__ == "__main__":
    asyncio.run(main())