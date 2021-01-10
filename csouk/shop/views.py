from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders
from math import ceil


# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)

    allProds = []
    catprod = Product.objects.values('category', 'id', 'product_name')
    cats = {item['category'] for item in catprod}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = ((n // 4) + ceil((n / 4) - (n // 4)))
        allProds.append([prod, range(1, nSlides), nSlides])
        # print(allProds)

    # params = {'products': products, 'no_of_slides': nSlides, 'range': range(1, nSlides)}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]

    params = {'allProds': allProds}   #params is always dictionary
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', 'default')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contacts = Contact(name=name, email=email, phone_number=phone, description=desc)
        contacts.save()


    return render(request, 'shop/contact.html')


def tracker(request):
    return render(request, 'shop/tracker.html')


def search(request):
    return HttpResponse("we are at search.")


def productview(request, myid):
    # Fetch the Products by Id
    product = Product.objects.filter(id=myid)   # product is the list
    product = {'product': product[0]}    # this.product is the dictionary
    return render(request, 'shop/productView.html', product)


class Order(object):
    pass


def checkout(request):
    if request.method == 'POST':
        items_json = request.POST.get('items_json', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        pincode = request.POST.get('pincode', '')
        # print(name, email, phone, desc)
        orders = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, pin_code=pincode, phone=phone)
        orders.save()
        thank = True
        id = orders.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')




