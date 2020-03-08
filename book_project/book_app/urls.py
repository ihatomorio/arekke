from django.urls import path
import book_app.views

urlpatterns = [
    path('book/list/', book_app.views.book_list, name='book_list'),
    path('book/new/', book_app.views.book_new, name='book_new'),
    path('product/list/', book_app.views.product_list, name='product_list'),
    path('product/new/', book_app.views.product_new, name='product_new'),
    path('account/list/', book_app.views.account_list, name='account_list'),
    path('account/new/', book_app.views.account_new, name='account_new'),
]