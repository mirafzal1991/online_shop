from django.urls import path
from shop.views import product_list, add_product, product_detail, edit_product, delete_product,login_page,logout_page


urlpatterns = [
    path('', product_list,name='products'),
    path('product-add/',add_product,name='add_product'),
    path('product-detail/<int:product_id>',product_detail,name='product_detail'),
    path('product/<int:product_id>/update',edit_product,name='edit'),
    path('product/<int:product_id>/delete', delete_product, name='delete'),
    path('login-page/', login_page, name='login'),
    path('logout-page/',logout_page,name='logout')

]