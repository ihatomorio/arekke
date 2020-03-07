from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils import timezone
from .models import Book, Product
from .forms import BookForm, ProductForm
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
        webscraper.get_single_item(obj)

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

