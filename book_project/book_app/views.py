from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils import timezone
from django.db import models
import book_app.models
import book_app.forms

def book_list(request):
    books = book_app.models.Book.objects.all()
    return render(request, 'book_app/book_list.html', {'books': books})


def book_new(request):
    if request.method == "POST":
        form = book_app.forms.BookForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()

            return redirect('/book/list/', pk=post.pk)
    else:
        form = book_app.forms.BookForm()
    return render(request, 'book_app/book_new.html', {'form': form})


def product_list(request):
    products = book_app.models.Product.objects.all()
    return render(request, 'book_app/product_list.html', {'products': products})


def product_new(request):
    if request.method == "POST":
        form = book_app.forms.ProductForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.added_date = timezone.now()
            # post.image_path = request.FILES['file']
            post.save()

            return redirect('/product/list/', pk=post.pk)
    else:
        form = book_app.forms.ProductForm()
    return render(request, 'book_app/product_new.html', {'form': form})

