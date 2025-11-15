# from django.shortcuts import render
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .provider import ExchangeRateProvider
import os

# Create your views here.
CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 300))

@api_view(["GET"])
def get_rates(request):
    base = request.GET.get("base", "USD").upper()
    symbols = request.GET.get("symbols")

    cache_key = f"rates:{base}:{symbols}"
    data = cache.get(cache_key)
    if not data:
        try:
            data = ExchangeRateProvider.get_latest(base=base, symbols=symbols)
            cache.set(cache_key, data, timeout=CACHE_TIMEOUT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    return Response(data)
    
@api_view(["GET"])
def convert_currency(request):
    frm = request.GET.get("from")
    to = request.GET.get("to")
    amount = request.GET.get("amount", 1)
    date = request.GET.get("date") 
    if not frm or not to:
        return Response({"error": "Parameters 'from' and 'to' are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        amount = float(amount)
    except ValueError:
        return Response({"error": "Amount must be a number"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    cache_key = f"convert:{frm}:{to}:{amount}:{date or 'latest'}"
    data = cache.get(cache_key)
    if not data:
        try:
            data = ExchangeRateProvider.convert(frm, to, amount)
            cache.set(cache_key, data, timeout=CACHE_TIMEOUT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    return Response(data)
    
@api_view(["GET"])
def get_historical(request):
    date = request.GET.get("date")
    base = request.GET.get("base", "USD").upper()
    symbols = request.GET.get("symbols")


    if not date:
        return Response({"error": "Parameter 'date' is required"}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = f"history:{date}:{base}:{symbols}"
    data = cache.get(cache_key)
    if not data:
        try:
            data = ExchangeRateProvider.historical(date, base, symbols)
            cache.set(cache_key, data, timeout=CACHE_TIMEOUT)
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_502_BAD_GATEWAY)
    return Response(data)
    