from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm 
from django import forms 




# Create your views here.

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
            messages.success(req, ('You have registered succcessfully!!!'))
            return redirect('home')
        else:
            messages.success(req, ('There was a problem please try again'))
            return redirect('register')
    else:
        return render(req, 'register.html', {'form':form})
    
    
   