"""
topic_app/forms.py

Django Forms handle:
  1. Rendering HTML <input> fields
  2. Validating submitted data (type-checking, required fields, etc.)
  3. Returning clean Python values to the view

We have ONE form with conditional fields for all four input modes.
"""

from django import forms


# ─────────────────────────────────────────────────────────────────────────────
# TOPIC ANALYSIS FORM
# ─────────────────────────────────────────────────────────────────────────────

class TopicAnalysisForm(forms.Form):
    """
    Single unified form that covers all four input types:
      - manual  → textarea
      - txt     → file upload (.txt)
      - csv     → file upload (.csv)
      - url     → text input (http/https)

    Plus LDA hyperparameters: num_topics and num_words_per_topic.
    """

    # ── Input-type selector ───────────────────────────────────────────────────
    INPUT_CHOICES = [
        ('manual', '✍️  Paste Text'),
        ('txt',    '📄  Upload TXT'),
        ('csv',    '📊  Upload CSV'),
        ('url',    '🌐  Scrape URL'),
    ]

    input_type = forms.ChoiceField(
        choices=INPUT_CHOICES,
        initial='manual',
        widget=forms.RadioSelect(attrs={'class': 'input-type-radio'}),
        label='Input Method'
    )

    # ── Manual text input ─────────────────────────────────────────────────────
    # required=False because it's only needed when input_type == 'manual'
    manual_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 10,
            'placeholder': 'Paste your text here… (minimum 50 words recommended)',
            'class': 'form-textarea',
            'id': 'id_manual_text',
        }),
        label='Your Text'
    )

    # ── TXT file upload ───────────────────────────────────────────────────────
    txt_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': '.txt',
            'class': 'form-file-input',
            'id': 'id_txt_file',
        }),
        label='Upload .txt File'
    )

    # ── CSV file upload ───────────────────────────────────────────────────────
    # For CSV, each row (or a specific column) is treated as a separate document
    csv_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': '.csv',
            'class': 'form-file-input',
            'id': 'id_csv_file',
        }),
        label='Upload .csv File'
    )

    # Column name in the CSV that contains the text (default = first column)
    csv_text_column = forms.CharField(
        required=False,
        initial='text',
        widget=forms.TextInput(attrs={
            'placeholder': 'Column name containing text (e.g. "text", "review")',
            'class': 'form-input',
            'id': 'id_csv_text_column',
        }),
        label='CSV Text Column'
    )

    # ── URL scraping ──────────────────────────────────────────────────────────
    scrape_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://example.com/article',
            'class': 'form-input',
            'id': 'id_scrape_url',
        }),
        label='Website URL'
    )

    # ── LDA Hyperparameters ───────────────────────────────────────────────────
    num_topics = forms.IntegerField(
        min_value=2,
        max_value=20,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'min': '2',
            'max': '20',
            'id': 'id_num_topics',
        }),
        label='Number of Topics'
    )

    num_words = forms.IntegerField(
        min_value=5,
        max_value=20,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'min': '5',
            'max': '20',
            'id': 'id_num_words',
        }),
        label='Words per Topic'
    )

    # ── Custom validation ─────────────────────────────────────────────────────

    def clean(self):
        """
        Cross-field validation: ensure the correct field is filled
        based on the chosen input_type.

        clean() is called AFTER all individual field validators pass.
        self.cleaned_data contains the validated values so far.
        We raise forms.ValidationError to report problems.
        """
        cleaned = super().clean()
        input_type = cleaned.get('input_type')

        if input_type == 'manual':
            text = cleaned.get('manual_text', '').strip()
            if not text:
                self.add_error('manual_text', 'Please paste some text to analyze.')
            elif len(text.split()) < 20:
                self.add_error('manual_text', 'Please provide at least 20 words for meaningful analysis.')

        elif input_type == 'txt':
            if not cleaned.get('txt_file'):
                self.add_error('txt_file', 'Please upload a .txt file.')

        elif input_type == 'csv':
            if not cleaned.get('csv_file'):
                self.add_error('csv_file', 'Please upload a .csv file.')

        elif input_type == 'url':
            if not cleaned.get('scrape_url'):
                self.add_error('scrape_url', 'Please enter a valid URL.')

        return cleaned
