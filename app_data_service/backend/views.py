from rest_framework import viewsets
import yfinance as yf

class YahooViewSet(viewsets.ViewSet):
    def getStockData(self, request):
        


