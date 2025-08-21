# polygon-api-client
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from polygon import RESTClient

class PolygonStockRequest(BaseModel):
    """The Ticker to get the market information on"""
    ticker: str = Field(..., description="The stock ticker to research.")

class PolygonStockTool(BaseTool):
    
    name: str = "Use the polygon api for market data to get information"
    description: str = (
        "This tool is used to get stock information from the Polygon API on a specific ticker."
    )
    args_schema: Type[BaseModel] = PolygonStockRequest

    def _getFin(self, client, ticker):
        financials = []
        for f in client.vx.list_stock_financials(
            ticker=ticker,
            order="asc",
            limit="5",
            period_of_report_date_gte="2025-01-01",
            sort="filing_date",
            ):
            financials.append(f.__dict__)
        return financials

    def _run(self, ticker: str) -> str:
        polygonToken = os.getenv("POLYGON_DATA_TOKEN")
        client = RESTClient(polygonToken)
        gen = client.get_ticker_details(ticker)
        fin = self._getFin(client, ticker)
        macd = client.get_macd(
                ticker=ticker,
                timespan="day",
                short_window=12,
                long_window=26,
                signal_window=9,
                series_type="close",
            )
        sma = client.get_sma(
                ticker=ticker,
                timespan="day",
                window=50,
                series_type="close",
            )
        ema = client.get_ema(
                ticker=ticker,
                timespan="day",
                window=50,
                series_type="close",
            )
        return {'ticker': ticker, 'financials': fin, 'macd': macd.__dict__, 'sma': sma.__dict__, 'ema': ema.__dict__}