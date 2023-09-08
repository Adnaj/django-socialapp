
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def test(request):
    return HttpResponse("test")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test),
    path('',include("base.urls")),
    path('api/',include("base.api.urls")),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)