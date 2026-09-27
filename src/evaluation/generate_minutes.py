import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def generate_minutes():
    input_file = "outputs/meeting_minutes/extracted_minutes.csv"
    output_dir = "outputs/meeting_minutes/formatted/"
    
    if not os.path.exists(input_file):
        logging.error(f"Input file not found: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate minutes for first 3 meetings
    for idx, row in df.head(3).iterrows():
        title = row.get('title', 'Unknown Meeting')
        date = row.get('date', 'Unknown')
        participants = row.get('participants', 'Unknown')
        
        summary = row.get('generated_summary', 'Not specified')
        action_items = row.get('extracted_action_items', 'Not specified')
        decisions = row.get('extracted_decisions', 'Not specified')
        persons = row.get('extracted_persons', 'Not specified')
        dates = row.get('extracted_dates', 'Not specified')
        
        minutes = f"""MEETING MINUTES

Meeting Title: {title}
Date: {date}
Participants: {participants}

EXECUTIVE SUMMARY
{summary}

KEY DISCUSSION POINTS
Not specified (handled in executive summary for baseline)

DECISIONS
{decisions}

ACTION ITEMS
{action_items}

RESPONSIBLE PERSONS
{persons}

IMPORTANT DATES
{dates}
"""
        filename = os.path.join(output_dir, f"meeting_{idx+1}_minutes.txt")
        with open(filename, 'w') as f:
            f.write(minutes)
            
    logging.info(f"Generated formatted meeting minutes in {output_dir}")

if __name__ == "__main__":
    generate_minutes()
