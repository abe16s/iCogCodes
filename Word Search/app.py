from flask import Flask, render_template, request, redirect, url_for, flash
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import PyPDF2
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production

# Download NLTK resources if not already downloaded
nltk.download("stopwords", quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize stopwords and lemmatizer
stopwords_list = set(stopwords.words('english'))
lemmer = WordNetLemmatizer()

# Global vectorizer instance
vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), stop_words=list(stopwords_list))

def preprocess_text(text):
    # Text preprocessing function
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)  # Remove punctuation
    text = re.sub(r'[0-9]', '', text)  # Remove digits
    return ' '.join([lemmer.lemmatize(word) for word in text.split() if word not in stopwords_list])

def extract_text_from_pdf(pdf_file):
    # Extract text from PDF
    text = ""
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""  # Handle None if extract_text fails
    return text

def partition_text(text):
    # Partition the extracted text into sections based on paragraphs
    sections = text.split('.')  # Split on sentences (you can adjust this)
    return [section.strip() for section in sections if section.strip()]  # Clean empty sections

def get_similar_articles(q, df, top_results):
    # Get similar articles based on cosine similarity
    # Fit the vectorizer on the document texts
    X = vectorizer.fit_transform(df['documents'])
    
    # Transform the query
    q_vec = vectorizer.transform([q]).toarray().reshape(X.shape[1],)
    
    sim = {}
    for i in range(len(df)):
        # Calculate cosine similarity
        doc_vec = X[i].toarray().flatten()  # Flatten the matrix to 1D array
        sim[i] = np.dot(doc_vec, q_vec) / (np.linalg.norm(doc_vec) * np.linalg.norm(q_vec))
    
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)[:top_results]
    return [(df['titles'][i], df['documents'][i], v) for i, v in sim_sorted if v > 0]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        query = request.form['query']
        top_results = int(request.form['top_results'])
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and file.filename.endswith('.pdf'):
            # Save the file temporarily
            pdf_path = os.path.join('uploads', file.filename)
            file.save(pdf_path)
            
            pdf_text = extract_text_from_pdf(pdf_path)
            documents = partition_text(pdf_text)  # Partition the text into sections
            titles = [f'Section {i + 1}' for i in range(len(documents))]  # Generate titles for sections
            df = pd.DataFrame({'titles': titles, 'documents': documents})

            processed_query = preprocess_text(query)
            similar_articles = get_similar_articles(processed_query, df, top_results)

            # Clean up the uploaded file after processing
            os.remove(pdf_path)

            return render_template('results.html', similar_articles=similar_articles)

    return render_template('upload.html')

if __name__ == '__main__':
    # Ensure the uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
