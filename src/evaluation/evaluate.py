import os
import pandas as pd
from rouge_score import rouge_scorer
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_evaluation():
    input_file = "outputs/meeting_minutes/extracted_minutes.csv"
    output_file = "outputs/evaluation/evaluation_report.txt"
    
    if not os.path.exists(input_file):
        logging.error(f"Input file not found: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    logging.info(f"Loaded {len(df)} records for evaluation.")
    
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    rouge1_scores = []
    rouge2_scores = []
    rougeL_scores = []
    
    for _, row in df.iterrows():
        ref_summary = str(row['summary'])
        gen_summary = str(row.get('generated_summary', ''))
        
        scores = scorer.score(ref_summary, gen_summary)
        rouge1_scores.append(scores['rouge1'].fmeasure)
        rouge2_scores.append(scores['rouge2'].fmeasure)
        rougeL_scores.append(scores['rougeL'].fmeasure)
        
    avg_r1 = sum(rouge1_scores) / len(rouge1_scores) if rouge1_scores else 0
    avg_r2 = sum(rouge2_scores) / len(rouge2_scores) if rouge2_scores else 0
    avg_rL = sum(rougeL_scores) / len(rougeL_scores) if rougeL_scores else 0
    
    logging.info(f"Average ROUGE-1 F1: {avg_r1:.4f}")
    logging.info(f"Average ROUGE-2 F1: {avg_r2:.4f}")
    logging.info(f"Average ROUGE-L F1: {avg_rL:.4f}")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        f.write("# Evaluation Report\n\n")
        f.write("## Summarization Metrics (ROUGE)\n")
        f.write(f"- ROUGE-1 F1: {avg_r1:.4f}\n")
        f.write(f"- ROUGE-2 F1: {avg_r2:.4f}\n")
        f.write(f"- ROUGE-L F1: {avg_rL:.4f}\n")
        
    logging.info(f"Evaluation report saved to {output_file}")

if __name__ == "__main__":
    run_evaluation()
