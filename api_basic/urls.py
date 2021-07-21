from django.urls import path
from .views import ticker_list, TickerAPIView, TickerDetails, TickerMostrar
#from .views import TickerAPIView, TickerDetails, TickerMostrar
urlpatterns = [
    path('show/<str:ticker_id>', ticker_list), 
    path('ticker/', TickerAPIView.as_view()),
    path('detail/<str:ticker_id>', TickerDetails.as_view()),
    # path('mostrar/<str:ticker_id>', TickerMostrar.as_view()),
    path('mostrar/', TickerMostrar.as_view()),
    
]