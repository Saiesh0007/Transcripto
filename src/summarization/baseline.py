import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Ensure punkt is downloaded for sentence tokenization
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    logging.info("Downloading NLTK punkt data...")
    nltk.download('punkt')
    nltk.download('punkt_tab')

def extractive_summarize(text, num_sentences=5):
    if not isinstance(text, str) or not text.strip():
        return ""
    
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
        
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Score sentences based on their tf-idf sum
        sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
        
        # Get top indices
        top_indices = sentence_scores.argsort()[-num_sentences:][::-1]
        top_indices.sort() # sort chronologically
        
        summary = " ".join([sentences[i] for i in top_indices])
        return summary
    except Exception as e:
        logging.error(f"Error in extractive_summarize: {e}")
        return ""

def run_summarization():
    input_file = "data/processed/meeting_transcripts_processed.csv"
    output_file = "outputs/summaries/baseline_summaries.csv"
    
    if not os.path.exists(input_file):
        logging.error(f"Input file not found: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    logging.info(f"Loaded {len(df)} records for baseline summarization.")
    
    logging.info("Running TF-IDF extractive summarization...")
    df['generated_summary'] = df['cleaned_transcript'].apply(lambda x: extractive_summarize(x, num_sentences=5))
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    logging.info(f"Saved baseline summaries to {output_file}")
    
if __name__ == "__main__":
    run_summarization()
