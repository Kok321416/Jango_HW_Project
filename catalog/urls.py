from catalog.apps import CatalogConfig
from django.urls import path
from catalog.views import HomeView, ContactView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
