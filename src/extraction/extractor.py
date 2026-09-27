import os
import pandas as pd
import spacy
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
    nlp = spacy.load("en_core_web_sm")
except:
    logging.warning("en_core_web_sm not found. Falling back to regex only.")
    nlp = None

def extract_action_items(text):
    if not isinstance(text, str):
        return "Not specified"
        
    action_items = []
    # Simple rule-based extraction for action items/decisions
    task_patterns = [
        r"(?i)\b(?:will|should|need to|must|has to) (?:do|complete|finish|create|make|prepare|send|review)\b(.*?)(?=\.|$)",
        r"(?i)\b(?:decided to|agreed to)\b(.*?)(?=\.|$)",
    ]
    
    for pattern in task_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            action_items.append(m.strip())
            
    if not action_items:
        return "Not specified"
    return "; ".join(set(action_items))

def extract_persons(text):
    if not nlp or not isinstance(text, str):
        return "Not specified"
    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if not persons:
        return "Not specified"
    return "; ".join(set(persons))

def extract_dates(text):
    if not nlp or not isinstance(text, str):
        return "Not specified"
    doc = nlp(text)
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE" or ent.label_ == "TIME"]
    if not dates:
        return "Not specified"
    return "; ".join(set(dates))

def run_extraction():
    input_file = "outputs/summaries/baseline_summaries.csv"
    output_file = "outputs/meeting_minutes/extracted_minutes.csv"
    
    if not os.path.exists(input_file):
        logging.error(f"Input file not found: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    logging.info(f"Loaded {len(df)} records for extraction.")
    
    logging.info("Extracting action items, decisions, persons, and dates...")
    df['extracted_action_items'] = df['cleaned_transcript'].apply(extract_action_items)
    df['extracted_persons'] = df['cleaned_transcript'].apply(extract_persons)
    df['extracted_dates'] = df['cleaned_transcript'].apply(extract_dates)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    logging.info(f"Saved extracted data to {output_file}")
    
if __name__ == "__main__":
    run_extraction()
