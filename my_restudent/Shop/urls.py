from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Shop import views 
from .forms import LoginForm,MyPasswordChangeForm, MyPasswordResetForm ,MySetpassword
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.ProductView.as_view(), name="home" ),
    
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path ('Electronics/',views.Electronicss, name='Electronic'),
   
    path ('Electronics/<slug:data>',views.Electronicss, name='Electronicitem'),

    path('accounts/login/',auth_views.LoginView.as_view(template_name='Shop/login.html', authentication_form=LoginForm) , name='login'),
    
    path('registrations/',views.customerRegistrationview.as_view(),name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
   
    path('profile/', views.ProfileView.as_view(), name='profile'),
   
    path('address/', views.address, name='address'),
    path('add-to-cart/', views.add_to_cart, name='addTocart'),
    path('cart/', views.show_cart, name="showCart"),
    path("pluscart/",views.plus_cart , name="plusCart"),
    path("minuscart/", views.minus_cart, name="minuscart"),
    path("removeCart/", views.remove_cart, name="removeCart"),
    path("chakeout/", views.checkout, name="chakeout"),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='Shop/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name = 'Shop/passwordChangeDone.html'),name='MyPasswordChangeForm'),
    path('passwordReset/',auth_views.PasswordResetView.as_view(template_name = 'Shop/password_reset.html',form_class = MyPasswordResetForm ),name='passwordReset'),
    path('passWord-reset/Done/',auth_views.PasswordResetDoneView.as_view(template_name = 'Shop/password_reset_done.html'),name='password_reset_done'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Shop/password_reset_complete.html'), name='password_reset_complete'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Shop/password_reset_confirm.html', form_class=MySetpassword), name='password_reset_confirm'),
 
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)