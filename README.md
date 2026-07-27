# Python-Based Topic Modeling using Django and NLP

A **Python-based Django web application** that leverages **Natural Language Processing (NLP)** and **Latent Dirichlet Allocation (LDA)** to extract meaningful topics from text documents and web content. The application preprocesses textual data, identifies hidden topics, and presents the results through a user-friendly web interface.

---

## 🚀 Features

- Upload text documents for topic analysis
- Extract textual content from website URLs
- Text preprocessing using NLP techniques
  - Tokenization
  - Stopword Removal
  - Lemmatization
- Topic extraction using **Latent Dirichlet Allocation (LDA)**
- Interactive Django web interface
- Display extracted topics with representative keywords

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Framework
- Django

### Machine Learning & NLP
- Scikit-learn
- NLTK
- Latent Dirichlet Allocation (LDA)
- CountVectorizer

### Data Processing
- NumPy

### Web Scraping
- Requests
- BeautifulSoup4
- lxml

### Utilities
- Pillow

---

## 📁 Project Structure

```
topic-modeling-nlp/
│
├── app/
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/<username>/topic-modeling-nlp.git
cd topic-modeling-nlp
```

### Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Download NLTK resources

```python
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
```

### Apply migrations

```bash
python manage.py migrate
```

### Run the application

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 🔍 How It Works

1. Upload a text document or enter a website URL.
2. The application extracts textual content.
3. Text is preprocessed using NLP techniques:
   - Tokenization
   - Stopword Removal
   - Lemmatization
4. A document-term matrix is generated using **CountVectorizer**.
5. **Latent Dirichlet Allocation (LDA)** identifies the underlying topics.
6. The discovered topics and keywords are displayed through the Django interface.

---

## 📦 Requirements

- Django 4.2+
- Python 3.10+
- Scikit-learn
- NLTK
- NumPy
- Requests
- BeautifulSoup4
- lxml
- Pillow

---

## 🎯 Applications

- Document Categorization
- News Article Analysis
- Research Paper Organization
- Content Classification
- Text Mining
- Educational NLP Projects

---

## 🚀 Future Enhancements

- Interactive topic visualization
- Support for PDF and DOCX files
- Topic coherence evaluation
- User authentication
- Export results to PDF and Excel
- Additional topic modeling algorithms (NMF, BERTopic)

---

## 👥 Team

This project was developed as a collaborative academic project by:

- Kalavalapalli Venkata Sesha Satyanarayana
- Katta Udaya Lakshmi
- Kandala Vineetha
- Kukkala Dileep Babu
- Pinishetty Srinivas

---

### My Contribution

As a core contributor to this project, I contributed to:

- Developing the topic modeling pipeline using Python and NLP
- Implementing Django application features
- Data preprocessing and text analysis
- Testing and debugging the application
- Documentation and project integration

## 📄 License

This project is intended for educational and academic purposes.
