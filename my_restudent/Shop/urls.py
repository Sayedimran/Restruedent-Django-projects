from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Shop import views
urlpatterns = [
    path('', views.ProductView.as_view(), name="home" ),
     path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
     

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)