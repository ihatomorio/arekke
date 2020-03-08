from django import forms
from .models import Book, Product, Account

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'circle')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('info', 'shop', 'url', 'date', 'image_path')


class AccountForm(forms.Form):
    shop = forms.ChoiceField(
        label = 'サイト',
        widget=forms.Select,
        choices=Account.SHOPS,
        required=True,
    )

    user = forms.CharField(
        label='ユーザー名',
        max_length=200,
        required=True,
    )

    password = forms.CharField(
        label='パスワード',
        widget = forms.PasswordInput(),
        max_length=200,
        required=True,
    )