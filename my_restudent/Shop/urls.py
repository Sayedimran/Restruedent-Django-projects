from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Shop import views 
from .forms import LoginForm
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.ProductView.as_view(), name="home" ),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path ('Electronics/',views.Electronicss, name='Electronic'),
    path ('Electronics/<slug:data>',views.Electronicss, name='Electronicitem'),
    path('login/',auth_views.LoginView.as_view(template_name='Shop/login.html', authentication_form=LoginForm) , name='login'),
    path('registrations/',views.customerRegistrationview.as_view(),name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)