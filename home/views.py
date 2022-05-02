from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from home.forms import UserForm
from home.helper import lookup, apology, usd
from home.models import StockUser, History, AvailableStocks
# Create your views here.

USER = None

# def index(request):
#     global USER
#     USER = request.user
#     # available_cash = StockUser.objects.values('cash').get(user=USER)['cash']
#     # print(available_cash)
    

#     # form = UserForm()
#     # print(dir(form))
#     quote = lookup("nflx")
#     # print(quote)
#     return render(request, "home/index.html", context={'quote': quote})

class Index(LoginRequiredMixin, View):
    def get(self, request):
        global USER
        USER = request.user
        # print(USER)
        id = StockUser.objects.get(user=USER)
        try:
            stocks = AvailableStocks.objects.filter(user=id).order_by('symbol')
        except Exception:
            stocks = None
        cash = float(id.cash)
        total = cash
        quotes = None
        if stocks:
            quotes = []
            for stock in stocks:
                quote = {
                    'symbol': stock.symbol,
                    'shares': stock.shares,
                }
                # print(quote)
                # print(lookup(quote["symbol"]))
                # print(lookup(quote["symbol"]))
                quote.update(lookup(quote["symbol"]))
                quote["total"] = (quote["price"] * quote["shares"])
                quote["price"] = usd(quote["price"])
                quotes.append(quote)
            for quote in quotes:
                total += quote["total"]            
                quote["total"] = usd(quote["total"])
        
        cash = usd(cash)
        total = usd(total)
        context = {
            "quotes": quotes,
            "total":total,
            "cash":cash 
        }
        return render(request, "home/index.html", context)

class Buy(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/buy.html")
    
    def post(self, request):
        symbol = request.POST.get("symbol")
        shares = int(request.POST.get("shares"))
        if not symbol:
            return apology(request, "Invalid Symbol")
        if not shares or shares < 0:
            return apology(request, "Invalid shares")
        
        price = lookup(symbol).get("price")
        total_cost = shares * price
        global USER
        USER = request.user
        # print(USER)
        id = StockUser.objects.get(user=USER)
        available_cash = float(id.cash)
        if total_cost > available_cash:
            return apology(request, "Don't have enough cash")
        available_cash = available_cash - total_cost
        category = "bought"
        id.cash = available_cash
        id.save()
        History.objects.create(category=category, price=price, shares=shares, symbol=symbol, user=id)
        try:
            stock = AvailableStocks.objects.get(user=id, symbol=symbol)
        except Exception:
            stock = None
        if stock:
            available_shares = stock.shares
            current_shares = available_shares + shares
            stock.shares = current_shares
            stock.save()
        else:
            AvailableStocks.objects.create(user=id, symbol=symbol, shares=shares)
        messages.success(request, "Bought!")
        return redirect(reverse_lazy("home:index"))

class ChangePassword(SuccessMessageMixin, PasswordChangeView):
    template_name = "registration/password_change.html"
    success_message = "Password Changed Successfully!"
    def get_success_url(self):
        success_url = reverse_lazy("logout") + "?next=" + reverse_lazy("login")
        return success_url

class HistoryList(LoginRequiredMixin, ListView):
    model = History

    # def get_context_data(self, **kwargs):
    #     global USER
    #     USER = self.request.user
    #     id = StockUser.objects.get(user = USER)
    #     rows = History.objects.filter(user=id)
    #     context = super().get_context_data(**kwargs)
    #     context['rows'] = rows
    #     return context

class Quote(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/quote.html")

    def post(self, request):
        symbol = request.POST.get("symbol")
        # print(symbol)
        quote = lookup(symbol)
        if not quote:
            return apology(request, "Invalid Symbol")
        quote["price"] = usd(quote["price"])
        # print(quote["price"])
        context = {
            "quote": quote
        }
        return render(request, "home/quoted.html", context=context)

class Register(SuccessMessageMixin, CreateView):
    form_class = UserForm
    model = User
    success_message = "Registered!"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.cleaned_data.get("username")
        StockUser.objects.create(user=user)
        return super().form_valid(form)
    
class Sell(LoginRequiredMixin, View):
    def get(self, request):
        global USER
        USER = request.user
        id = StockUser.objects.get(user = USER)
        symbols = AvailableStocks.objects.values('symbol').filter(user=id).order_by('symbol')
        context = {
            'symbols': symbols
        }
        return render(request, "home/sell.html", context)
    
    def post(self, request):
        global USER
        USER = request.user
        id = StockUser.objects.get(user = USER)
        symbol = request.POST.get("symbol")
        shares = int(request.POST.get("shares"))
        if not symbol:
            return apology(request, "Invalid Symbol")
        if not shares or shares < 0:
            return apology(request, "Invalid Shares")
        try:
            stock = AvailableStocks.objects.get(user=id, symbol=symbol)
            available_shares = stock.shares
        except Exception:
            available_shares = None
        if not available_shares or available_shares < shares:
            return apology(request, "Don't have enough shares")

        available_shares = available_shares - shares
        if available_shares > 0:
            stock.shares = available_shares
            stock.save()
        else:
            stock.delete()

        price = lookup(symbol).get("price")
        got_cash = price * shares
        cash = float(id.cash)
        cash += got_cash
        id.cash = cash
        id.save()
        category = "Sold"
        History.objects.create(category=category, price=price, shares=shares, symbol=symbol, user=id)
        price = usd(price)
        messages.success(request, "Sold!")
        return redirect(reverse_lazy("home:index"))