import os
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
import torch

def train():
    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv("Transcripto/data/processed/meeting_transcripts_processed.csv")
    
    # We only need transcript and summary. Let's drop nan summaries.
    df = df.dropna(subset=['cleaned_transcript', 'summary'])
    
    # For testing and to prevent hours of training on CPU/Mac, we take a subset (e.g. 50 samples)
    # Use the entire dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"Training on {len(df)} samples...")
    
    dataset = Dataset.from_pandas(df)
    dataset = dataset.train_test_split(test_size=0.1)

    model_name = "t5-base"
    print(f"Loading model and tokenizer: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Prefix for T5
    prefix = "summarize: "
    max_input_length = 512
    max_target_length = 128

    def preprocess_function(examples):
        inputs = [prefix + str(doc) for doc in examples["cleaned_transcript"]]
        model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, padding="max_length")

        labels = tokenizer(text_target=[str(s) for s in examples["summary"]], max_length=max_target_length, truncation=True, padding="max_length")
        
        # Replace pad tokens with -100 so they are ignored by loss function
        labels["input_ids"] = [
            [(l if l != tokenizer.pad_token_id else -100) for l in label] for label in labels["input_ids"]
        ]

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    print("Tokenizing dataset...")
    tokenized_datasets = dataset.map(preprocess_function, batched=True)

    args = Seq2SeqTrainingArguments(
        output_dir="./models/t5-finetuned",
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=2, 
        per_device_eval_batch_size=2,
        weight_decay=0.01,
        save_total_limit=1,
        num_train_epochs=1,
        predict_with_generate=True,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        processing_class=tokenizer,
    )

    print("Starting training...")
    trainer.train()
    
    # Save the final model
    print("Saving final model...")
    trainer.save_model("./models/t5-finetuned")
    tokenizer.save_pretrained("./models/t5-finetuned")
    print("Done! Model saved to ./models/t5-finetuned")

if __name__ == "__main__":
    train()
