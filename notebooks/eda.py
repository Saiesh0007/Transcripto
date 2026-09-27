import os
import pandas as pd
import matplotlib.pyplot as plt
import logging
from collections import Counter
import re

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_eda():
    input_file = "data/processed/meeting_transcripts_processed.csv"
    output_dir = "outputs/eda/"
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(input_file):
        logging.error(f"File not found: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    logging.info(f"Loaded {len(df)} records for EDA.")
    
    # Analyze total meetings
    total_meetings = len(df)
    
    # Transcript lengths (characters)
    df['char_length'] = df['cleaned_transcript'].astype(str).apply(len)
    
    # Word counts (simple whitespace split)
    df['word_count'] = df['cleaned_transcript'].astype(str).apply(lambda x: len(x.split()))
    
    # Sentence counts (simple period split)
    df['sentence_count'] = df['cleaned_transcript'].astype(str).apply(lambda x: len(x.split('.')))
    
    # Vocabulary & frequent words
    all_words = ' '.join(df['cleaned_transcript'].astype(str)).lower()
    words = re.findall(r'\b\w+\b', all_words)
    word_freq = Counter(words)
    most_common = word_freq.most_common(20)
    
    logging.info(f"Average char length: {df['char_length'].mean()}")
    logging.info(f"Average word count: {df['word_count'].mean()}")
    logging.info(f"Average sentence count: {df['sentence_count'].mean()}")
    logging.info(f"Vocabulary size: {len(word_freq)}")
    
    # Plot word counts
    plt.figure(figsize=(10, 6))
    plt.hist(df['word_count'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Transcript Word Counts')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'word_counts_hist.png'))
    plt.close()
    
    # Plot most frequent words
    plt.figure(figsize=(12, 6))
    words_top, freqs_top = zip(*most_common)
    plt.bar(words_top, freqs_top, color='coral')
    plt.title('Top 20 Most Frequent Words')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, 'top_words.png'))
    plt.close()
    
    # Save a text report
    report_path = os.path.join(output_dir, "eda_report.txt")
    with open(report_path, "w") as f:
        f.write(f"Total Meetings: {total_meetings}\n")
        f.write(f"Average Word Count: {df['word_count'].mean()}\n")
        f.write(f"Average Sentence Count: {df['sentence_count'].mean()}\n")
        f.write(f"Total Vocabulary Size: {len(word_freq)}\n")
        f.write("Top 20 Words:\n")
        for w, count in most_common:
            f.write(f"{w}: {count}\n")
            
    logging.info(f"EDA complete. Outputs saved to {output_dir}")

if __name__ == "__main__":
    run_eda()
