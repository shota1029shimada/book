from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('book/',include('book.urls')),#bookアプリのurl.pyに移動
]

urlpatterns+= static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)#画像を呼び出すURL