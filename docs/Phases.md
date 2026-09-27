
---

# 5. `Phases.md`

```markdown
# AI Meeting Minutes Generator — Development Phases

## Phase 0 — Project Setup

### Tasks

- Inspect repository
- Create project structure
- Create virtual environment
- Install dependencies
- Create documentation
- Create README
- Create `.gitignore`

### Deliverables

```text
Repository
docs/
README.md
requirements.txt
Phase 1 — Research and Source Discovery
Goal

Find suitable publicly accessible meeting transcript sources.

Tasks
Search the web for candidate sources.
Identify sources containing real meeting transcripts.
Estimate available record count.
Inspect transcript quality.
Inspect metadata.
Check accessibility and usage restrictions.
Compare sources.
Select the most suitable source or compatible sources.
Deliverable
source_report.md

The report must include:

Source
URL
Number of candidate records
Transcript availability
Metadata availability
Accessibility
Restrictions
License/usage information
Reason for selection/rejection

Do not start large-scale scraping until this phase is completed.

Phase 2 — Scraper Development
Goal

Build a reliable scraper/parser.

Tasks
Discover transcript URLs
Fetch pages responsibly
Parse transcript content
Extract metadata
Generate meeting IDs
Deduplicate
Validate
Save raw data
Log errors
Deliverables
scraper/source_discovery.py
scraper/scraper.py
scraper/parser.py
scraper/validator.py
Phase 3 — Collect 100 Records
Team Allocation
Member 1 → 25
Member 2 → 25
Member 3 → 25
Member 4 → 25
Requirements
Exactly 100 valid records
Unique IDs
No duplicates
Source URL retained
Raw transcript retained
Deliverable
data/combined/meeting_transcripts_100.csv
Phase 4 — Dataset Validation

Check:

Duplicate URLs
Duplicate transcripts
Empty transcripts
Very short transcripts
Encoding issues
HTML artifacts
Missing fields
Incorrect IDs

Create a validation report.

Deliverable
outputs/dataset_validation_report.md
Phase 5 — Data Preprocessing

Perform:

HTML cleaning
Boilerplate removal
Whitespace normalization
Speaker normalization
Sentence segmentation
Tokenization
Lemmatization
Optional stop-word processing

Preserve raw data.

Deliverable
data/processed/meeting_transcripts_processed.csv
Phase 6 — Exploratory Data Analysis

Analyze:

Total meetings
Transcript lengths
Word counts
Sentence counts
Vocabulary
Frequent words
N-grams
Named entities
Speaker counts where available

Create visualizations.

Deliverables
notebooks/03_eda.ipynb
outputs/eda/
Phase 7 — NLP Baseline

Implement:

TF-IDF
Extractive sentence ranking
TextRank
NER
Keyword extraction

The baseline provides an interpretable benchmark.

Phase 8 — Summarization

Implement at least one extractive summarization method.

Recommended:

TF-IDF

or:

TextRank

Then, if computationally feasible, implement a pretrained transformer.

Possible models:

BART
T5
PEGASUS

Long transcripts must use chunking where required.

Phase 9 — Information Extraction

Extract:

Key Discussion Points
Decisions
Action Items
Responsible Persons
Deadlines
Important Dates
Next Steps

Use hybrid approaches where useful:

Rules + NER + NLP model

Do not rely only on keyword matching for complex relationships.

Phase 10 — Meeting Minutes Generation

Combine:

Summary
+
Discussion Points
+
Decisions
+
Action Items
+
Persons
+
Deadlines

Generate:

Meeting Minutes

for each selected evaluation/example meeting.

Phase 11 — Evaluation
Summarization

Use:

ROUGE-1
ROUGE-2
ROUGE-L

when reference summaries are available.

Information Extraction

Use:

Precision
Recall
F1

when reference annotations are available.

Human Evaluation

Evaluate:

Relevance
Coverage
Faithfulness
Readability
Action-item correctness
Phase 12 — Error Analysis

Inspect examples involving:

Incorrect summaries
Missing decisions
Incorrect task owners
Incorrect deadlines
Hallucinated information
Repeated information
Lost context
Long transcript failures

Document causes and potential fixes.

Phase 13 — Integration

Create an end-to-end workflow:

Transcript
    ↓
Preprocessing
    ↓
NLP Analysis
    ↓
Summarization
    ↓
Information Extraction
    ↓
Meeting Minutes
    ↓
Evaluation

The pipeline should be runnable without manually modifying intermediate data.

Phase 14 — Documentation

Update:

README.md
Architecture.md
Design.md
Memory.md
Phases.md
Project.md
Rules.md

with actual implementation details and results.

Do not leave documentation describing functionality that has not actually been implemented.

Phase 15 — Final Demonstration

Prepare examples covering:

Short meeting
Medium meeting
Long meeting
Meeting with clear action items
Meeting with decisions and deadlines

Show:

Original Transcript
        ↓
Preprocessed Text
        ↓
Generated Summary
        ↓
Extracted Information
        ↓
Final Meeting Minutes
Final Completion Checklist
 Source research completed
 Source report created
 Scraper implemented
 100 records collected
 25 records per member
 Duplicate detection completed
 Dataset validated
 Raw data preserved
 Preprocessing completed
 EDA completed
 NLP baseline completed
 Summarization completed
 Information extraction completed
 Minutes generator completed
 Evaluation completed
 Error analysis completed
 Documentation completed
 End-to-end pipeline tested
