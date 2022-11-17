from fastapi import APIRouter, Request
from typing import Optional
import requests

from currency_converter_api.schemas import Output
from currency_converter_api._secrets import key

router = APIRouter()

# apikey provided upon request
API_KEY = key
BASE_URL = "https://api.fastforex.io/"
HEADERS = {"accept": "application/json"}


@router.get("/currencies", response_model=Output)
async def currencies(request: Request):
    """
    Fetch a list of supported currencies
    """
    currencies_url = f"currencies?api_key={API_KEY}"
    response = requests.get(BASE_URL + currencies_url, headers=HEADERS)
    return Output(success=True, results=[response.text])


@router.get("/convert", response_model=Output)
async def convert(
    request: Request,
    amount: int,
    from_curr: str,
    to_curr: str,
    date: Optional[str] = None
):
    """
    Convert an amount of one currency into another currency.
    from_curr : Base currency symbol
    to_curr : Target currency symbol
    amount : Amount of source currency to convert
    date: UTC date in YYYY-MM-DD format. Must be within the last 14 days.
    """
    convert_url = f"convert?from={from_curr}&to={to_curr}&amount={amount}&" \
                  f"api_key={API_KEY}"
    response = requests.get(BASE_URL + convert_url, headers=HEADERS)
    if date is not None:
        historical_url = f"historical?date={date}&from={from_curr}&" \
                         f"to={to_curr}&api_key={API_KEY}"
        response2 = requests.get(BASE_URL + historical_url, headers=HEADERS)
        return Output(success=True, results=[response.text, response2.text])
    else:
        return Output(success=True, results=[response.text])


@router.get("/fetch_one", response_model=Output)
async def fetch_one(
    request: Request,
    from_curr: str,
    to_curr: str
):
    """
    Fetch a single currency exchange rate, from and to any supported currency.
    from_curr : Base currency symbol
    to_curr : Target currency symbol
    """
    fetch_one_url = f"fetch-one?from={from_curr}&to={to_curr}&api_key={API_KEY}"
    response = requests.get(BASE_URL + fetch_one_url, headers=HEADERS)
    return Output(success=True, results=[response.text])


@router.get("/fetch_all", response_model=Output)
async def fetch_all(request: Request, from_curr: str):
    """
    Fetch all available currency rates.
    from_curr : Base currency symbol
    """
    fetch_all_url = f"fetch-all?from={from_curr}&api_key={API_KEY}"
    response = requests.get(BASE_URL + fetch_all_url, headers=HEADERS)
    return Output(success=True, results=[response.text])