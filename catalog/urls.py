from django.urls import path
from .views import (
    home, contact, ProductListView, ProductDetailView, 
    ProductCreateView, ProductUpdateView, ProductDeleteView, 
    UnpublishProductView, CategoryProductsView
)

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/unpublish/', UnpublishProductView.as_view(), name='unpublish_product'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
    path('contacts/', contact, name='contact'),
]
