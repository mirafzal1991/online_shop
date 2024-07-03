from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from shop.forms import LoginForm,CommentModelForm,OrderModelForm


from shop.forms import ProductModelForm
from shop.models import Product
from django.db.models import Q

# Create your views here.

def product_list(request):
    search_query = request.GET.get('search')
    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query))
    else:
        products = Product.objects.all()

    context = {'products': products}
    return render(request,'shop/home.html',context)

@login_required(login_url='login')
def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {

        'form': form,

    }
    return render(request, 'shop/add-product.html', context)

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    category = product.category
    related_products = Product.objects.filter(category=category).exclude(id=product_id)
    comments = product.comments.filter(is_possible=True)

    context = {
        'product': product,
        'comments': comments,
        'related_products':related_products,

    }
    return render(request,'shop/detail.html', context)
@login_required(login_url='login')
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(instance=product, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

            return redirect('products')
    context = {
        'form': form,
    }
    return render(request, 'shop/edit-product.html', context)
@login_required(login_url='login')
def delete_product(request, product_id):
    customer = Product.objects.get(id=product_id)
    if customer:
        customer.delete()

        return redirect('products')

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('products')
    else:
        form = LoginForm()

    return render(request, 'shop/login.html', {'form': form})

def logout_page(request):
    if request.method == 'GET':
        logout(request)
        return redirect('products')
    return render(request, 'shop/logout.html')

def add_comment(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            comment.product = product
            comment.save()
            return redirect('product_detail', product_id)
    else:
        form = CommentModelForm(request.GET)

    return render(request, 'shop/detail.html', {'form': form, 'product': product})

def add_order(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)

            new_order.product = product
            new_order.save()
            return redirect('product_detail',product_id)
    else:
        form = OrderModelForm(request.GET)

    return render(request,'shop/detail.html',{'form': form, 'product': product})


