# AI Meeting Minutes Generator

## 1. Project Overview

**Project Name:** AI Meeting Minutes Generator

**Domain:** Natural Language Processing (NLP)

**Project Type:** NLP Course Mini Project

The objective of this project is to develop an NLP-based AI Meeting Minutes Generator that accepts meeting transcripts and automatically produces structured meeting minutes.

The system should process long and unstructured meeting conversations and identify the most important information, including:

- Meeting summary
- Key discussion points
- Decisions
- Action items
- Responsible persons
- Deadlines
- Important dates
- Next steps

The project must be developed as a complete end-to-end pipeline beginning with public meeting-transcript data collection and ending with evaluation of the generated meeting minutes.

---

## 2. Problem Statement

Meetings contain large amounts of conversational information involving discussions, decisions, tasks, responsibilities, and deadlines. Manually reviewing lengthy meeting transcripts and preparing accurate meeting minutes is time-consuming and may result in important information being missed.

The proposed system will use Natural Language Processing techniques to automatically analyze meeting transcripts, summarize the discussion, extract important information, and generate concise and structured meeting minutes.

---

## 3. Project Objectives

The system should:

1. Study NLP applications relevant to meeting analysis.
2. Identify suitable publicly accessible meeting transcript sources.
3. Collect a dataset of exactly 100 valid meeting transcript records.
4. Divide the data collection workload equally among four team members.
5. Preprocess and normalize the collected transcripts.
6. Perform exploratory analysis of the dataset.
7. Apply NLP techniques to meeting transcripts.
8. Implement text summarization.
9. Extract important meeting information.
10. Identify decisions and action items.
11. Identify responsible persons when explicitly supported by the transcript.
12. Identify deadlines and important dates.
13. Generate structured meeting minutes.
14. Evaluate the generated output.
15. Perform error analysis.
16. Maintain reproducible documentation and code.

---

## 4. Team Dataset Requirement

There are four members in the project team.

The 100 records will be collected as follows:

| Team Member | Records |
|-------------|---------|
| Member 1 | 25 |
| Member 2 | 25 |
| Member 3 | 25 |
| Member 4 | 25 |
| **Total** | **100** |

The 25-25-25-25 split represents the **data collection workload**.

It does NOT mean that four separate models should be created.

All 100 records must eventually be combined into one standardized dataset and used by the project pipeline.

---

## 5. Dataset Requirements

The final dataset should preferably contain:

| Field | Description |
|-------|-------------|
| meeting_id | Unique meeting identifier |
| title | Meeting title |
| date | Meeting date, if available |
| participants | Participants/speakers, if available |
| transcript | Full meeting transcript |
| summary | Reference summary, if available |
| action_items | Reference action items, if available |
| decisions | Reference decisions, if available |
| source_url | Original source URL |
| source_name | Website/dataset name |
| collection_member | Team member who collected the record |
| license_or_usage_note | Source/license information |

Required fields:

- `meeting_id`
- `transcript`
- `source_url`
- `source_name`
- `collection_member`

---

## 6. Data Collection Requirements

The system must first research possible public sources containing meeting transcripts.

Do NOT immediately scrape the first website found.

Candidate sources should be evaluated based on:

- Number of available transcripts
- Transcript quality
- Transcript length
- Metadata availability
- Public accessibility
- Consistency of page structure
- Source provenance
- Access restrictions
- Terms of use
- Suitability for academic use

The source should provide enough data to obtain 100 useful meeting records.

If one source cannot provide enough suitable records, multiple compatible public sources may be considered.

---

## 7. NLP Tasks

The project should cover the following NLP tasks.

### Text Preprocessing

- HTML removal
- Noise removal
- Whitespace normalization
- Sentence segmentation
- Tokenization
- Stop-word handling
- Lemmatization

### Exploratory NLP

- Transcript length
- Sentence count
- Word frequency
- Vocabulary analysis
- N-grams
- Named entities

### Text Summarization

At least one summarization approach should be implemented.

Possible methods:

- TF-IDF extractive summarization
- TextRank
- Transformer-based summarization

### Information Extraction

The system should attempt to identify:

- Key discussion points
- Decisions
- Action items
- Responsible persons
- Deadlines
- Important dates
- Follow-up tasks

### Named Entity Recognition

NER may be used to identify:

- PERSON
- ORGANIZATION
- DATE
- TIME
- LOCATION

---

## 8. Final Meeting Minutes

The final output should follow a structure similar to:

Meeting Minutes

Meeting Title:
Date:
Participants:

### Executive Summary

...

### Key Discussion Points

1. ...
2. ...
3. ...

### Decisions

1. ...
2. ...

### Action Items

| Task | Responsible Person | Deadline |
|------|--------------------|----------|
| ... | ... | ... |

### Important Dates

...

### Next Steps

...

Information that is not available should be marked:

`Not specified`

The system must not invent information.

---

## 9. Model Development

The project should use a single integrated NLP pipeline/model approach.

The four team members are responsible for collecting 25 records each. They are NOT responsible for creating four separate models.

Possible development strategy:

1. Create an extractive baseline.
2. Evaluate the baseline.
3. Implement a pretrained transformer-based approach if feasible.
4. Implement information extraction.
5. Integrate the components.
6. Evaluate the final system.

Do not claim that a large language model was trained from scratch using only 100 records.

If a pretrained model is used, clearly document:

- Model name
- Model source
- Whether it is used for inference or fine-tuning
- Dataset usage
- Limitations

---

## 10. Evaluation

For summarization, use appropriate metrics such as:

- ROUGE-1
- ROUGE-2
- ROUGE-L

For information extraction, where reference annotations are available:

- Precision
- Recall
- F1-score

Also perform qualitative evaluation for:

- Relevance
- Coverage
- Faithfulness
- Readability
- Action-item correctness
- Hallucination

---

## 11. Expected Deliverables

The project should contain:

- 100-record dataset
- Dataset collection/scraping code
- Dataset validation code
- Preprocessing code
- EDA notebook
- NLP pipeline
- Summarization implementation
- Information extraction implementation
- Evaluation code
- Generated meeting minutes
- Error analysis
- Documentation
- README
- Final demonstration

---

## 12. Success Criteria

The project is considered complete when:

- Exactly 100 valid meeting records exist.
- 25 records have been collected by each team member.
- Duplicate records have been removed.
- Source URLs are preserved.
- Raw data is preserved.
- Processed data is generated.
- NLP processing works successfully.
- Summaries can be generated.
- Meeting information can be extracted.
- Structured meeting minutes can be generated.
- Evaluation results are available.
- The complete pipeline can be reproduced.