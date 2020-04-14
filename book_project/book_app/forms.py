from django import forms
from .models import Product, Account


class ProductForm(forms.Form):
    shop = forms.ChoiceField(
        label = 'サイト',
        widget=forms.Select,
        choices=Account.SHOPS,
        required=True,
    )

    url = forms.URLField(
        label='URL',
        max_length=512,
        required=False,
    )

    title = forms.CharField(
        label='書名',
        max_length=256,
        required=True,
    )

    author = forms.CharField(
        label='著者',
        max_length=256,
        required=False,
    )
    
    circle = forms.CharField(
        label='サークル名',
        max_length=256,
        required=False,
    )
    
    bought_date = forms.DateField(
        label='購入日',
        required=False,
    )

    image_path=forms.ImageField(
        label='ファイルを選択',
        required=False,
    )

    class Meta:
        model = Product
    #     fields = ('title', 'author', 'circle' 'shop', 'url', 'date', 'image_path')


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