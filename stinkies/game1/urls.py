from django.urls import path

from game1 import views

app_name = "game1"

urlpatterns = [
    path('', views.homepage_view, name="homepage"),
    path('buy/stinky/new/', views.buy_new_stinky_view, name="buy-new-stinky"),
]