from django import forms

from .models import Book, Product

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'circle')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('info', 'shop', 'url', 'date')