from django.urls import path

from game1 import views

app_name = "game1"

urlpatterns = [
    path('', views.homepage_view, name="homepage"),
    path('buy/stinky/new/', views.buy_new_stinky_view, name="buy-new-stinky"),
    path('sell/<int:inventory_item_id>/', views.sell_back_stinky_view, name="sell-back-stinky"),
    path('player/<slug:username>/', views.view_player_view, name="view-player"),
    path('trade/<int:inv_id>/', views.trade_item_view, name="trade-stinky"),
    path('trade/<int:inv_id>/cancel/', views.dont_trade_item_view, name="dont-trade-stinky"),
]