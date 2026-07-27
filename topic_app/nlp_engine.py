"""
topic_app/nlp_engine.py

This is the BRAIN of the project — all NLP and LDA logic lives here.

Pipeline:
  raw text / file / URL
       ↓
  text_extractor()   → extracts plain text from any source
       ↓
  preprocess_text()  → cleans & tokenises text
       ↓
  run_lda()          → trains LDA model, extracts topics
       ↓
  returns structured dict of topics + metadata
"""

import re
import csv
import io
import logging

import nltk
import requests
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────
# Get a named logger — messages will appear in the Django dev console.
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# NLTK DATA DOWNLOAD (runs once automatically)
# ─────────────────────────────────────────────────────────────────────────────
# NLTK needs these data files to tokenise and remove stopwords.
# quiet=True suppresses "already downloaded" messages.
def _ensure_nltk_data():
    """Download required NLTK corpora if not already present."""
    packages = ['stopwords', 'punkt', 'punkt_tab', 'wordnet']
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception as e:
            logger.warning(f"Could not download NLTK package '{pkg}': {e}")

_ensure_nltk_data()

from nltk.corpus   import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem     import WordNetLemmatizer


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

# English stopwords from NLTK + common web/HTML noise words
_STOP_WORDS = set(stopwords.words('english')).union({
    'also', 'would', 'could', 'should', 'may', 'might', 'said', 'say',
    'get', 'got', 'use', 'used', 'using', 'one', 'two', 'three', 'like',
    'make', 'made', 'go', 'going', 'gone', 'come', 'came', 'take', 'took',
    'http', 'https', 'www', 'com', 'org', 'net', 'html', 'php', 'utm',
})

# Lemmatizer reduces words to their base form: "running" → "run"
_LEMMATIZER = WordNetLemmatizer()


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — TEXT EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_text_from_manual(text: str) -> list[str]:
    """
    Manual input: split text into sentence-level mini-documents.

    Why not treat it as ONE document?
    LDA needs MULTIPLE documents to find cross-document patterns.
    With only 1 document, min_df=2 wipes the entire vocabulary.

    Strategy:
      1. Split on double newlines -> paragraphs (preferred)
      2. If too few paragraphs, split on sentence boundaries
      3. Group every 3 sentences into one mini-document
    """
    text = text.strip()

    # Try splitting on double newlines first (paragraph mode)
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if len(p.strip().split()) >= 8]
    if len(paragraphs) >= 4:
        return paragraphs

    # Fall back: split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) >= 5]

    if not sentences:
        return [text]

    # Group every 3 sentences into one mini-document
    chunks = []
    for i in range(0, len(sentences), 3):
        chunk = ' '.join(sentences[i:i+3])
        if chunk.strip():
            chunks.append(chunk)

    return chunks if chunks else [text]


def extract_text_from_txt(file_obj) -> list[str]:
    """
    TXT upload: read the file, treat entire content as one document.

    file_obj is a Django InMemoryUploadedFile or similar.
    We decode bytes → string using UTF-8 (fallback to latin-1).
    """
    raw_bytes = file_obj.read()
    try:
        text = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        text = raw_bytes.decode('latin-1')

    # Split on double newlines to get paragraph-level documents
    # This gives LDA more granular documents to work with
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if len(p.strip()) > 30]

    # If splitting produced very few paragraphs, use the whole text as one doc
    return paragraphs if len(paragraphs) >= 3 else [text.strip()]


def extract_text_from_csv(file_obj, text_column: str = 'text') -> list[str]:
    """
    CSV upload: each ROW is treated as a separate document.

    text_column: the column header name whose values contain the text.
    If the column is not found, we fall back to the FIRST column.

    Returns a list of strings (one per row).
    """
    raw_bytes = file_obj.read()
    try:
        content = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        content = raw_bytes.decode('latin-1')

    reader = csv.DictReader(io.StringIO(content))
    documents = []

    for row in reader:
        # Try the user-specified column first
        if text_column in row:
            cell = row[text_column].strip()
        else:
            # Fall back to first column value
            cell = list(row.values())[0].strip() if row else ''

        if cell and len(cell.split()) >= 5:   # Skip very short rows
            documents.append(cell)

    if not documents:
        raise ValueError(
            f"No usable text found in CSV. "
            f"Make sure the column '{text_column}' exists and contains text."
        )

    return documents


def extract_text_from_url(url: str) -> list[str]:
    """
    URL scraping: download the page, extract visible text using BeautifulSoup.

    Steps:
      1. requests.get() downloads the HTML
      2. BeautifulSoup parses the HTML tree
      3. We remove script/style tags (non-visible)
      4. We extract paragraphs (<p> tags) as separate documents
      5. Fallback: use all visible text if <p> tags are sparse

    Returns a list of paragraph strings.
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()   # Raise exception for HTTP 4xx/5xx
    except requests.exceptions.Timeout:
        raise ValueError("The URL timed out. Please try a different URL.")
    except requests.exceptions.ConnectionError:
        raise ValueError("Could not connect to the URL. Check if it's accessible.")
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"HTTP error {e.response.status_code} when fetching URL.")

    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove non-content tags
    for tag in soup(['script', 'style', 'nav', 'header', 'footer',
                     'aside', 'form', 'button', 'iframe', 'noscript']):
        tag.decompose()

    # Extract <p> tag text as individual documents
    paragraphs = [
        p.get_text(separator=' ', strip=True)
        for p in soup.find_all('p')
        if len(p.get_text(strip=True).split()) >= 10   # At least 10 words
    ]

    # If we got enough paragraphs, use them
    if len(paragraphs) >= 5:
        return paragraphs

    # Fallback: split all visible text on double newlines
    all_text = soup.get_text(separator='\n', strip=True)
    chunks = [c.strip() for c in all_text.split('\n\n') if len(c.strip().split()) >= 10]

    if not chunks:
        raise ValueError("Could not extract enough text from the URL. Try a different page.")

    return chunks


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — TEXT PREPROCESSING
# ─────────────────────────────────────────────────────────────────────────────

def preprocess_document(text: str) -> str:
    """
    Clean and normalise a single document string.

    Operations (in order):
      1. Lowercase everything
      2. Remove URLs
      3. Remove email addresses
      4. Remove HTML entities (&amp; &nbsp; etc.)
      5. Remove punctuation and numbers
      6. Tokenise into individual words
      7. Remove stopwords and very short words (< 3 chars)
      8. Lemmatise each word (running → run, better → good)

    Returns a single cleaned string of space-separated tokens.
    """

    # 1. Lowercase
    text = text.lower()

    # 2. Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)

    # 3. Remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # 4. Remove HTML entities
    text = re.sub(r'&[a-z]+;', ' ', text)

    # 5. Remove everything that's not a letter or space
    text = re.sub(r'[^a-z\s]', ' ', text)

    # 6. Tokenise: split string into list of words
    tokens = word_tokenize(text)

    # 7 & 8. Filter stopwords + lemmatise
    cleaned_tokens = [
        _LEMMATIZER.lemmatize(token)
        for token in tokens
        if token not in _STOP_WORDS and len(token) >= 3
    ]

    return ' '.join(cleaned_tokens)


def preprocess_corpus(documents: list[str]) -> list[str]:
    """
    Apply preprocess_document() to every document in the list.

    Also filters out any empty strings produced by preprocessing.
    """
    cleaned = [preprocess_document(doc) for doc in documents]
    # Remove documents that became empty after cleaning
    cleaned = [doc for doc in cleaned if doc.strip()]
    return cleaned


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — VECTORISATION (Bag of Words)
# ─────────────────────────────────────────────────────────────────────────────

def build_dtm(cleaned_docs: list[str], max_features: int = 1000):
    """
    Convert cleaned text documents into a Document-Term Matrix (DTM).

    CountVectorizer:
      - Converts each document into a vector of word counts
      - max_features: only keep the top N most frequent words (vocabulary)
      - min_df=2: ignore words that appear in fewer than 2 documents
      - max_df=0.90: ignore words that appear in more than 90% of documents
                     (these are too common to be informative)

    Returns:
      dtm        : sparse matrix of shape (n_docs, n_features)
      vectorizer : fitted CountVectorizer (needed to get feature names)
    """
    # Dynamically compute min_df and max_df based on corpus size
    # to prevent "vocabulary too small" errors on small inputs.
    n = len(cleaned_docs)
    if n <= 2:
        min_df = 1
        max_df = 1.0      # No upper limit for tiny corpus
    elif n <= 5:
        min_df = 1
        max_df = 0.99
    elif n <= 10:
        min_df = 1
        max_df = 0.95
    else:
        min_df = 2
        max_df = 0.90

    vectorizer = CountVectorizer(
        max_features=max_features,
        min_df=min_df,
        max_df=max_df,
        ngram_range=(1, 1),    # Unigrams only (single words)
        strip_accents='unicode',
    )

    dtm = vectorizer.fit_transform(cleaned_docs)
    return dtm, vectorizer


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — LDA MODEL
# ─────────────────────────────────────────────────────────────────────────────

def run_lda(dtm, vectorizer, num_topics: int = 5, num_words: int = 10) -> dict:
    """
    Train a Latent Dirichlet Allocation (LDA) model.

    LDA assumes:
      - Each DOCUMENT is a mixture of topics
      - Each TOPIC is a mixture of words

    Parameters:
      dtm          : Document-Term Matrix from CountVectorizer
      vectorizer   : Fitted CountVectorizer (to map indices → words)
      num_topics   : K — how many latent topics to discover
      num_words    : How many top keywords to extract per topic

    Returns a dict:
      {
        'topics': [
          {'id': 1, 'label': 'Topic 1', 'words': ['word1', 'word2', ...],
           'weights': [0.05, 0.04, ...], 'word_weight_pairs': [...]},
          ...
        ],
        'doc_topic_matrix': [[...], ...],   # n_docs × n_topics
        'perplexity': float,
        'num_topics': int,
        'num_docs': int,
        'vocabulary_size': int,
      }
    """

    # ── Train LDA ─────────────────────────────────────────────────────────────
    lda_model = LatentDirichletAllocation(
        n_components=num_topics,       # K — number of topics
        max_iter=20,                   # EM iterations (more = better but slower)
        learning_method='online',      # Online variational Bayes (faster)
        learning_offset=50.0,          # Downweights early iterations
        random_state=42,               # Reproducibility seed
        doc_topic_prior=None,          # Alpha: auto (symmetric Dirichlet)
        topic_word_prior=None,         # Beta:  auto (symmetric Dirichlet)
        n_jobs=-1,                     # Use all CPU cores
    )

    # fit_transform() trains the model AND returns doc-topic distributions
    # Shape: (n_documents, n_topics) — each value = probability
    doc_topic_matrix = lda_model.fit_transform(dtm)

    # ── Extract top words per topic ────────────────────────────────────────────
    # lda_model.components_ shape: (n_topics, n_vocabulary)
    # Each row = one topic, values = unnormalised word weights
    feature_names = vectorizer.get_feature_names_out()   # Vocabulary array

    topics = []
    for topic_idx, topic_vector in enumerate(lda_model.components_):
        # argsort() returns indices from lowest to highest
        # [-num_words:]  → last N indices = highest-weight words
        # [::-1]         → reverse so highest weight is first
        top_indices = topic_vector.argsort()[-num_words:][::-1]

        # Map indices → actual word strings
        top_words = [feature_names[i] for i in top_indices]

        # Normalised weights (sum to 1 across all vocabulary for this topic)
        total = topic_vector.sum()
        top_weights = [
            round(float(topic_vector[i] / total), 4)
            for i in top_indices
        ]

        # zip words with weights for easy template iteration
        word_weight_pairs = list(zip(top_words, top_weights))

        topics.append({
            'id':               topic_idx + 1,
            'label':            f'Topic {topic_idx + 1}',
            'words':            top_words,
            'weights':          top_weights,
            'word_weight_pairs': word_weight_pairs,
        })

    # ── Document-topic assignments ─────────────────────────────────────────────
    # For each document, find the dominant topic
    dominant_topics = np.argmax(doc_topic_matrix, axis=1).tolist()

    # Serialise doc-topic matrix as list of lists (JSON-friendly)
    doc_topic_list = [
        [round(float(v), 4) for v in row]
        for row in doc_topic_matrix
    ]

    # ── Perplexity ────────────────────────────────────────────────────────────
    # Lower perplexity = model fits the data better
    try:
        perplexity = round(lda_model.perplexity(dtm), 2)
    except Exception:
        perplexity = None

    return {
        'topics':           topics,
        'doc_topic_matrix': doc_topic_list,
        'dominant_topics':  dominant_topics,
        'perplexity':       perplexity,
        'num_topics':       num_topics,
        'num_docs':         dtm.shape[0],
        'vocabulary_size':  dtm.shape[1],
    }


# ─────────────────────────────────────────────────────────────────────────────
# MASTER PIPELINE FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def run_topic_modeling(
    input_type: str,
    num_topics: int = 5,
    num_words: int = 10,
    manual_text: str = '',
    txt_file=None,
    csv_file=None,
    csv_text_column: str = 'text',
    scrape_url: str = '',
) -> dict:
    """
    Master function called by the Django view.

    Orchestrates extraction → preprocessing → vectorisation → LDA.

    Returns the same dict structure as run_lda() plus extracted 'raw_text'.

    Raises ValueError with a user-friendly message if anything goes wrong.
    """

    # ── STEP 1: Extract raw documents ─────────────────────────────────────────
    logger.info(f"Starting topic modeling | input_type={input_type} | topics={num_topics}")

    if input_type == 'manual':
        documents = extract_text_from_manual(manual_text)
        raw_text  = manual_text

    elif input_type == 'txt':
        documents = extract_text_from_txt(txt_file)
        raw_text  = f"[TXT file — {len(documents)} paragraph(s) extracted]"

    elif input_type == 'csv':
        documents = extract_text_from_csv(csv_file, csv_text_column)
        raw_text  = f"[CSV file — {len(documents)} row(s) extracted]"

    elif input_type == 'url':
        documents = extract_text_from_url(scrape_url)
        raw_text  = f"[URL: {scrape_url} — {len(documents)} paragraph(s) extracted]"

    else:
        raise ValueError(f"Unknown input_type: {input_type}")

    logger.info(f"Extracted {len(documents)} document(s)")

    # ── STEP 2: Preprocess ────────────────────────────────────────────────────
    cleaned_docs = preprocess_corpus(documents)

    if len(cleaned_docs) == 0:
        raise ValueError("No usable text after preprocessing. Please provide more content.")

    # ── Safety check: can't have more topics than documents ───────────────────
    if num_topics > len(cleaned_docs):
        num_topics = max(2, len(cleaned_docs))
        logger.warning(f"Reduced num_topics to {num_topics} to match corpus size")

    # ── STEP 3: Vectorise ─────────────────────────────────────────────────────
    try:
        dtm, vectorizer = build_dtm(cleaned_docs)
    except ValueError as e:
        raise ValueError(
            f"Vocabulary is too small to model topics. "
            f"Please provide longer or more varied text. (Detail: {e})"
        )

    if dtm.shape[1] == 0:
        raise ValueError("No valid words found after preprocessing. Please provide richer text.")

    # ── STEP 4: LDA ───────────────────────────────────────────────────────────
    results = run_lda(dtm, vectorizer, num_topics=num_topics, num_words=num_words)
    results['raw_text']      = raw_text
    results['input_type']    = input_type
    results['actual_topics'] = num_topics

    logger.info(f"LDA complete | perplexity={results.get('perplexity')}")

    return results
