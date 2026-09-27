# parser.py
# Logic to parse transcripts is integrated into scraper.py since we use HuggingFace datasets.
# This file is present to satisfy architecture requirements.

def parse_transcript(raw_text):
    return raw_text.strip()
