# AI Meeting Minutes Generator — Architecture

## 1. System Architecture

The system is designed as an end-to-end NLP pipeline.

```text
                PUBLIC MEETING SOURCES
                         |
                         v
                 SOURCE DISCOVERY
                         |
                         v
                SOURCE VALIDATION
                         |
                         v
                   WEB SCRAPER
                         |
                         v
                RAW TRANSCRIPTS
                         |
                         v
                 DATA VALIDATION
                         |
                         v
                DATA INTEGRATION
                         |
                         v
              100-RECORD DATASET
                         |
                         v
                PREPROCESSING
                         |
                         v
               EXPLORATORY ANALYSIS
                         |
                         v
                  NLP PIPELINE
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
         NER       KEYWORD EXTRACTION  SUMMARIZATION
          |              |              |
          +--------------+--------------+
                         |
                         v
              INFORMATION EXTRACTION
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      DISCUSSION      DECISIONS     ACTION ITEMS
       POINTS                           |
                                       v
                             PERSON / DEADLINE
                         |
                         v
                 MINUTES GENERATOR
                         |
                         v
                STRUCTURED MINUTES
                         |
                         v
                    EVALUATION

2. Source Discovery Layer

The first component identifies suitable public meeting-transcript sources.

The agent must research candidate sources before writing the final scraper.

For every candidate source, record:

Source name
URL
Number of available records
Transcript availability
Metadata availability
Accessibility
Restrictions
License/usage information
Suitability
3. Web Scraping Layer

The scraper should:

Discover transcript pages.
Extract transcript URLs.
Download permitted public pages.
Parse transcript text.
Extract metadata.
Generate unique IDs.
Detect duplicates.
Validate records.
Save raw data.
Log failures.

The scraper must use reasonable request delays and should not bypass authentication, CAPTCHAs, or access restrictions.

4. Data Validation Layer

Each record must be checked for:

Valid meeting ID
Non-empty transcript
Valid source URL
Useful transcript length
Duplicate content
Encoding problems
Scraping artifacts

Invalid records should be logged and reviewed.

5. Data Integration Layer

The four member datasets must be combined:

Member 1 → 25
Member 2 → 25
Member 3 → 25
Member 4 → 25
                ↓
             100 records

The final dataset should have standardized column names and data types.

6. Preprocessing Layer

The raw transcript should never be overwritten.

Maintain:

raw_transcript
cleaned_transcript

Processing should include:

HTML cleaning
Boilerplate removal
Whitespace normalization
Speaker-label preservation
Sentence segmentation
Tokenization
Lemmatization
Optional stop-word processing
7. NLP Layer

The NLP pipeline consists of:

Clean Transcript
      |
      +---- Tokenization
      |
      +---- Lemmatization
      |
      +---- POS Tagging
      |
      +---- Named Entity Recognition
      |
      +---- Keyword Extraction
      |
      +---- Summarization
      |
      +---- Information Extraction
8. Summarization Layer

Implement a baseline first.

Recommended baseline:

TF-IDF sentence scoring
TextRank

Then optionally implement:

BART
T5
PEGASUS

Long transcripts should be processed using chunking/hierarchical summarization if required.

9. Information Extraction Layer

The system should extract:

Discussion Points
Decisions
Action Items
Responsible Persons
Deadlines
Important Dates
Next Steps

The extraction system must use transcript context and must not invent information.

10. Minutes Generation Layer

The minutes generator combines the outputs of summarization and information extraction.

Transcript
    |
    +--> Summary
    |
    +--> Key Points
    |
    +--> Decisions
    |
    +--> Action Items
    |
    +--> Persons
    |
    +--> Deadlines
             |
             v
      Meeting Minutes
11. Evaluation Layer

The system should evaluate:

Summarization
ROUGE-1
ROUGE-2
ROUGE-L
Information Extraction
Precision
Recall
F1
Qualitative Evaluation
Relevance
Coverage
Faithfulness
Readability
Action-item correctness
12. Recommended Repository
AI-Meeting-Minutes-Generator/
│
├── README.md
│
├── docs/
│   ├── Architecture.md
│   ├── Design.md
│   ├── Memory.md
│   ├── Phases.md
│   ├── Project.md
│   └── Rules.md
│
├── data/
│   ├── raw/
│   │   ├── member1/
│   │   ├── member2/
│   │   ├── member3/
│   │   └── member4/
│   │
│   ├── combined/
│   │   └── meeting_transcripts_100.csv
│   │
│   └── processed/
│       └── meeting_transcripts_processed.csv
│
├── scraper/
│   ├── source_discovery.py
│   ├── scraper.py
│   ├── parser.py
│   └── validator.py
│
├── notebooks/
│   ├── 01_validation.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_summarization.ipynb
│   ├── 05_extraction.ipynb
│   └── 06_evaluation.ipynb
│
├── src/
│   ├── preprocessing/
│   ├── summarization/
│   ├── extraction/
│   └── evaluation/
│
├── outputs/
│   ├── summaries/
│   ├── meeting_minutes/
│   └── evaluation/
│
└── logs/