from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils import timezone
from .models import Book, Product, Account
from .forms import BookForm, ProductForm, AccountForm
from engine import webscraper

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_app/book_list.html', {'books': books})


def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()

            return redirect('/book/list/', pk=post.pk)
    else:
        form = BookForm()
    return render(request, 'book_app/book_new.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    if request.method == "POST":
        # POSTリクエストからpkを取り出す
        pk_id = request.POST.get('pk',None)

        # 指定のpkからobjを取り出す
        obj = Product.objects.get(pk=pk_id)

        # Webスクレイピングを実行
        webscraper.get_product_info(obj)

        # objを取得してきた情報で確定
        obj.save()
        obj.info.save()

        # 同じページにリダイレクトしてPOSTの要求をクリアする
        return redirect('/product/list/')
    
    return render(request, 'book_app/product_list.html', {'products': products})


def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.added_date = timezone.now()
            # post.image_path = request.FILES['file']
            post.save()

            return redirect('/product/list/', pk=post.pk)
    else:
        form = ProductForm()
    return render(request, 'book_app/product_new.html', {'form': form})


def account_list(request):
    accounts = Account.objects.all()
    if request.method == "POST":
        # POSTリクエストからpkを取り出す
        pk_id = request.POST.get('pk',None)

        # 指定のpkからobjを取り出す
        obj = Account.objects.get(pk=pk_id)

        # Webスクレイピングを実行
        webscraper.get_product_list(obj, request)

        # objを取得してきた情報で確定
        obj.date = timezone.now()
        obj.save()

        # 同じページにリダイレクトしてPOSTの要求をクリアする
        return redirect('/account/list/')
    
    return render(request, 'book_app/account_list.html', {'accounts': accounts})


def account_new(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = Account()
            account.shop = form.cleaned_data['shop']
            account.user = form.cleaned_data['user']
            account.password = form.cleaned_data['password']

            Account.objects.create(
                owner = request.user,
                shop = account.shop,
                user = account.user,
                password = account.password,
            )

            return redirect('/account/list/')
    else:
        form = AccountForm()
    return render(request, 'book_app/account_new.html', {'form': form})


def CreateFromUrl(url, request):
    # URL被りがあったら-1で終了
    if Product.objects.filter(url=url):
        return -1

    info = Book.objects.create(
        owner = request.user,
    )
    product = Product.objects.create(
        owner = request.user,
        info = info,
        shop = 0,
        url = url
    )
    webscraper.get_product_info(product)
    info.save()
    product.save()