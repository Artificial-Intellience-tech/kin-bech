from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from posts.views import home  # <-- adjust if your view has a different name

urlpatterns = [
    path("", home, name="home"),  # root URL opens dashboard/home

    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("posts/", include("posts.urls")),
    path("messaging/", include("messaging.urls")),
    path("search/", include("search.urls")),

    # Marketplace
    path("market/", include("market.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)