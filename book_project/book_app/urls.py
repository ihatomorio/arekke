from django.urls import path
from . import views

urlpatterns = [
    # product pages
    path('', views.product_list, name='product_list'), #R
    path('product/list/', views.product_list, name='product_list'), # delete future
    path('product/new/', views.product_new, name='product_new'),
    path('product/new-from-url/', views.product_new_from_url, name='product_new_from_url'),
    path('product/edit/<int:pk>', views.product_edit, name='product_edit'),

    # account pages
    path('account/list/', views.account_list, name='account_list'),
    path('account/new/', views.account_new, name='account_new'),
    path('account/edit/<int:pk>', views.account_edit, name='account_edit'),
]