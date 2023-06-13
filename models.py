"""
Models for Derebit-exchange client.
"""
from sqlalchemy import BigInteger, Float, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Ticker(Base):
    __tablename__ = 'tickers'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticker = mapped_column(String, nullable=False)
    price = mapped_column(Float, nullable=False)
    timestamp = mapped_column(BigInteger, nullable=False)

    def __repr__(self) -> str:
        return f"Ticker(ticker={self.ticker!r}, price={self.price!r})"
