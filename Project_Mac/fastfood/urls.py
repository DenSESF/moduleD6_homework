from django.urls import path
# from .views import Products, ProductsList, ProductDetail, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView
from .views import ProductsList, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView

# from .views import Products
# from .views import ProductsList, ProductDetail


app_name = 'fastfood'
urlpatterns = [
    # path('', ProductsList.as_view()),
    path('', ProductsList.as_view(), name='products'),
    # path('<int:pk>', ProductDetail.as_view()),
    # path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
    
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    
    # path('products/', Products.as_view()),
]
