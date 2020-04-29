from concurrent import futures

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Product, Account
from .forms import ProductForm, AccountForm

from engine.webscraper import DoujinShop


# global variable
_executer = futures.ThreadPoolExecutor(max_workers=4)


@login_required
def product_list(request):
    products = Product.objects.filter(owner=request.user)

    # POSTの場合更新処理
    if request.method == "POST":
        # POSTリクエストからpkを取り出す
        pk_id = request.POST.get('pk', None)

        # 指定のpkからproductを取り出す
        product = get_object_or_404(Product, pk=pk_id)

        # 並列処理で商品情報を取得する
        # DoujinShop.UpdateProductInfo(product, False)
        _executer.submit(fn=DoujinShop.UpdateProductInfo, product=product, set_shop_num=False)

        # 同じページにリダイレクトしてPOSTの要求をクリアする
        return redirect('/')

    # render() shortcut eliminates HttpResponce and loader
    return render(request, 'book_app/product_list.html', {'products': products})


@login_required
def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            Product.objects.create(
                owner=request.user,
                shop = cd['shop'],
                url = cd['url'],
                title = cd['title'],
                author = cd['author'],
                circle = cd['circle'],
                image_path = cd['image_path'],
                added_date = timezone.now(),
            )

            return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'book_app/product_new.html', {'form': form})


@login_required
def product_new_from_url(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        # if form.is_valid(): #skipo check
        print(form)
        cd = form.cleaned_data

        added_product = Product.objects.create(
            owner=request.user,
            url = cd['url'],
            title = 'loading',
            added_date = timezone.now(),
        )

        _executer.submit(fn=DoujinShop.UpdateProductInfo, product=added_product, set_shop_num=True)

        return redirect('/product/new-from-url/')
    else:
        form = ProductForm()
    return render(request, 'book_app/product_new_from_url.html', {'form': form})


@login_required
def product_edit(request, pk):
    procuct_object = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            procuct_object.shop = cd['shop']
            procuct_object.url = cd['url']
            procuct_object.title = cd['title']
            procuct_object.author = cd['author']
            procuct_object.circle = cd['circle']
            procuct_object.image_path = cd['image_path']

            procuct_object.save()
            return redirect('/')
    else:
        procuct_object = get_object_or_404(Product, pk=pk)

        form = ProductForm({
            'shop': procuct_object.shop,
            'url': procuct_object.url,
            'title': procuct_object.title,
            'author': procuct_object.author,
            'circle': procuct_object.circle,
            'image_path': procuct_object.image_path,
            })

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
        # DoujinShop.GetProductList(account, request.user)
        _executer.submit(fn=DoujinShop.GetProductList, account=account, request_by=request.user)

        # 同じページにリダイレクトしてPOSTの要求をクリアする
        return redirect('/account/list/')

    return render(request, 'book_app/account_list.html', {'accounts': accounts})


@login_required
def account_new(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
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
        form = AccountForm()
    return render(request, 'book_app/account_new.html', {'form': form})

