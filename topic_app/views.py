"""
topic_app/views.py  (FINAL VERSION)
"""

import logging
import json
from django.shortcuts       import render, redirect, get_object_or_404
from django.contrib         import messages
from django.views.decorators.http import require_POST

from .forms      import TopicAnalysisForm
from .models     import Analysis
from .nlp_engine import run_topic_modeling

logger = logging.getLogger(__name__)


def home(request):
    form = TopicAnalysisForm()
    return render(request, 'topic_app/home.html', {'form': form})


def analyze(request):
    if request.method != 'POST':
        return redirect('home')

    form = TopicAnalysisForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(request, 'topic_app/home.html', {'form': form})

    cd               = form.cleaned_data
    input_type       = cd['input_type']
    num_topics       = cd['num_topics']
    num_words        = cd['num_words']
    manual_text      = cd.get('manual_text', '')
    csv_text_column  = cd.get('csv_text_column', 'text') or 'text'
    scrape_url       = cd.get('scrape_url', '')

    txt_file  = request.FILES.get('txt_file')
    csv_file  = request.FILES.get('csv_file')

    try:
        results = run_topic_modeling(
            input_type      = input_type,
            num_topics      = num_topics,
            num_words       = num_words,
            manual_text     = manual_text,
            txt_file        = txt_file,
            csv_file        = csv_file,
            csv_text_column = csv_text_column,
            scrape_url      = scrape_url,
        )
    except ValueError as e:
        messages.error(request, str(e))
        return render(request, 'topic_app/home.html', {'form': form})
    except Exception as e:
        logger.exception("Unexpected error during topic modeling")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return render(request, 'topic_app/home.html', {'form': form})

    analysis = Analysis(
        input_type = input_type,
        raw_text   = results.get('raw_text', '')[:5000],
        source_url = scrape_url if input_type == 'url' else None,
        num_topics = num_topics,
        num_words  = num_words,
    )
    analysis.results = results

    if input_type == 'txt' and txt_file:
        txt_file.seek(0)
        analysis.uploaded_file = txt_file
    elif input_type == 'csv' and csv_file:
        csv_file.seek(0)
        analysis.uploaded_file = csv_file

    analysis.save()

    messages.success(
        request,
        f"Analysis complete! Discovered {results['actual_topics']} topics "
        f"from {results['num_docs']} document(s)."
    )
    return redirect('results', pk=analysis.pk)


def results(request, pk):
    analysis     = get_object_or_404(Analysis, pk=pk)
    results_data = analysis.results
    topics       = results_data.get('topics', [])

    chart_data_per_topic = [
        {'label': t['label'], 'words': t['words'][:8], 'weights': t['weights'][:8]}
        for t in topics
    ]

    if results_data.get('dominant_topics'):
        from collections import Counter
        topic_counts = Counter(results_data['dominant_topics'])
        pie_labels   = [f"Topic {t+1}" for t in sorted(topic_counts.keys())]
        pie_values   = [topic_counts[t] for t in sorted(topic_counts.keys())]
    else:
        pie_labels, pie_values = [], []

    context = {
        'analysis':        analysis,
        'results':         results_data,
        'topics':          topics,
        'chart_data_json': json.dumps(chart_data_per_topic),
        'pie_labels_json': json.dumps(pie_labels),
        'pie_values_json': json.dumps(pie_values),
        'perplexity':      results_data.get('perplexity'),
        'num_docs':        results_data.get('num_docs', 0),
        'vocabulary_size': results_data.get('vocabulary_size', 0),
    }
    return render(request, 'topic_app/results.html', context)


def history(request):
    analyses = Analysis.objects.all()[:50]
    return render(request, 'topic_app/history.html', {'analyses': analyses})


@require_POST
def delete_analysis(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    analysis.delete()
    messages.success(request, "Analysis deleted.")
    return redirect('history')


def about(request):
    pipeline_steps = [
        ('01', 'Text Extraction',   'Extract raw text from paste / .txt / .csv / URL scrape'),
        ('02', 'Preprocessing',     'Lowercase, strip punctuation, remove stopwords, lemmatise'),
        ('03', 'Vectorisation',     'Build Document-Term Matrix using CountVectorizer (Bag-of-Words)'),
        ('04', 'LDA Training',      'Fit LatentDirichletAllocation via online variational Bayes'),
        ('05', 'Result Extraction', 'Extract top K words + weights per topic and doc-topic matrix'),
    ]

    tech_stack = [
        ('Django',         '4.x',    'Web framework — views, models, templates, ORM'),
        ('scikit-learn',   '1.x',    'LDA model + CountVectorizer'),
        ('NLTK',           '3.x',    'Tokenisation, stopwords, WordNetLemmatizer'),
        ('BeautifulSoup4', '4.x',    'HTML parsing for URL scraping'),
        ('requests',       '2.x',    'HTTP client for URL fetching'),
        ('numpy',          '1.x',    'Array operations for topic/doc matrices'),
        ('Chart.js',       '4.x',    'Interactive bar + doughnut charts (CDN)'),
        ('SQLite',         'built-in','Default Django database'),
    ]

    return render(request, 'topic_app/about.html', {
        'pipeline_steps': pipeline_steps,
        'tech_stack':     tech_stack,
    })
