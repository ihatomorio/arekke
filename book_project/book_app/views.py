from concurrent import futures

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from book_app.models import Product, Account
from . import forms

from engine.webscraper import DoujinShop


@login_required
def product_list(request):
    products = Product.objects.filter(owner=request.user)
    if request.method == "POST":
        # POSTリクエストからpkを取り出す
        pk_id = request.POST.get('pk', None)

        # 指定のpkからproductを取り出す
        product = Product.objects.get(pk=pk_id)

        # 並列処理で商品情報を取得する
        # DoujinShop.QueueUpdateProductInfo(product, False)
        DoujinShop.UpdateProductInfo(product, False)
        # futures.ThreadPoolExecutor(max_workers=4).submit(fn=DoujinShop.UpdateProductInfo, product=product, set_shop_num=True)

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
        account = Account.objects.get(pk=pk_id)

        # Webスクレイピングを実行
        try:
            # DoujinShop.QueueGetProductList(account, request.user)
            DoujinShop.GetProductList(account, request.user)
            # futures.ThreadPoolExecutor(max_workers=4).submit(fn=DoujinShop.GetProductList, account=account, request_by=request.user)
        except:
            pass

        # 同じページにリダイレクトしてPOSTの要求をクリアする
        return redirect('/account/list/')
    
    return render(request, 'book_app/account_list.html', {'accounts': accounts})


@login_required
def account_new(request):
    if request.method == "POST":
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            # アカウントを作って保存
            Account.objects.create(
                owner = request.user,
                shop = form.cleaned_data['shop'],
                user = form.cleaned_data['user'],
                password = form.cleaned_data['password'],
            )

            return redirect('/account/list/')
    else:
        form = forms.AccountForm()
    return render(request, 'book_app/account_new.html', {'form': form})

