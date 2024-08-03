from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views




urlpatterns = [
   path('', views.home, name='home'),
   path('about/', views.about, name='about'),
   path('login/', views.login_user, name='login'),
   path('logout/', views.logout_user, name='logout'),
   path('flogout/', auth_views.LogoutView.as_view(), name='flogout'),
   path('social-auth/', include('social_django.urls', namespace='social')),
   path('register/', views.register_user, name='register'),
   path('product/<int:pk>', views.product, name='product'),
   path('category/<str:foo>', views.category, name='category'),
   
]