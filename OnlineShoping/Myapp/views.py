from django.shortcuts import render
from .models import *
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse


# Create your views here.


def index(request):
    product = Product.objects.filter(category="Mens")
    women = Product.objects.filter(category="Women")
    d = {"product":product,"women":women}
    return render(request,'index-2.html', d)


def single(request, cat):
    all_prod = Product.objects.filter(category=cat)
    context = {"all_prod":all_prod}
    return render(request, "shop-gird.html", context)


def checkout(request):
    return render(request, 'checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    global checksum
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'index.html', {'response': response_dict})







