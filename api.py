"""
Api for processing stored data.
"""
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware

from db import async_db_session
from models import Ticker

app: FastAPI = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'])


@app.get("/get_all_data_about_ticker")
async def get_all_data_about_ticker(ticker: str = Query(...)):
    try:
        async with async_db_session() as session:
            async with session.begin():
                ticker_all_data: Query = await session.execute(
                    select(Ticker).filter_by(ticker=ticker)
                )
                ticker_all_data = ticker_all_data.scalars().all()

        if not ticker_all_data:
            raise HTTPException(status_code=404, detail="Ticker not found")

        return [
            {"ticker": t.ticker, "price": t.price, "timestamp": t.timestamp}
            for t in ticker_all_data
        ]

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="DB error") from error


@app.get("/get_last_price_of_ticker")
async def get_last_price_of_ticker(ticker: str = Query(...)):
    try:
        async with async_db_session() as session:
            async with session.begin():
                last_ticker_data: Query = await session.execute(
                    select(Ticker).filter_by(ticker=ticker).order_by(
                        Ticker.timestamp.desc()
                    )
                )
                last_ticker_data = last_ticker_data.scalars().first()

                if not last_ticker_data:
                    raise HTTPException(
                        status_code=404, detail="Ticker not found"
                    )

                return {"ticker": last_ticker_data.ticker,
                        "price": last_ticker_data.price,
                        "timestamp": last_ticker_data.timestamp}

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="DB error") from error


@app.get("/get_price_of_ticker_by_time")
async def get_price_of_ticker_by_time(
        ticker: str = Query(...), timestamp: int = Query(...)):
    try:
        async with async_db_session() as session:
            async with session.begin():
                ticker_data: Query = await session.execute(
                    select(Ticker).filter_by(
                        ticker=ticker, timestamp=timestamp
                    )
                )
                ticker_data = ticker_data.scalars().first()

                if not ticker_data:
                    raise HTTPException(
                        status_code=404, detail="Ticker not found"
                    )

                return {"ticker": ticker_data.ticker,
                        "price": ticker_data.price,
                        "timestamp": ticker_data.timestamp}

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="DB error") from error
