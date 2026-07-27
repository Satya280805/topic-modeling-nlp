"""
topic_app/urls.py

URL patterns for our topic_app.
Each path() maps a URL to a view function.

These are included from the project-level urls.py via:
    path('', include('topic_app.urls'))
"""

from django.urls import path
from . import views

# NOTE: app_name / namespace is intentionally removed.
# With a namespace, all {% url %} tags and redirect() calls would need
# the prefix, e.g. {% url 'topic_app:home' %}. Without it, plain names
# like {% url 'home' %} and redirect('home') work correctly everywhere.

urlpatterns = [

    # ── Home page (GET) ───────────────────────────────────────────────────────
    # URL: /
    # View: views.home
    # Name: 'home'  → used in redirect('home') and {% url 'home' %}
    path('', views.home, name='home'),

    # ── Analyze (POST) ────────────────────────────────────────────────────────
    # URL: /analyze/
    # Receives form submission from home page
    path('analyze/', views.analyze, name='analyze'),

    # ── Results page (GET) ────────────────────────────────────────────────────
    # URL: /results/5/  (where 5 is the Analysis primary key)
    # <int:pk> captures the integer pk from the URL
    path('results/<int:pk>/', views.results, name='results'),

    # ── Analysis history (GET) ────────────────────────────────────────────────
    # URL: /history/
    path('history/', views.history, name='history'),

    # ── Delete analysis (POST only) ───────────────────────────────────────────
    # URL: /delete/5/
    path('delete/<int:pk>/', views.delete_analysis, name='delete_analysis'),

    # ── About page (GET) ──────────────────────────────────────────────────────
    # URL: /about/
    path('about/', views.about, name='about'),
]
