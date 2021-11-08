from django.urls import path
from . import views
app_name = 'ecommerce'
urlpatterns = [
    path('home/', views.show_my_page, name='home'),
    path('edit/<int:id>', views.product_edit_view, name='product-edit'),
    path('new/', views.product_create, name='product-create'),
    path('detail/<int:id>', views.product_detail_view, name='product-detail')
]