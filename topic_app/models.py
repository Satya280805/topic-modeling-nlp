"""
topic_app/models.py

Models define the DATABASE TABLES for our application.
Each class = one table. Each attribute = one column.

We store every analysis run so users can revisit past results.
"""

from django.db import models
import json


# ─────────────────────────────────────────────────────────────────────────────
# ANALYSIS MODEL
# ─────────────────────────────────────────────────────────────────────────────

class Analysis(models.Model):
    """
    Stores a single topic-modeling run.

    Fields
    ------
    input_type     : How the user provided text (manual / txt / csv / url)
    raw_text       : The full original text that was analyzed
    source_url     : If input_type == 'url', the URL that was scraped
    uploaded_file  : If input_type == 'txt' or 'csv', the uploaded file
    num_topics     : How many topics the user requested (e.g. 5)
    num_words      : How many top-words per topic (e.g. 10)
    results_json   : The LDA results stored as a JSON string
    created_at     : Timestamp when this analysis was run
    """

    # ── Input type choices ────────────────────────────────────────────────────
    INPUT_TYPE_CHOICES = [
        ('manual', 'Manual Text'),
        ('txt',    'TXT File Upload'),
        ('csv',    'CSV File Upload'),
        ('url',    'URL Scrape'),
    ]

    input_type    = models.CharField(
        max_length=10,
        choices=INPUT_TYPE_CHOICES,
        default='manual'
    )

    # Stores the raw text (either entered directly or extracted from file/URL)
    raw_text      = models.TextField(blank=True, default='')

    # Only populated when input_type == 'url'
    source_url    = models.URLField(blank=True, null=True, max_length=500)

    # Only populated for file uploads — saves the file to media/uploads/
    uploaded_file = models.FileField(
        upload_to='uploads/',
        blank=True,
        null=True
    )

    # LDA hyperparameters chosen by the user
    num_topics    = models.IntegerField(default=5)
    num_words     = models.IntegerField(default=10)

    # The full LDA output, serialised as JSON text
    # We manually serialize/deserialize via properties below
    results_json  = models.TextField(blank=True, default='{}')

    # Auto-set to now() when a record is first created
    created_at    = models.DateTimeField(auto_now_add=True)

    # ── Helper properties ─────────────────────────────────────────────────────

    @property
    def results(self):
        """Deserialize results_json → Python dict for use in templates/views."""
        try:
            return json.loads(self.results_json)
        except (json.JSONDecodeError, TypeError):
            return {}

    @results.setter
    def results(self, data):
        """Serialize a Python dict → JSON string before saving to DB."""
        self.results_json = json.dumps(data)

    def __str__(self):
        """String representation shown in Django admin and shell."""
        return f"Analysis #{self.pk} | {self.input_type} | {self.num_topics} topics | {self.created_at:%Y-%m-%d %H:%M}"

    class Meta:
        # Most recent analyses shown first in querysets
        ordering = ['-created_at']
        verbose_name        = 'Analysis'
        verbose_name_plural = 'Analyses'
