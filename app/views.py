from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePassswordForm, UserInfoForm
from django import forms 
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress




# Create your views here.

    

def update_user(req):
    if req.user.is_authenticated:
        current_user = User.objects.get(id=req.user.id)
        user_form = UpdateUserForm(req.POST or None, instance = current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(req, current_user)
            messages.success(req, "User Has Been Updated")
            return redirect('home')
        return render(req, 'update_user.html', {'user_form':user_form})
    else:
         messages.success(req, "You must be logged in to access this page")
         return redirect('home')
    
    
def update_password(req):
    return render(req, 'update_password.html', {})


def sales(req):
    products = Product.objects.all()
    return render(req, 'sales.html', {'products': products})



def category(req,foo):
    foo = foo.replace('-', ' ')
    #grabing the category model
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(req, 'category.html', {'products': products,'category':category})
    except: 
        messages.success(req, ("this category doesn't exist..."))
        return redirect('home')


def product(req,pk):
    product = Product.objects.get(id=pk)
    return render(req, 'product.html', {'product': product})


def home(req):
    products = Product.objects.all()
    return render(req, 'home.html', {'products': products})

def about(req):
    return render(req, 'about.html', {})


def login_user(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            #for the shopping cart
            current_user = Profile.objects.get(user__id=req.user.id)
            #get their saved cart
            saved_cart = current_user.old_cart
            #convert string into py dictionary
            if saved_cart:
            #convert into dictionary
                converted_cart = json.loads(saved_cart)
                cart = Cart(req)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
                    
            messages.success(req, ('You have been logged in'))
            return redirect('home')
    
        else:
             messages.success(req, ('There was an error'))
             return redirect('login')
        
    else:
        return render(req, 'login.html', {})
 
 
def logout_user(req):
    logout(req)
    messages.success(req, ('You Have Been Log Out'))
    return redirect('home')

def register_user(req):
    form = SignUpForm()
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in 
            user = authenticate(username=username, password=password)
            login(req, user)
            messages.success(req, ('Username created Please fill out your information'))
            return redirect('update_info')
        else:
            messages.success(req, ('There was a problem please try again'))
            return redirect('register')
    else:
        return render(req, 'register.html', {'form':form})
    
    
   
def update_password(req):
    if req.user.is_authenticated:
        current_user = req.user
        #did they fill out the form
        if req.method == 'POST':
            form = ChangePassswordForm(current_user, req.POST)
            #is he form valid
            if form.is_valid():
                form.save()
                messages.success(req, 'Your Password is Updated')
                login(req, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(req,error)
                    return redirect('update_password')
        else:
            form = ChangePassswordForm(current_user)
            return render(req,'update_password.html',{'form':form})
    else:
        messages.success(req, ('You must be logged in to see this page'))
        return redirect('home')
    
def update_info(req):
    if req.user.is_authenticated:
        current_user = Profile.objects.get(user__id=req.user.id)
       # shipping_user = ShippingAddress.objects.get(id=req.user.id)
        form = UserInfoForm(req.POST or None, instance = current_user)
        #shipping_form = ShippingForm(req.POST or None, instance = shipping_user)
        
        if form.is_valid():
            form.save()
            
            messages.success(req, "Your Info Has Been Updated")
            return redirect('home')
        return render(req, 'update_info.html', {'form':form,})
    else:
         messages.success(req, "You must be logged in to access this page")
         return redirect('home')
     
     
     
     
     
     
     
def search(req):
    #determin if they filled out the form
    if req.method == 'POST':
        searched = req.POST['searched']
        #query the product DB
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
             messages.success(req, "Sorry we coudn't find a match for your search")
        return render(req, 'search.html', {'searched': searched})
    else:
        return render(req, 'search.html', {})