
---

# 3. `Design.md`

```markdown
# AI Meeting Minutes Generator — Design

## 1. Design Objective

The system should convert long, unstructured meeting transcripts into concise and structured meeting minutes.

The design should prioritize:

- Accuracy
- Reproducibility
- Explainability
- Faithfulness to the transcript
- Ease of evaluation

---

# 2. Dataset Design

The final dataset contains exactly 100 meeting transcripts.

```text
Member 1 = 25
Member 2 = 25
Member 3 = 25
Member 4 = 25
3. Canonical Dataset Schema

Use:

meeting_id
title
date
participants
transcript
summary
action_items
decisions
source_url
source_name
collection_member
license_or_usage_note

Derived fields may include:

cleaned_transcript
word_count
sentence_count
speaker_count
language
4. Data Storage Design

Raw records:

data/raw/

Combined dataset:

data/combined/meeting_transcripts_100.csv

Processed dataset:

data/processed/meeting_transcripts_processed.csv

The original transcript must always remain available.

5. Web Scraping Design
Step 1 — Source Discovery

Search for public meeting transcript sources.

The agent should compare multiple candidate sources.

A source should preferably:

Contain many records
Provide complete transcripts
Have consistent structure
Provide metadata
Be publicly accessible
Have stable URLs
Step 2 — Source Validation

Before scraping, create:

source_report.md

The report should document:

Source:
URL:
Candidate record count:
Transcript available:
Metadata available:
Access restrictions:
License/usage information:
Decision:
Reason:
Step 3 — URL Discovery

Find transcript pages or downloadable transcript records.

Store discovered URLs before scraping all pages.

Step 4 — Transcript Extraction

For each record extract:

title
date
participants
transcript
source_url
source_name

Do not fabricate missing metadata.

Step 5 — Deduplication

Check:

URL duplicates
Identical transcripts
Near-duplicate titles
Duplicate meeting IDs
6. Data Validation Design

A record is valid when:

meeting_id exists
AND
transcript is non-empty
AND
source_url exists
AND
record is not a duplicate

Very short transcripts should be flagged for review.

7. Preprocessing Design

The preprocessing pipeline should be:

Raw Transcript
      ↓
HTML Cleaning
      ↓
Boilerplate Removal
      ↓
Whitespace Normalization
      ↓
Speaker Normalization
      ↓
Sentence Segmentation
      ↓
Tokenization
      ↓
Lemmatization
      ↓
Clean Transcript
8. Important Preprocessing Rule

Do not remove information needed for:

Speaker identification
Decisions
Action items
Dates
Deadlines

Do not use aggressive stop-word removal on the text supplied to transformer summarization models.

Keep separate representations for classical NLP and transformer-based processing when necessary.

9. Summarization Design
Baseline

Implement an extractive baseline.

Preferred:

TF-IDF sentence ranking

or:

TextRank
Advanced

If computational resources permit, implement a pretrained transformer.

Possible models:

BART
T5
PEGASUS

The exact model should be selected based on transcript length, available compute, and compatibility.

10. Long Transcript Handling

Do not blindly truncate long meetings.

Use:

Long Transcript
      ↓
Sentence Segmentation
      ↓
Chunking
      ↓
Chunk-level Processing
      ↓
Intermediate Summaries
      ↓
Final Summary

This should preserve important information from later parts of the meeting.

11. Information Extraction
Key Discussion Points

Use methods such as:

TF-IDF
Keyword extraction
KeyBERT
Topic modeling
Sentence ranking
Decisions

Identify explicit decision statements using contextual analysis.

Possible signals:

decided
agreed
approved
finalized
selected
will proceed

These are signals only; surrounding context must be considered.

Action Items

Identify task statements such as:

Person will do X.
Person should do X.
Please complete X.
Let's assign X.
X needs to be completed by DATE.
Responsible Person

Only identify a person as responsible when the transcript explicitly supports the assignment.

Deadlines

Extract explicit date/time expressions using:

NER
Regex
Rule-based extraction
12. Final Minutes Design

Use:

MEETING MINUTES

Meeting Title:
Date:
Participants:

EXECUTIVE SUMMARY

KEY DISCUSSION POINTS

1.
2.
3.

DECISIONS

1.
2.

ACTION ITEMS

| Task | Responsible Person | Deadline |
|------|--------------------|----------|

IMPORTANT DATES

NEXT STEPS
13. Evaluation Design
Summarization

If reference summaries exist:

ROUGE-1
ROUGE-2
ROUGE-L
Extraction

If reference labels exist:

Precision
Recall
F1-score
Human Evaluation

Evaluate a representative sample for:

Relevance
Coverage
Faithfulness
Readability
Action-item accuracy
14. Reproducibility

Record:

Dataset version
Source
Model name
Model version
Parameters
Preprocessing settings
Evaluation settings

Use fixed random seeds where applicable.

15. Technology Preference

Preferred stack:

Python
Pandas
NumPy
NLTK
spaCy
Scikit-learn
Transformers
PyTorch
BeautifulSoup
Requests

Use Google Colab/Jupyter where appropriate.

Do not introduce unnecessary infrastructure such as Docker unless specifically required.