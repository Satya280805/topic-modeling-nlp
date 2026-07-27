"""
topic_app/admin.py

Register models with Django's admin panel so they can be
viewed, searched, filtered, and managed at /admin/.
"""

from django.contrib import admin
from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Analysis model.
    """

    # Columns shown in the list view (/admin/topic_app/analysis/)
    list_display = [
        'id',
        'input_type',
        'num_topics',
        'num_docs_display',
        'perplexity_display',
        'created_at',
    ]

    # Clickable column (click to open detail page)
    list_display_links = ['id', 'input_type']

    # Right-side filter panel
    list_filter = ['input_type', 'num_topics', 'created_at']

    # Search bar — searches these fields
    search_fields = ['raw_text', 'source_url']

    # Most recent first
    ordering = ['-created_at']

    # Make these fields read-only in detail view (auto-generated)
    readonly_fields = ['created_at', 'results_json']

    # ── Custom display methods ────────────────────────────────────────────────

    @admin.display(description='Documents')
    def num_docs_display(self, obj):
        """Show how many documents were in the corpus."""
        results = obj.results
        return results.get('num_docs', '—')

    @admin.display(description='Perplexity')
    def perplexity_display(self, obj):
        """Show model perplexity score."""
        results = obj.results
        p = results.get('perplexity')
        return f"{p:.2f}" if p else '—'
