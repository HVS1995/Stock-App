from django.http.response import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import time
import queue
from threading import Thread
from asgiref.sync import sync_to_async
# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()      #stock which are going to get display
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})

@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True

async def stockTracker(request):
    is_loginned = await checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")
    stockpicker = request.GET.getlist('stockpicker')
    stockshare=str(stockpicker)[1:-1]
    
    print(stockpicker)
    data = {}
    available_stocks = tickers_nifty50()         #allow to select stocks from nifty 
    for i in stockpicker:                       # loop will help to irretare over all stock
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")
    
    n_threads = len(stockpicker)           #we are using multithreads which will increase our efficiency
    thread_list = []
    que = queue.Queue()           # we are using queue which is used to stored data. we need to import this 
    start = time.time()
    # for i in stockpicker:
    #     result = get_quote_table(i)
    #     data.update({i: result})
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)           #add in thread list
        thread_list[i].start()               # this will start multithreading

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)
    end = time.time()
    time_taken =  end - start
    print(time_taken)
            
    
    print(data)
    return render(request, 'mainapp/stocktracker.html', {'data': data, 'room_name': 'track','selectedstock':stockshare})