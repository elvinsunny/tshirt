from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.contrib.auth import authenticate,logout
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .forms import CustomerSignUpForm, SellerSignUpForm,CustomerLoginForm, SellerLoginForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('customer_login') # Redirect to customer dashboard
    else:
        form = CustomerSignUpForm()
    return render(request, 'register.html', {'form': form})

# def customer_login(request):
#     if request.method == 'POST':
#         form = CustomerLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None and user.is_customer:
#                 auth_login(request, user)
#                 return redirect('home')  # Redirect to customer dashboard
#             else:
#                 # Handle invalid login for customers
#                 return render(request, 'login.html', {'form': form, 'error_message': 'Invalid credentials'})
#     else:
#         form = CustomerLoginForm()
#     return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomerLoginForm

def customer_login(request):
    error_message = None
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Assuming you have a custom user attribute 'is_customer'
                if hasattr(user, 'is_customer') and user.is_customer:
                    auth_login(request, user)
                    return redirect('home')  # Redirect to customer dashboard
                else:
                    error_message = 'Invalid customer credentials'
            else:
                error_message = 'Invalid credentials'
    else:
        form = CustomerLoginForm()

    return render(request, 'login.html', {'form': form, 'error_message': error_message})




def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will handle creating both CustomUser and Seller
            auth_login(request, user)
            return redirect('seller_login') # Redirect to seller login
    else:
        form = SellerSignUpForm()
    return render(request, 'seller_register.html', {'form': form})




from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    auth_login(request, user)
                    return redirect('hom')  # Redirect to home for superuser
                elif user.is_seller:
                    auth_login(request, user)
                    return redirect('seller_dashboard')  # Redirect to seller dashboard
            # Handle invalid login for both superuser and sellers
            messages.error(request, 'Invalid credentials')
            return render(request, 'seller_login.html', {'form': form})
    else:
        form = SellerLoginForm()
    return render(request, 'seller_login.html', {'form': form})




def logout_view(request):
    # Use the built-in logout function to log the user out
    logout(request)
    return redirect('home')


from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from .forms import ForgotPasswordForm

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=None,
                email_template_name='password_reset_email.html',
                subject_template_name='password_reset_subject.txt',
                request_template_name='password_reset_form.html',
            )
            # Redirect to a page indicating that the password reset email has been sent
            return render(request, 'password_reset_sent.html')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})





from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render,redirect


from .models import Category,Product
from .forms import ProductForm

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages





def home(request):
    categories = Category.objects.all()

    # Create a dictionary to store products for each category
    category_products = {}
    for category in categories:
        products = Product.objects.filter(category=category)
        category_products[category] = products

    context = {
        'user': request.user,
        'categories': categories,
        'category_products': category_products,
    }

    return render(request, 'index1.html', context)



from django.shortcuts import render
from django.db.models import Q
from .models import Product

def search_results(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            # Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        products = Product.objects.none()

    return render(request, 'search_results.html', {'products': products, 'query': query})



def hom(request):
    categories = Category.objects.all()

    # Create a dictionary to store products for each category
    category_products = {}
    for category in categories:
        products = Product.objects.filter(category=category)
        category_products[category] = products

    context = {
        'categories': categories,
        'category_products': category_products,
    }

    return render(request, 'admin_index.html', context)





def category_list(request):
    categories = Category.objects.all()

    # Group products by category
    category_products = {}
    for category in categories:
        category_products[category] = Product.objects.filter(category=category)

    return render(request, 'category_list.html', {'category_products': category_products})



# def view(request):
#     products = Product.objects.all()
#     return render(request,'view.html',{"products":products})


def view(request):
    products = Product.objects.filter(status='approved')
    return render(request, 'view.html', {"products": products})
# views.py
from django.shortcuts import render
from .models import Order

def view_orders(request):
    orders = Order.objects.all().select_related('user', 'shipping_details').prefetch_related('products')
    return render(request, 'view_orders.html', {'orders': orders})


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Seller

def approved_sellers(request):
    sellers = Seller.objects.filter(is_approved=True)
    return render(request, 'approved_sellers.html', {'sellers': sellers})

def delete_seller(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    seller.delete()
    return redirect(reverse('approved_sellers'))



def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})



from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from django.contrib import messages


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            
            # Save quantities for each size variant
            product.quantity_S = form.cleaned_data['quantity_S']
            product.quantity_M = form.cleaned_data['quantity_M']
            product.quantity_L = form.cleaned_data['quantity_L']
            product.quantity_XL = form.cleaned_data['quantity_XL']
            
            product.save()
            
            messages.success(request, "Product added successfully.")
            return redirect('view')
    else:
        form = ProductForm()

    return render(request, 'addproduct.html', {'form': form})





from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Get the form instance without saving it yet
            updated_product = form.save(commit=False)
            
            # Retrieve the input quantities from the form
            quantity_S = form.cleaned_data.get('quantity_S', 0)
            quantity_M = form.cleaned_data.get('quantity_M', 0)
            quantity_L = form.cleaned_data.get('quantity_L', 0)
            quantity_XL = form.cleaned_data.get('quantity_XL', 0)
            
            # Add the input quantities to the existing quantities
            updated_product.quantity_S += quantity_S
            updated_product.quantity_M += quantity_M
            updated_product.quantity_L += quantity_L
            updated_product.quantity_XL += quantity_XL
            
            # Save the updated product
            updated_product.save()

            return redirect('view')  # Redirect to the appropriate URL after updating
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_update.html', {'form': form, 'product': product})

from django.shortcuts import redirect, get_object_or_404
from .models import Product

def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Delete the product
    product.delete()

    return redirect('view')


from django.shortcuts import render, redirect
from django.contrib import messages


# ... (your existing code)

@login_required(login_url='customer_login')
def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    # Calculate the total quantity
    total_quantity = sum(item.quantity for item in cart_items)

    # Calculate subtotals for each cart item
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity

    total_cart_price = sum(item.subtotal for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_cart_price': total_cart_price, 'total_quantity': total_quantity})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CartItem

@login_required(login_url='customer_login')
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        size = request.POST.get('size')

        if not size:
            messages.error(request, "Please select a size.")
            return redirect('product_detail', product_id=product.id)

        # Determine the appropriate quantity field based on the selected size
        quantity_field = f'quantity_{size}'
        quantity_value = getattr(product, quantity_field)

        if quantity_value == 0:
            messages.error(request, "This size is out of stock.")
            return redirect('product_detail', product_id=product.id)

        # Check if the maximum quantity for the selected variant is already in the cart
        cart_items_with_variant = CartItem.objects.filter(user=user, product=product, size=size)
        total_quantity_in_cart = sum(cart_item.quantity for cart_item in cart_items_with_variant)

        if total_quantity_in_cart >= quantity_value:
            messages.error(request, "This variant is already in your cart.")
            return redirect('product_detail', product_id=product.id)

        # Create or update cart item with the selected size
        cart_item, created = CartItem.objects.get_or_create(user=user, product=product, size=size)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, "Product added to cart.")
        return redirect('cart')
    
    # Handle GET request (redirect to home or display an error message)
    messages.error(request, "Invalid request.")
    return redirect('home')





from django.shortcuts import get_object_or_404

def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    # Check if the quantity in the cart exceeds the original variant size quantity
    variant_quantity_field = f'quantity_{cart_item.size}'
    original_variant_quantity = getattr(cart_item.product, variant_quantity_field)
    
    if cart_item.quantity < original_variant_quantity:
        # Increase the quantity in the cart
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')



def decrease_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)

    # Check if the cart item's quantity is greater than 1 before decreasing it
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')







def calculate_cart_total_price(cart_items):
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.product.price * cart_item.quantity
    return total_price


def delete_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        product = cart_item.product


        cart_item.delete()

        messages.success(request, f"{product.name} has been removed from your cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in your cart.")

    return redirect('cart')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ShippingDetailsForm
from .models import CartItem, ShippingDetails

@login_required
def enter_address(request):
    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST)
        if form.is_valid():
            shipping_details = form.save(commit=False)
            shipping_details.user = request.user
            shipping_details.save()
            return redirect('checkout')
    else:
        form = ShippingDetailsForm()
    return render(request, 'enter_address.html', {'form': form})


# from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.http import HttpResponseServerError
# from .forms import ShippingDetailsForm
# from .models import Order, OrderItem, ShippingDetails, CartItem

# def checkout(request):
#     if request.method == 'POST':
#         # Process the shipping details form
#         form = ShippingDetailsForm(request.POST)
#         if form.is_valid():
#             # Save the shipping details
#             shipping_details = form.save(commit=False)
#             shipping_details.user = request.user
#             shipping_details.save()
            
#             # Create the order
#             order = Order.objects.create(user=request.user, shipping_details=shipping_details, total_price=0)
            
#             # Retrieve the user's cart items and associate them with the order
#             cart_items = CartItem.objects.filter(user=request.user)
#             order_items = []
#             for cart_item in cart_items:
#                 if cart_item.product.price is None:
#                     # Log an error if the product price is missing
#                     return HttpResponseServerError("Product price is missing")
#                 order_item = OrderItem(
#                     order=order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     price=cart_item.product.price  # Assign product price to OrderItem
#                 )
#                 order_items.append(order_item)
#             OrderItem.objects.bulk_create(order_items)
            
#             # Calculate the total price based on individual product prices
#             total_price = sum(item.product.price * item.quantity for item in cart_items)
#             order.total_price = total_price
#             order.save()
            
#             # Clear the user's cart
#             cart_items.delete()
            
#             # Redirect to the order detail page
#             order_detail_url = reverse('order_detail', kwargs={'order_id': order.id})
#             return redirect(order_detail_url)
#     else:
#         form = ShippingDetailsForm()
    
#     return render(request, 'checkout.html', {'form': form})



# from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.http import HttpResponseServerError
# from .forms import ShippingDetailsForm
# from .models import Order, OrderItem, ShippingDetails, CartItem, OrderStatus

# def checkout(request):
#     if request.method == 'POST':
#         # Process the shipping details form
#         form = ShippingDetailsForm(request.POST)
#         if form.is_valid():
#             # Save the shipping details
#             shipping_details = form.save(commit=False)
#             shipping_details.user = request.user
#             shipping_details.save()
            
#             # Create the order
#             order = Order.objects.create(user=request.user, shipping_details=shipping_details, total_price=0)
            
#             # Retrieve the user's cart items and associate them with the order
#             cart_items = CartItem.objects.filter(user=request.user)
#             order_items = []
#             order_statuses = []
#             for cart_item in cart_items:
#                 if cart_item.product.price is None:
#                     # Log an error if the product price is missing
#                     return HttpResponseServerError("Product price is missing")
#                 order_item = OrderItem(
#                     order=order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     price=cart_item.product.price  # Assign product price to OrderItem
#                 )
#                 order_items.append(order_item)
                
#                 # Create an OrderStatus for each OrderItem
#                 order_status = OrderStatus(
#                     order=order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     pstatus='processing'  # Default status
#                 )
#                 order_statuses.append(order_status)
                
#             OrderItem.objects.bulk_create(order_items)
#             OrderStatus.objects.bulk_create(order_statuses)
            
#             # Calculate the total price based on individual product prices
#             total_price = sum(item.product.price * item.quantity for item in cart_items)
#             order.total_price = total_price
#             order.save()
            
#             # Clear the user's cart
#             cart_items.delete()
            
#             # Redirect to the order detail page
#             order_detail_url = reverse('order_detail', kwargs={'order_id': order.id})
#             return redirect(order_detail_url)
#     else:
#         form = ShippingDetailsForm()
    
#     return render(request, 'checkout.html', {'form': form})




from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseServerError
from .forms import ShippingDetailsForm
from .models import Order, OrderItem, ShippingDetails, CartItem, OrderStatus, Product

# def checkout(request):
#     if request.method == 'POST':
#         # Process the shipping details form
#         form = ShippingDetailsForm(request.POST)
#         if form.is_valid():
#             # Save the shipping details
#             shipping_details = form.save(commit=False)
#             shipping_details.user = request.user
#             shipping_details.save()
            
#             # Create the order
#             order = Order.objects.create(user=request.user, shipping_details=shipping_details, total_price=0)
            
#             # Retrieve the user's cart items and associate them with the order
#             cart_items = CartItem.objects.filter(user=request.user)
#             order_items = []
#             order_statuses = []
#             for cart_item in cart_items:
#                 if cart_item.product.price is None:
#                     # Log an error if the product price is missing
#                     return HttpResponseServerError("Product price is missing")
                
#                 # Decrease the product quantity based on the size
#                 product = cart_item.product
#                 if cart_item.size == 'S':
#                     if product.quantity_S < cart_item.quantity:
#                         return HttpResponseServerError("Not enough stock for Small size")
#                     product.quantity_S -= cart_item.quantity
#                 elif cart_item.size == 'M':
#                     if product.quantity_M < cart_item.quantity:
#                         return HttpResponseServerError("Not enough stock for Medium size")
#                     product.quantity_M -= cart_item.quantity
#                 elif cart_item.size == 'L':
#                     if product.quantity_L < cart_item.quantity:
#                         return HttpResponseServerError("Not enough stock for Large size")
#                     product.quantity_L -= cart_item.quantity
#                 elif cart_item.size == 'XL':
#                     if product.quantity_XL < cart_item.quantity:
#                         return HttpResponseServerError("Not enough stock for Extra Large size")
#                     product.quantity_XL -= cart_item.quantity
                
#                 product.save()
                
#                 order_item = OrderItem(
#                     order=order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     price=cart_item.product.price  # Assign product price to OrderItem
#                 )
#                 order_items.append(order_item)
                
#                 # Create an OrderStatus for each OrderItem
#                 order_status = OrderStatus(
#                     order=order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     pstatus='processing'  # Default status
#                 )
#                 order_statuses.append(order_status)
                
#             OrderItem.objects.bulk_create(order_items)
#             OrderStatus.objects.bulk_create(order_statuses)
            
#             # Calculate the total price based on individual product prices
#             total_price = sum(item.product.price * item.quantity for item in cart_items)
#             order.total_price = total_price
#             order.save()
            
#             # Clear the user's cart
#             cart_items.delete()
            
#             # Redirect to the order detail page
#             order_detail_url = reverse('order_detail', kwargs={'order_id': order.id})
#             return redirect(order_detail_url)
#     else:
#         form = ShippingDetailsForm()
    
#     return render(request, 'checkout.html', {'form': form})





from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def checkout(request):
    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST)
        if form.is_valid():
            shipping_details = form.save(commit=False)
            shipping_details.user = request.user
            shipping_details.save()
            
            order = Order.objects.create(user=request.user, shipping_details=shipping_details, total_price=0)
            
            cart_items = CartItem.objects.filter(user=request.user)
            order_items = []
            order_statuses = []
            for cart_item in cart_items:
                if cart_item.product.price is None:
                    return HttpResponseServerError("Product price is missing")
                
                product = cart_item.product
                if cart_item.size == 'S':
                    if product.quantity_S < cart_item.quantity:
                        return HttpResponseServerError("Not enough stock for Small size")
                    product.quantity_S -= cart_item.quantity
                elif cart_item.size == 'M':
                    if product.quantity_M < cart_item.quantity:
                        return HttpResponseServerError("Not enough stock for Medium size")
                    product.quantity_M -= cart_item.quantity
                elif cart_item.size == 'L':
                    if product.quantity_L < cart_item.quantity:
                        return HttpResponseServerError("Not enough stock for Large size")
                    product.quantity_L -= cart_item.quantity
                elif cart_item.size == 'XL':
                    if product.quantity_XL < cart_item.quantity:
                        return HttpResponseServerError("Not enough stock for Extra Large size")
                    product.quantity_XL -= cart_item.quantity
                
                product.save()
                
                order_item = OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                order_items.append(order_item)
                
                order_status = OrderStatus(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    pstatus='processing'
                )
                order_statuses.append(order_status)
                
            OrderItem.objects.bulk_create(order_items)
            OrderStatus.objects.bulk_create(order_statuses)
            
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            order.total_price = total_price
            order.save()
            
            cart_items.delete()
            
            # Send email confirmation
            subject = 'Order Confirmation'
            html_message = render_to_string('order_confirmation_email.html', {'order': order, 'order_items': order_items})
            plain_message = strip_tags(html_message)
            from_email = 'your_email@gmail.com'
            to = request.user.email
            
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            
            order_detail_url = reverse('order_detail', kwargs={'order_id': order.id})
            return redirect(order_detail_url)
    else:
        form = ShippingDetailsForm()
    
    return render(request, 'checkout.html', {'form': form})





# views.py

from django.shortcuts import render, get_object_or_404
from .models import Order

def order_detail(request, order_id):
    # Retrieve the order with the given ID from the database
    order = get_object_or_404(Order, id=order_id)
    
    # Render the order detail template with the order object
    return render(request, 'order_detail.html', {'order': order})





# from django.shortcuts import render
# from .models import Order

# def order_history(request):
#     orders = Order.objects.filter(user=request.user)
#     return render(request, 'order_history.html', {'orders': orders})


#views.py

# from django.shortcuts import render
# from .models import Order, OrderStatus

# def order_history(request):
#     orders = Order.objects.filter(user=request.user)
#     order_statuses = OrderStatus.objects.filter(order__in=orders)
#     return render(request, 'order_history.html', {'orders': orders, 'order_statuses': order_statuses})

from django.shortcuts import render
from .models import Order, OrderStatus

def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set__product')
    for order in orders:
        for item in order.orderitem_set.all():
            status = OrderStatus.objects.filter(order=order, product=item.product).first()
            item.status = status.pstatus if status else 'Pending'

    return render(request, 'order_history.html', {'orders': orders})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# def list_users(request):
#     users = User.objects.all()
#     return render(request, "list_users.html", {"users": users})

from .models import CustomUser

def list_users(request):
    # Exclude superuser (admin) and sellers from the list
    users = CustomUser.objects.filter(is_superuser=False, is_customer=True)

    return render(request, "list_users.html", {"users": users})

def remove_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        messages.success(request, f"User {user.username} has been removed.")
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('list_users')





def order_list(request):
    orders = Order.objects.all()
    status_choices = OrderStatus.STATUS_CHOICES

    context = {
        'orders': orders,
        'status_choices': status_choices,
    }

    return render(request, 'order_list.html', context)


from django.shortcuts import get_object_or_404


def change_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=order_id)
        new_status = request.POST.get('status')
        
        if new_status not in dict(OrderStatus.STATUS_CHOICES):
            messages.error(request, "Invalid status.")
            return redirect('order_list')
        
        order_status, created = OrderStatus.objects.get_or_create(order=order)
        order_status.status = new_status
        order_status.save()
        
        messages.success(request, "Order status updated successfully.")
        return redirect('order_list')
    return redirect('order_list')








from django.contrib import messages

def my_view(request):
    # Example of adding different types of messages
    messages.success(request, 'This is a success message.')
    messages.error(request, 'This is an error message.')
    messages.warning(request, 'This is a warning message.')
    messages.info(request, 'This is an info message.')


# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer

def view_profile(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the user is a customer
        if hasattr(request.user, 'customer_profile'):
            # Get the customer profile
            customer = request.user.customer_profile
            # Get the username
            username = request.user.username
            return render(request, 'view_profile.html', {'customer': customer, 'username': username})
        else:
            # If the user is not a customer, redirect to the customer login page
            return redirect('customer_login')  # Assuming 'customer_login' is the name of your customer login URL pattern
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect('customer_login')  


from django.shortcuts import render, redirect
from .forms import EditProfileForm,EditUserForm
from django.contrib.auth.decorators import login_required



from django.contrib.auth.forms import PasswordChangeForm

@login_required
def edit_profile(request):
    user = request.user
    customer = user.customer_profile

    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, instance=customer)
        password_form = PasswordChangeForm(user, request.POST)
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            return redirect('view_profile')
    else:
        profile_form = EditProfileForm(instance=customer)
        password_form = PasswordChangeForm(user)

    return render(request, 'edit_profile.html', {'profile_form': profile_form, 'password_form': password_form})






from django.shortcuts import render
from Myapp.models import CustomUser

def user_order_status(request):
    # Retrieve all users along with their orders and order statuses
    users = CustomUser.objects.all()

    context = {
        'users': users,
    }

    return render(request, 'user_order_status.html', context)









# from django.shortcuts import render
# from django.contrib import messages
# from .models import Product

# def seller_dashboard(request):
#     # Fetch all products belonging to the seller
#     products = Product.objects.filter(seller=request.user.seller_profile)
    
#     # Check for products with quantity 5 or below and send a reorder alert
#     low_quantity_products = []
#     for product in products:
#         if product.quantity_S <= 5 or product.quantity_M <= 5 or product.quantity_L <= 5 or product.quantity_XL <= 5:
#             low_quantity_products.append(product)
    
#     if low_quantity_products:
#         messages.warning(request, f"Alert: You have {len(low_quantity_products)} product(s) with quantity 5 or below. Please update the quantity.")

#     return render(request, 'seller_dashboard.html', {'products': products})


# from django.shortcuts import render
# from .models import Product

# def seller_dashboard(request):
#     # Fetch all products belonging to the seller
#     products = Product.objects.filter(seller=request.user.seller_profile)
    
#     return render(request, 'seller_dashboard.html', {'products': products})

from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def seller_dashboard(request):
    # Fetch only the approved products belonging to the seller
    products = Product.objects.filter(seller=request.user.seller_profile, status='approved')
    
    return render(request, 'seller_dashboard.html', {'products': products})


# views.py

from django.shortcuts import render
from .models import Product

def reorder_level_alerts(request):
    seller = request.user.seller_profile
    products = Product.objects.filter(seller=seller)
    low_quantity_products = []

    for product in products:
        min_quantity = min(product.quantity_S, product.quantity_M, product.quantity_L, product.quantity_XL)
        if min_quantity <= product.reorder_level:
            low_quantity_products.append(product)

    return render(request, 'reorder_level_alerts.html', {'products': low_quantity_products})



# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Seller

@login_required
def seller_profile(request):
    # Fetch the seller's profile for the logged-in user
    seller = get_object_or_404(Seller, user=request.user)

    return render(request, 'seller_profile.html', {'seller': seller})


# views.py
from django.shortcuts import render, redirect
from .forms import EditSellerProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_seller_profile(request):
    user = request.user
    seller = user.seller_profile

    if request.method == 'POST':
        form = EditSellerProfileForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            return redirect('seller_profile')
    else:
        form = EditSellerProfileForm(instance=seller)

    return render(request, 'edit_seller_profile.html', {'form': form})




# views.py
from django.shortcuts import render
from .models import Product

def seller_products(request):
    # Retrieve all approved products belonging to the logged-in seller
    seller = request.user.seller_profile
    products = Product.objects.filter(seller=seller, status='approved')
    return render(request, 'seller_products.html', {'products': products})



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import SellerProductForm

def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = SellerProductForm(request.POST, instance=product)
        if form.is_valid():
            # Save the form data
            form.save()
            return redirect('seller_dashboard')  # Redirect to the seller dashboard
    else:
        form = SellerProductForm(instance=product)

    return render(request, 'product_update.html', {'form': form, 'product': product})




# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')  # Redirect to the seller products page

    return render(request, 'delete_product_confirm.html', {'product': product})









# from django.shortcuts import render, get_object_or_404, redirect
# from .models import OrderItem, OrderStatus

# def seller_order_list(request):
#     if not request.user.is_authenticated or not request.user.is_seller:
#         return redirect('login')
    
#     orders = OrderItem.objects.filter(product__seller=request.user.seller_profile)
#     return render(request, 'seller_order_list.html', {'orders': orders})

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
# from .models import OrderItem, OrderStatus


from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, OrderStatus

def seller_order_list(request):
    if not request.user.is_authenticated or not request.user.is_seller:
        return redirect('login')
    
    orders = OrderItem.objects.filter(product__seller=request.user.seller_profile).select_related('order', 'order__user', 'order__shipping_details')
    return render(request, 'seller_order_list.html', {'orders': orders})




def update_order_status(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    try:
        order_status = OrderStatus.objects.get(order=order_item.order, product=order_item.product)
    except OrderStatus.DoesNotExist:
        return HttpResponse("OrderStatus not found for this order item", status=404)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [status[0] for status in OrderStatus.STATUS_CHOICES]:
            order_status.pstatus = new_status
            order_status.save()
            return redirect('seller_order_list')

    return render(request, 'update_order_status.html', {'order_status': order_status, 'order_item': order_item})














from django.shortcuts import render, get_object_or_404
from .models import Product, Order

def product_customers(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    orders = Order.objects.filter(cart_items__product=product)
    return render(request, 'product_customers.html', {'product': product, 'orders': orders})




# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def pending_products(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('status_'):
                product_id = key.split('_')[1]
                product = Product.objects.get(id=product_id)
                product.status = value
                product.save()
        return redirect('pending_products')

    pending_products = Product.objects.filter(status='pending')
    return render(request, 'pending_products.html', {'pending_products': pending_products})








from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Seller

@login_required
@user_passes_test(lambda u: u.is_superuser)
def new_suppliers(request):
    if request.method == 'POST':
        approve_ids = request.POST.getlist('approve')
        reject_ids = request.POST.getlist('reject')

        for seller_id in approve_ids:
            try:
                seller = Seller.objects.get(pk=seller_id)
                seller.is_approved = True
                seller.save()
                messages.success(request, f'Seller {seller.user.username} approved.')
            except Seller.DoesNotExist:
                messages.error(request, f'Seller with ID {seller_id} does not exist.')

        for seller_id in reject_ids:
            try:
                seller = Seller.objects.get(pk=seller_id)
                seller.delete()
                messages.success(request, f'Seller {seller.user.username} rejected and deleted.')
            except Seller.DoesNotExist:
                messages.error(request, f'Seller with ID {seller_id} does not exist.')

        return redirect('new_suppliers')

    new_suppliers = Seller.objects.filter(is_approved=False)
    return render(request, 'new_suppliers.html', {'new_suppliers': new_suppliers})



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SellerProductForm
from .models import Product

def add_product(request):
    if request.user.is_authenticated and request.user.is_seller:
        # Check if the seller is approved
        if not request.user.seller_profile.is_approved:
            messages.error(request, 'Your account is not approved yet. Please wait for admin approval.')
            return redirect('seller_dashboard')  # Redirect to seller dashboard or any other appropriate URL
            
        if request.method == 'POST':
            form = SellerProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                seller = request.user.seller_profile  # Fetch the seller profile associated with the logged-in user
                product.seller = seller
                product.save()
                return redirect('seller_dashboard')  # Redirect to the home page or any other appropriate URL after adding the product
        else:
            form = SellerProductForm()
        
        return render(request, 'add_product.html', {'form': form})
    else:
        # Redirect to login page if not logged in as seller
        return redirect('seller_login')


