"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from demo import views
from demo.views import detail
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from myproject import settings

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('admin/', admin.site.urls),
    path('', views.about, name='about'),
    path('about/', views.about, name='about'),
    path('competitions/', views.competitions, name='competitions'),
    path('rate/', views.rate, name='rate'),
    path('catalog/', views.catalog, name='catalog'),
    path('competitions', views.competitions, name='competitions'),

    #     тарифы
    path('pageVologda/', views.pageVologda, name='pageVologda'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('delete_order/<pk>', views.delete_order, name='delete_order'),
    path('confirm_order/<pk>', views.confirm_order, name='confirm_order'),
    # path('detail/<id:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('product<int:id>/', detail, name='productdetail'),
    path('to_cart/<int:pk>', views.to_cart, name='to_cart'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('application/', views.application, name='application'),

]
urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
