---

# 6. `Rules.md`

```markdown
# AI Meeting Minutes Generator — Rules

## 1. Master Rule

This project must be developed as a complete end-to-end NLP system.

The agent must not stop after creating the dataset.

Required workflow:

```text
Research
→ Source Discovery
→ Source Validation
→ Web Scraping
→ Data Validation
→ Data Integration
→ Preprocessing
→ EDA
→ NLP Baseline
→ Summarization
→ Information Extraction
→ Minutes Generation
→ Evaluation
→ Error Analysis
→ Documentation
2. Dataset Rules
Final target = exactly 100 valid meeting records.
Each member contributes 25 records.
IDs must be unique.
Recommended IDs: M001 to M100.
Duplicate records do not count toward the 100.
Every record must retain its source URL.
Raw transcript must be preserved.
Do not fabricate missing metadata.
Do not fabricate reference summaries.
Do not fabricate action items or decisions.
3. Web Scraping Rules
Allowed
Public web pages
Public datasets
Public transcript pages
Public downloadable transcript files
Prohibited

Do not:

Bypass login systems
Bypass authentication
Bypass CAPTCHAs
Circumvent access controls
Scrape private content
Circumvent technical restrictions
Responsible Scraping

Use:

Reasonable request delays
Retry with backoff
Timeouts
Logging
Caching where practical

Respect applicable website access rules and robots.txt where relevant.

If a website does not permit the required automated access, find another source rather than attempting to bypass its restrictions.

4. Source Selection Rules

Do not automatically select the first website found.

Compare multiple sources.

Prefer sources with:

Large number of records
Complete transcripts
Consistent structure
Useful metadata
Stable URLs
Public accessibility
Clear provenance

The selected source must be documented.

5. Data Quality Rules

Every record should be checked for:

Unique ID
Valid URL
Non-empty transcript
Meaningful transcript length
Duplicate status
Encoding
Scraping artifacts

Records that fail validation should be logged.

Do not silently discard records.

6. Raw Data Rule

Never overwrite the original transcript.

Use:

raw_transcript
cleaned_transcript

as separate fields or files.

7. Preprocessing Rules

Apply a consistent preprocessing pipeline.

Preserve information necessary for:

Speaker identification
Decisions
Action items
Dates
Deadlines

Do not aggressively remove stop words from transformer input.

8. NLP Rules

Start with an interpretable baseline.

Recommended:

TF-IDF
TextRank
NER
Keyword extraction

Then implement advanced transformer-based approaches if useful and feasible.

Every NLP technique must have a clear purpose.

9. Model Rules

The project uses one integrated pipeline/model approach.

The four-member split is only a data collection split.

Do not create:

Model 1 → Member 1
Model 2 → Member 2
Model 3 → Member 3
Model 4 → Member 4

unless explicitly required by the project supervisor.

Instead:

100 combined records
        ↓
Single project pipeline/model
10. Pretrained Model Rule

If using a pretrained model:

Clearly state:

Model name
Model source
Model purpose
Whether inference or fine-tuning is performed
Dataset role
Limitations

Never claim that a pretrained model was trained from scratch by the project.

11. Train/Test Rule

If a train/validation/test split is used, document it.

Do not use the same records for tuning and final evaluation and then present the result as unbiased test performance.

Because the dataset contains only 100 records, be conservative when interpreting evaluation results.

12. Summarization Rules

Generated summaries must:

Preserve meaning
Focus on important information
Avoid unnecessary repetition
Avoid unsupported claims
Avoid hallucination

For long transcripts, use chunking or hierarchical summarization.

Do not simply truncate long transcripts unless the limitations are explicitly documented.

13. Action Item Rules

An action item should preferably contain:

Task
Responsible Person
Deadline

Example:

Sarah: I will finish the frontend by Friday.

Correct extraction:

Task: Finish frontend
Responsible: Sarah
Deadline: Friday

Do not assign responsibility based solely on who discussed the task.

14. Decision Rules

Distinguish:

Suggestion
Discussion
Proposal
Decision

A proposal is not automatically a decision.

A decision must have contextual evidence of agreement/finalization.

15. Deadline Rules

Extract explicit deadlines.

Examples:

by Friday
before Monday
on 20 October
next week
tomorrow

Relative dates should only be converted to actual calendar dates when enough context exists.

Preserve the original expression.

16. Hallucination Rule

The system must NEVER invent:

People
Tasks
Decisions
Deadlines
Dates
Organizations
Meeting details

If information is unavailable:

Not specified
17. Evaluation Rules

Use appropriate metrics.

Summarization
ROUGE-1
ROUGE-2
ROUGE-L
Information Extraction
Precision
Recall
F1-score

when reference annotations exist.

Also perform qualitative evaluation.

Do not manually edit model outputs to improve evaluation scores.

18. Reproducibility Rules

Maintain:

requirements.txt
README.md
source code
notebooks
dataset documentation
logs
outputs
configuration

Record:

Dataset version
Model name
Model version
Parameters
Preprocessing settings
Evaluation settings
19. Error Handling

The system must log:

Failed URLs
Parsing failures
Empty transcripts
Duplicate records
Encoding errors
Model errors
Unexpected output formats

Errors must not be silently ignored.

20. Academic Integrity

Clearly identify:

External sources
External datasets
Pretrained models
Third-party libraries
Reference summaries
Original project implementation

Do not present external model capabilities or external datasets as original work.

21. Agent Execution Rules

When Antigravity starts the project:

Step 1

Inspect the existing repository.

Do not overwrite existing project files without checking them first.

Step 2

Read all files in docs/.

Step 3

Research candidate meeting-transcript sources.

Step 4

Create source_report.md.

Step 5

Select a suitable source.

Step 6

Implement and test the scraper on a small number of records first.

Step 7

Only after successful validation, collect the required 100 records.

Step 8

Validate and deduplicate the dataset.

Step 9

Create the preprocessing pipeline.

Step 10

Perform EDA.

Step 11

Implement the NLP baseline.

Step 12

Implement summarization.

Step 13

Implement meeting information extraction.

Step 14

Implement meeting-minutes generation.

Step 15

Implement evaluation.

Step 16

Perform error analysis.

Step 17

Update documentation with actual results.

Step 18

Run the complete end-to-end pipeline.

22. Do Not Fake Completion

Do not mark a phase as completed simply because code exists.

A phase is complete only when:

Code exists.
Code runs.
Output has been generated.
Output has been checked.
Documentation reflects the actual result.
23. Definition of Done
[ ] Public source researched
[ ] Source validated
[ ] Scraper implemented
[ ] Scraper tested
[ ] 100 valid transcripts collected
[ ] 25 records per member
[ ] Duplicates removed
[ ] Source URLs preserved
[ ] Raw dataset preserved
[ ] Processed dataset generated
[ ] EDA completed
[ ] NLP preprocessing completed
[ ] Extractive baseline completed
[ ] Advanced summarization evaluated if feasible
[ ] NER/information extraction completed
[ ] Decisions extracted
[ ] Action items extracted
[ ] Deadlines extracted
[ ] Meeting minutes generated
[ ] Evaluation completed
[ ] Error analysis completed
[ ] Documentation updated
[ ] End-to-end pipeline tested
24. Final Principle

The primary goal is not simply to produce a large amount of code.

The goal is to produce a working, explainable, reproducible NLP project that can demonstrate:

Real Meeting Transcript
        ↓
Data Collection
        ↓
Preprocessing
        ↓
NLP Analysis
        ↓
Summarization
        ↓
Information Extraction
        ↓
AI Meeting Minutes
        ↓
Evaluation

Every major project decision should be documented and justified.