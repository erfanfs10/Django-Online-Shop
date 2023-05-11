from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('eco/admin/', admin.site.urls),
    path('eco/', include('product.urls')),
    path('eco/__debug__/', include('debug_toolbar.urls')),
    path('eco/account/', include("account.urls")),
    path('eco/basket/', include("basket.urls")),
    path('eco/shipping/', include("shipping.urls")),
    path('eco/order/', include("order.urls"))

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
