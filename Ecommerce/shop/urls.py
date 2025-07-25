"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
app_name='shop'
urlpatterns = [
    path('',views.CategoryView.as_view(),name='categories'),
    path('products/<int:i>',views.ProductView.as_view(),name='products'),
    path('pro/<int:i>', views.DetailView.as_view(), name='pro'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('otp', views.OtpView.as_view(), name='otp'),
    path('signin', views.LoginView.as_view(), name='signin'),
    path('signout', views.LogoutView.as_view(), name='signout'),
    path('addcategory',views.AddCategoryView.as_view(),name='addcategory'),
    path('addproduct', views.AddProductView.as_view(), name='addproduct'),
    path('search', views.SearchView.as_view(), name='search'),

]
