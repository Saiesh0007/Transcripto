# validator.py
# Logic to validate transcripts is integrated into scraper.py.
# This file is present to satisfy architecture requirements.

def validate_record(record):
    if not record.get('transcript'):
        return False
    if not record.get('meeting_id'):
        return False
    return True
