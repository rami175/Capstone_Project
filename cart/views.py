from django.shortcuts import render, get_object_or_404
from .cart import Cart
from app.models import Product
from django.http import JsonResponse
# Create your views here.

def cart_summary(req):
    # get the cart
    cart =Cart(req)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    total = cart.cart_total()
    return render(req, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "total": total})



def cart_add(req):
    # get the cart
    cart = Cart(req)
    # test for POST
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product_qty = int(req.POST.get('product_qty'))
        # lookup product in the DB
        product = get_object_or_404(Product, id=product_id)
        # save the session
        cart.add(product=product, quantity=product_qty)
        # get cart quantity
        cart_quantity = cart.__len__()
        
        #  return a response
        # reponse = JsonResponse({'Product Name: ': product.name})
        reponse = JsonResponse({'qty': cart_quantity})
        return reponse
    
    
    
    

def cart_delete(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        #call delete function
        cart.delete(product=product_id)
        
        #we don't need to return anything 
        response = JsonResponse({'product': product_id})
        return response






def cart_update(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product_qty = int(req.POST.get('product_qty'))
        
        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({'qty': product_qty})
        return response