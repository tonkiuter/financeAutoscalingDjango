from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.functional import new_method_proxy
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from .models import Ticket
from .serializers import TickerSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views import View



#APiViews
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#Cosas para la API
import yfinance as yf
import pandas_datareader as pdr
from yfinance import ticker
from os import name, stat
import json
from django.http import JsonResponse



class TickerAPIView(APIView):
    
    def get(self, request):
        tickers = Ticket.objects.all()
        serializer = TickerSerializer(tickers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TickerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class TickerDetails(APIView):

    def get_object(request, ticker_id):
        try: 
            return Ticket.objects.get(ticker_id=ticker_id)
        except Ticket.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

    def get(self, request, ticker_id):
        tick = self.get_object(ticker_id)
        serializer = TickerSerializer(tick)
        return Response(serializer.data)

    def put(self, request, ticker_id):
        tick = self.get_object(ticker_id)
        serializer = TickerSerializer(tick, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, ticker_id):
        tick = self.get_object(ticker_id)
        tick.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class TickerMostrar(View):

    # def get(self, request, ticker_id):
    #     tick = ticker_id
    #     new_ticker = yf.Ticker(tick)
    #     hist = new_ticker.history(period="1mo")
    #     data = hist.to_json()
    #     return JsonResponse(data, safe=False)
    def get(self, request):
        tick = "ALSEA.MX"
        #tick = tickerid
        new_ticker = yf.Ticker(tick)
        hist = new_ticker.history(period="6mo")
        data = hist.to_json()
        return JsonResponse(data, safe=False)
        
    def post(self, request, ticker_id):
        tick = ticker_id
        new_ticker = yf.Ticker(tick)
        hist = new_ticker.history(period="1y")
        data = hist.to_json()
        return JsonResponse(data, safe=False)



# Create your views here.
#@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def ticker_list(request, ticker_id): 
    if request.method == 'GET' or  request.method == 'POST':
        tick = ticker_id
        new_ticker = yf.Ticker(tick)
        
        historical = new_ticker.history(period="1mo")
        data = historical.to_json()
        
        return Response(data)
