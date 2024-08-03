from django.contrib import admin
from .models import Category, Customer, Order, Product, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile
    
#extend the user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', ' first_name', 'last_name', 'email']
    inlines = [ProfileInline]
    
#unregister the old model
admin.site.unregister(User)
# register the new model
admin.site.register(User, UserAdmin)