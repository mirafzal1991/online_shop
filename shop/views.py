from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from shop.forms import LoginForm,CommentModelForm,OrderModelForm,RegisterModelForm, EmailForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from shop.forms import ProductModelForm
from shop.models import Product
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from shop.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages

# Create your views here.

def product_list(request):

    search_query = request.GET.get('search')
    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query))
    else:
        page = request.GET.get('page','')
        products = Product.objects.all()
        paginator = Paginator(products, 3)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)


    context = {'products': products, 'page_obj': page_obj}
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
    product = Product.objects.get(id=product_id)
    if product:
        product.delete()

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

def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            if not user.is_active:
                current_site = get_current_site(request)
                user = request.user
                email = request.user.email
                subject = "Verify Email"
                message = render_to_string('shop/verify_email_message.html', {
                    'request': request,
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(
                    subject, message, to=[email]
                )
                email.content_subtype = 'html'
                email.send()
                return redirect('verify-email-done')
            else:
                return redirect('register')
        return render(request, 'shop/verify_email_message.html')
        user.save()

        send_mail('Register','Successfully registered','mirobitovmirafzalpython@gmail.com',[user.email],fail_silently=False)
        return redirect('products')
    else:
        form = RegisterModelForm()
    return render(request, 'shop/register.html',{'form':form})

def send_email(request):
    form = EmailForm()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            send_mail(form.cleaned_data['subject'],form.cleaned_data['message'],form.cleaned_data['email_from'],[form.cleaned_data['email_to']],fail_silently=False)

            return redirect('products')
    context = {'form': form}
    return render(request,'shop/send-mail.html',context)











