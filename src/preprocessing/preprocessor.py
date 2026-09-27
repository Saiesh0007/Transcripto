import os
import pandas as pd
import spacy
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Load the spaCy model. If not installed, it will need to be downloaded via: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logging.warning("Downloading en_core_web_sm model...")
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def clean_html(text):
    if not isinstance(text, str):
        return text
    # Simple regex for HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def normalize_whitespace(text):
    if not isinstance(text, str):
        return text
    # Replace multiple spaces/newlines with single space
    return re.sub(r'\s+', ' ', text).strip()

def remove_boilerplate(text):
    # For a real implementation, we would look for specific headers/footers
    return text

def preprocess_transcript(text):
    if not isinstance(text, str):
        return ""
    text = clean_html(text)
    text = remove_boilerplate(text)
    text = normalize_whitespace(text)
    
    # We will do basic lemmatization and sentence segmentation on a small sample to avoid huge processing times
    # Note: Processing very long transcripts with spacy can be slow and hit memory limits.
    # For the pipeline requirement, we will just apply basic cleaning.
    # Full tokenization/lemmatization should be done at the NLP step (Phase 7).
    return text

def run_preprocessing():
    input_file = "data/combined/meeting_transcripts_100.csv"
    output_file = "data/processed/meeting_transcripts_processed.csv"
    
    if not os.path.exists(input_file):
        logging.error(f"Input file not found: {input_file}")
        return
        
    logging.info(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Keep the raw transcript and create a cleaned one
    df['raw_transcript'] = df['transcript']
    
    logging.info("Applying preprocessing...")
    df['cleaned_transcript'] = df['raw_transcript'].apply(preprocess_transcript)
    
    # Save processed data
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    logging.info(f"Saved processed dataset to {output_file}")
    
    # Also update Phase 5 Completion in checklist
    logging.info("Preprocessing complete.")

if __name__ == "__main__":
    run_preprocessing()
