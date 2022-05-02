from django.urls import path, include

from home.views import Buy, Index , Sell, HistoryList, Register, Quote, ChangePassword
app_name = "home"
urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("buy", Buy.as_view(), name="buy"),
    path("change_password", ChangePassword.as_view(), name="change_password"),
    path("history", HistoryList.as_view(), name="history"),
    path("quote", Quote.as_view(), name="quote"),
    path("register", Register.as_view(), name="register"),
    path("sell", Sell.as_view(), name="sell"),
]
