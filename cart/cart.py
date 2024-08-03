from app.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        #Get request
        self.request = request
        
        # get session key
        cart = self.session.get('session_key')
        
        # if the user is new, create a session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
            
        # making cart available on all pages of the site
        self.cart = cart
        
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        #deal with logged in users
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert single quotation into double
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart = str(carty))
            self.session.modified = True
            
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        #deal with logged in users
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert single quotation into double
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart = str(carty))
            self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # getting the ids from the cart
        product_ids = self.cart.keys()
        # use the ids to loook up product from the DB
        products = Product.objects.filter(id__in= product_ids)
        
        return products 
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        # get the cart
        ourcart = self.cart
        # update the dictionary/cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        #deal with logged in users
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert single quotation into double
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart = str(carty))
            self.session.modified = True
        
        
        
        thing = self.cart
        return thing
    
    
    def delete(self,product):
        product_id = str(product)
        #delete from the cart dictionary
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        #deal with logged in users
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert single quotation into double
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart = str(carty))
            self.session.modified = True
        
    
    
    def cart_total(self):
        #get product ids
        product_ids = self.cart.keys()
        #lookup the matching products from the Product model
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        #looping through the cart items 
        for key, value in quantities.items():
            #converting key value in the cart into integer to compar with product.id
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total= total +(product.sale_price * value)
                    else:
                        total= total +(product.price * value)
                        
                
        return total
        