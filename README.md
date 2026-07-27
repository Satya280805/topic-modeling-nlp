# Python-Based Topic Modeling using Django and NLP

A **Python-based Django web application** that leverages **Natural Language Processing (NLP)** and **Latent Dirichlet Allocation (LDA)** to extract meaningful topics from text documents and web content. The application preprocesses textual data, identifies hidden topics, and presents the extracted topics through an intuitive and user-friendly web interface.

---

## 🚀 Features

- Upload text documents for topic analysis
- Extract textual content from website URLs
- Text preprocessing using NLP techniques:
  - Tokenization
  - Stopword Removal
  - Lemmatization
- Topic extraction using **Latent Dirichlet Allocation (LDA)**
- Interactive Django web interface
- Display extracted topics with representative keywords
- URL-based text extraction using web scraping

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Framework
- Django

### Machine Learning & Natural Language Processing
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

```text
topic-modeling-nlp/
│
├── topic_app/
├── topic_modeling_project/
├── templates/
├── static/
├── media/
├── Sample_Data/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
└── db.sqlite3
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/topic-modeling-nlp.git
cd topic-modeling-nlp
```

### 2. Create a Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK Resources

```python
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 🔍 How It Works

1. Upload a text document or provide a website URL.
2. The application extracts textual content from the uploaded file or webpage.
3. The extracted text is preprocessed using:
   - Tokenization
   - Stopword Removal
   - Lemmatization
4. A document-term matrix is generated using **CountVectorizer**.
5. **Latent Dirichlet Allocation (LDA)** identifies the underlying topics.
6. The extracted topics and representative keywords are displayed through the Django web interface.

---

## 📦 Requirements

- Python 3.10+
- Django 4.2+
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
- Support for PDF and DOCX documents
- Topic coherence evaluation
- User authentication and login system
- Export results to PDF and Excel
- Integration of advanced topic modeling algorithms such as NMF and BERTopic

---

## 👥 Team

This project was developed collaboratively as part of an academic mini project.

| Team Member | Role |
|-------------|------|
| **Kalavalapalli Venkata Sesha Satyanarayana** | **Team Lead, Repository Owner & Core Contributor** |
| **Katta Udaya Lakshmi** | Core Contributor |
| **Kandala Vineetha** | Team Member |
| **Kukkala Dileep Babu** | Team Member |
| **Pinishetty Srinivas** | Team Member |

---

## 💻 My Contributions

As the **Team Lead, Repository Owner, and Core Contributor**, I was responsible for:

- Leading project planning, task allocation, and team coordination
- Designing the overall project workflow and implementation strategy
- Developing the topic modeling pipeline using **Python**, **Natural Language Processing (NLP)**, and **Latent Dirichlet Allocation (LDA)**
- Implementing Django backend modules and application functionality
- Integrating web scraping for URL-based text extraction
- Performing text preprocessing, feature extraction, and data analysis
- Testing, debugging, and integrating project components
- Preparing project documentation and maintaining the GitHub repository

---

## 🤝 Acknowledgements

I sincerely thank all my teammates for their valuable contributions, collaboration, and support throughout the development of this academic project.

---

## 📄 License

This project is intended solely for **educational and academic purposes**.
