"""
Client for Derebit-exchange.
Every minute current script requesting actual price of tickers also
saving in the database every ticker, price and time in UNIX format.
"""
from asyncio import get_event_loop

from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import async_db_session, init_db
from models import Ticker


async def get_ticker(session: ClientSession, ticker: str) -> dict:
    endpoint: str = ("https://www.deribit.com/api/v2/public/" +
                     f"get_index_price?index_name={ticker}")
    async with session.get(endpoint) as response:
        return await response.json()


async def save_tickers_into_db(aio_db_session, tickers: list[str]) -> None:
    async with ClientSession() as http_session:
        async with aio_db_session() as db_session:
            async with db_session.begin():
                for ticker in tickers:
                    ticker_data: dict = await get_ticker(http_session, ticker)
                    db_session.add(
                        Ticker(
                            ticker=ticker,
                            price=ticker_data["result"]["index_price"],
                            timestamp=ticker_data["usOut"]
                        )
                    )


async def main() -> None:
    scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        save_tickers_into_db, trigger="interval", seconds=60,
        kwargs={
            "tickers": ["btc_usd", "eth_usd"],
            "aio_db_session": async_db_session,
        }
    )
    scheduler.start()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.create_task(init_db())
    loop.create_task(main())
    loop.run_forever()
