from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Product, Account
from . import forms
from engine import webscraper

@login_required
def product_list(request):
    products = Product.objects.filter(owner=request.user)
    if request.method == "POST":
        # POSTリクエストからpkを取り出す
        pk_id = request.POST.get('pk',None)

        # 指定のpkからobjを取り出す
        obj = Product.objects.get(pk=pk_id)

        # Webスクレイピングを実行
        webscraper.get_product_info(obj)

        # objを取得してきた情報で確定
        obj.save()

        # 同じページにリダイレクトしてPOSTの要求をクリアする
        return redirect('/product/list/')
    
    return render(request, 'book_app/product_list.html', {'products': products})

@login_required
def product_new(request):
    if request.method == "POST":
        form = forms.ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # post = form.save(commit=False)
            cd = form.cleaned_data
            post = Product.objects.create(
                owner=request.user,
                shop = cd['shop'],
                url = cd['url'],
                title = cd['title'],
                author = cd['author'],
                added_date = timezone.now(),
            )
            # post.owner = request.user
            # post.added_date = timezone.now()
            # post.image_path = request.FILES['file']
            # post.save()

            return redirect('/product/list/', pk=post.pk)
    else:
        form = forms.ProductForm()
    return render(request, 'book_app/product_new.html', {'form': form})

@login_required
def account_list(request):
    accounts = Account.objects.filter(owner=request.user)
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

@login_required
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

    product = Product.objects.create(
        owner = request.user,
        shop = 0,
        url = url
    )
    webscraper.get_product_info(product)
    product.save()