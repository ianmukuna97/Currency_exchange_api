import requests
import os


BASE_URL = os.getenv("PROVIDER_URL", "https://api.exchangerate.host")

class ExchangeRateProvider:
    @staticmethod
    def get_latest(base="USD", symbols=None):
        url = f"{BASE_URL}/latest"
        params = {}
        if symbols:
            params["symbols"] = symbols
        access_key = os.getenv("ACCESS_KEY") or os.getenv("EXCHANGE_API_KEY")
        if access_key:
            params["access_key"] = access_key
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    
    @staticmethod
    def convert(frm="USD", to="EUR", amount=1, date=None):
        # Since convert API is restricted, calculate using latest rates
        rates_data = ExchangeRateProvider.get_latest()
        if "rates" not in rates_data:
            raise ValueError("Unable to fetch rates for conversion")
        rates = rates_data["rates"]
        base = rates_data.get("base", "EUR")
        if frm == base:
            rate_to = rates.get(to.upper())
            if not rate_to:
                raise ValueError(f"Currency {to} not found in rates")
            converted_amount = amount * rate_to
        elif to == base:
            rate_from = rates.get(frm.upper())
            if not rate_from:
                raise ValueError(f"Currency {frm} not found in rates")
            converted_amount = amount / rate_from
        else:
            rate_from = rates.get(frm.upper())
            rate_to = rates.get(to.upper())
            if not rate_from or not rate_to:
                raise ValueError(f"Currency {frm} or {to} not found in rates")
            converted_amount = amount * (rate_to / rate_from)
        return {
            "success": True,
            "query": {
                "from": frm,
                "to": to,
                "amount": amount
            },
            "info": {
                "timestamp": rates_data.get("timestamp"),
                "rate": rate_to / rate_from if frm != base and to != base else (rate_to if frm == base else 1 / rate_from)
            },
            "date": rates_data.get("date"),
            "result": converted_amount
        }
    
    @staticmethod
    def historical(date, base="USD", symbols=None):
        url = f"{BASE_URL}/{date}"
        params = {}
        if symbols:
            params["symbols"] = symbols
        access_key = os.getenv("ACCESS_KEY") or os.getenv("EXCHANGE_API_KEY")
        if access_key:
            params["access_key"] = access_key
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
