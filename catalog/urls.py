from catalog.apps import CatalogConfig
from django.urls import path
from catalog.views import home, contact, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", home, name="home"),
    path("contacts/", contact, name="contact"),
    path("product/<int:pk>/", product_detail, name="product_detail"),
]
