import streamlit as st
import pandas as pd
import os
import sys

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from preprocessing.preprocessor import preprocess_transcript
from summarization.baseline import extractive_summarize
from extraction.extractor import extract_action_items, extract_persons, extract_dates

st.set_page_config(page_title="AI Meeting Minutes Generator", layout="wide", page_icon="📝")

st.title("📝 AI Meeting Minutes Generator")
st.markdown("An NLP pipeline that accepts unstructured meeting transcripts and produces structured meeting minutes.")

# --- Sidebar for Evaluation Metrics & Info ---
st.sidebar.header("📊 Project Evaluation")

eval_path = "outputs/evaluation/evaluation_report.txt"
if os.path.exists(eval_path):
    with open(eval_path, "r") as f:
        eval_text = f.read()
    st.sidebar.markdown(eval_text)
else:
    st.sidebar.markdown("""
    **ROUGE Metrics (Extractive Baseline)**
    - ROUGE-1 F1: 0.1910
    - ROUGE-2 F1: 0.0350
    - ROUGE-L F1: 0.1021
    """)

st.sidebar.markdown("---")
st.sidebar.header("Dataset Details")
st.sidebar.markdown("""
- **Source**: QMSum (HuggingFace)
- **Records**: 100 
- **Method**: TF-IDF & spaCy NER
""")

# --- Main App ---
tab1, tab2 = st.tabs(["Run on Dataset", "Paste Custom Transcript"])

# Load dataset
@st.cache_data
def load_data():
    csv_path = "data/processed/meeting_transcripts_processed.csv"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()

df = load_data()

with tab1:
    if not df.empty:
        st.subheader("Select a Meeting from the 100-Record Dataset")
        meeting_options = df['meeting_id'].astype(str).tolist()
        selected_meeting = st.selectbox("Meeting ID", meeting_options)
        
        row = df[df['meeting_id'].astype(str) == selected_meeting].iloc[0]
        raw_transcript = row.get('transcript', '')
        
        with st.expander("View Raw Transcript"):
            st.write(raw_transcript)
            
        if st.button("Generate Minutes", key="btn_dataset"):
            with st.spinner("Running NLP Pipeline..."):
                cleaned = row.get('cleaned_transcript', preprocess_transcript(raw_transcript))
                summary = extractive_summarize(cleaned)
                action_items = extract_action_items(cleaned)
                persons = extract_persons(cleaned)
                dates = extract_dates(cleaned)
                
            st.success("Minutes Generated!")
            st.markdown("### 📄 MEETING MINUTES")
            st.markdown(f"**Meeting Title:** Meeting {selected_meeting}")
            
            st.markdown("#### 📝 EXECUTIVE SUMMARY")
            st.info(summary)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("#### 🎯 ACTION ITEMS & DECISIONS")
                st.write(action_items)
            with col2:
                st.markdown("#### 👤 RESPONSIBLE PERSONS")
                st.write(persons)
            with col3:
                st.markdown("#### 📅 IMPORTANT DATES")
                st.write(dates)
    else:
        st.warning("Dataset not found. Please run the scraper first.")

with tab2:
    st.subheader("Process a New Meeting")
    custom_text = st.text_area("Paste meeting transcript here:", height=200)
    
    if st.button("Generate Minutes", key="btn_custom"):
        if custom_text.strip():
            with st.spinner("Running NLP Pipeline..."):
                cleaned = preprocess_transcript(custom_text)
                summary = extractive_summarize(cleaned)
                action_items = extract_action_items(cleaned)
                persons = extract_persons(cleaned)
                dates = extract_dates(cleaned)
                
            st.success("Minutes Generated!")
            st.markdown("### 📄 MEETING MINUTES")
            
            st.markdown("#### 📝 EXECUTIVE SUMMARY")
            st.info(summary)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("#### 🎯 ACTION ITEMS & DECISIONS")
                st.write(action_items)
            with col2:
                st.markdown("#### 👤 RESPONSIBLE PERSONS")
                st.write(persons)
            with col3:
                st.markdown("#### 📅 IMPORTANT DATES")
                st.write(dates)
        else:
            st.error("Please paste a transcript first.")
