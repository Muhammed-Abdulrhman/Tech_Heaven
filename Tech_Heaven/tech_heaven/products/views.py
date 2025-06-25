from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
# Create your views here.

@login_required(login_url='login')
def home_view(request):
    categories = Category.objects.all()
    latest_products = Product.objects.order_by('-id')[:12]
    for product in latest_products:
          product.final_price = product.price - product.discount
    return render(request, 'pages/home.html', {"username": request.user.username, 'latest_products':latest_products, 'categories':categories})

@login_required(login_url='login')
def category_view(request, category_name):
    categories = Category.objects.all()
    category = get_object_or_404(Category, title=category_name)
    laptops = Product.objects.filter(category=category).order_by('id')[:20]
    for product in laptops:
          product.final_price = product.price - product.discount
    return render(request, 'pages/category.html', {'category_products': laptops,'category': category, 'categories':categories})

@login_required(login_url='login')
def product_view(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    comments = Comments.objects.filter(product=product_id).order_by('-id')
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        content = request.POST.get('content')
        if quantity:
            quantity = int(quantity)
            cart_item, created = Cart.objects.get_or_create(
                client=request.user,
                product=product,
                defaults={
                    'quantity': quantity,
                    'price': product.price,
                    'total_price': product.price * quantity,
                }
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.total_price = cart_item.price * cart_item.quantity
                cart_item.save()
        elif content:
            comment = Comments.objects.create(
                client=request.user,
                product=product,
                content=content,
            )
            comment.save()
    return render(request, 'pages/product.html', {'product': product, 'categories': categories, 'comments': comments})

def cart_view(request):
    cart = Cart.objects.filter(client=request.user).order_by('-id')
    total = sum(item.total_price for item in cart)
    return render(request, 'pages/cart.html',{'cart':cart, 'total':total})

@login_required(login_url='login')
def delete_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, client=request.user)
    cart_item.delete()
    return redirect('cart')
