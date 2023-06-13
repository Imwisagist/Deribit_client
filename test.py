import pytest
from aiohttp import ClientSession
from fastapi import Query
from sqlalchemy import select
from sqlalchemy import delete

from client import get_ticker, save_tickers_into_db
from db import async_db_session
from models import Ticker


@pytest.mark.asyncio
async def test_get_ticker():
    tickers: list = ["btc_usd", "eth_usd"]
    async with ClientSession() as http_session:
        for ticker in tickers:
            ticker_data: dict = await get_ticker(http_session, ticker)
            assert bool(ticker_data["result"]["index_price"]) is True
            assert bool(ticker_data["usOut"]) is True


@pytest.mark.asyncio
async def test_save_tickers_into_db():
    ticker: str = "xrp_usd"
    async with async_db_session() as session:
        async with session.begin():
            ticker_exists: Query = await session.execute(
                select(Ticker).filter_by(ticker=ticker)
            )
            ticker_exists = ticker_exists.scalars().first()
            assert ticker_exists is None
            await save_tickers_into_db(async_db_session, [ticker])
            ticker_exists: Query = await session.execute(
                select(Ticker).filter_by(ticker=ticker)
            )
            ticker_exists = ticker_exists.scalars().first()
            assert ticker_exists is not None
            stmt = delete(Ticker).where(Ticker.ticker.in_([ticker]))
            session.execute(stmt)
            session.commit()
