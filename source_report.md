# Source Report

**Source:** QMSum (via Hugging Face Datasets `pszemraj/qmsum-cleaned`)
**URL:** https://huggingface.co/datasets/pszemraj/qmsum-cleaned
**Number of candidate records:** >100 records
**Transcript availability:** Yes (full transcripts available in `source_text`)
**Metadata availability:** Yes (reference summaries in `target_text`, topics)
**Accessibility:** Publicly accessible via Hugging Face without gating
**Restrictions:** Standard Hugging Face datasets terms of use.
**License/usage information:** CC BY 4.0
**Decision:** Selected
**Reason for selection:** Our initial choice (MeetingBank) turned out to be gated and required a login, which violates our rule against bypassing authentication. QMSum provides a large corpus of real-world meetings (academic, product, committee) with highly consistent structure, rich metadata, and reference summaries. This makes it ideal for training/evaluating summarization, extracting action items and decisions, and fulfilling the 100-record requirement.
