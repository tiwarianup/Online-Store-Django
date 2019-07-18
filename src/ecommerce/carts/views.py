from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from products.models import Product
from billing.models import BillingProfile
# Create your views here.
from .models import Cart
from orders.models import Order

# def cartCreate(user=None):
#     cartObj = Cart.objects.create(user=None)
#     print("New cart Id created")
#     return cartObj

def cartHome(request):
    cartObj, newObj = Cart.objects.createNewOrGet(request)
    return render(request, 'carts/home.html', {"cart":cartObj})

    # if cartId is None:#and isinstance(cartId, int):
    #     cartObj = Cart.objects.create(user=None)
    #     request.session['cartId'] = cartObj.id
    #     #print("new cerated",  request.session['cartId'])
    # else:
    #     print("Cart Id Exists.")
    #     cartObj = Cart.objects.get(id=cartId)
    #     #print(request.session.get('cartId'))

    # qs = Cart.objects.filter(id=cartId)
    # if qs.count() == 1:
    #     cartObj = qs.first()
    #     print('Cart ID exists')
    #     if request.user.is_authenticated() and cartObj.user is None:
    #         cartObj.user = request.user
    #         cartObj.save()
    # else:
    #     cartObj = Cart.objects.newCart(user=request.user)
    #     request.session['cartId'] = cartObj.id 

    

    #print(request.session.session_key)
    #request.session.set_expiry(300)

def cartUpdate(request):
    print(request.POST)
    productId = request.POST.get('productId')
    if productId is not None:

        try:
            productObj = Product.objects.get(id=productId)
        except Product.DoesNotExist:
            redirect("carts:home")
        
        cartObj, newObj = Cart.objects.createNewOrGet(request)
        if productObj in cartObj.products.all():
            cartObj.products.remove(productObj)
        else:
            cartObj.products.add(productObj)
        request.session['nItems'] = cartObj.products.all().count()
        print(request.session['nItems'])
    return redirect("carts:home")

def checkoutHome(request):
    cartObj, cartCreated = Cart.objects.createNewOrGet(request)
    print(cartObj, cartCreated)
    orderObj = None
    if cartCreated or cartObj.products.count() == 0:
        redirect("carts:home")
    else:
        orderObj, newOrderObj = Order.objects.get_or_create(cart=cartObj)
        print(orderObj, newOrderObj)
    
    user = request.user
    billingProfile = None
    loginForm = LoginForm()
    guestForm = GuestForm()
    guestEmailId = request.session.get('guestEmailId')

    if user.is_authenticated():
        billingProfile, bProfcreated = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guestEmailId is not None:
        guestEmailObj = GuestEmail.objects.get(id=guestEmailId)
        billingProfile, guestProfcreated = GuestEmail.objects.get_or_create(email=guestEmailObj.email)
    else:
        pass
    
    context = {
        "object": orderObj,
        "billingProfile": billingProfile,
        "loginForm": loginForm,
        "guestForm": guestForm
        }
    return render(request, 'carts/checkout.html', context)

