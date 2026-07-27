"""
topic_modeling_project/urls.py

This is the ROOT URL configuration for the entire Django project.
Every incoming request is matched against these URL patterns first.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ── Admin Panel ──────────────────────────────────────────────────────────
    # Django's built-in admin interface accessible at /admin/
    path('admin/', admin.site.urls),

    # ── Our App URLs ─────────────────────────────────────────────────────────
    # All URLs starting with '' (i.e., root) are delegated to topic_app/urls.py
    path('', include('topic_app.urls')),
]

# ── Serve Media Files in Development ─────────────────────────────────────────
# During development (DEBUG=True), Django itself serves uploaded files.
# In production you'd use Nginx or a CDN instead.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
