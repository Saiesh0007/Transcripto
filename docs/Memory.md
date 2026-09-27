
---

# 4. `Memory.md`

```markdown
# AI Meeting Minutes Generator — Memory Specification

## 1. Purpose

"Memory" in this project means preserving important meeting context while processing a transcript.

The system must retain enough context to correctly connect discussions, decisions, action items, people, and deadlines.

---

# 2. Meeting Context

For every meeting, retain:

```text
meeting_id
title
date
participants
transcript
source_url
source_name
Where available:

agenda
organization
meeting type
reference summary
reference decisions
reference action items
3. Speaker Context

If speaker labels are available, preserve them.

Example:

John:
Sarah:
Mike:

If names are unavailable:

Speaker 1
Speaker 2
Speaker 3

should be preserved.

Never guess the identity of an anonymous speaker.

4. Conversation Context

Information must be interpreted using surrounding context.

Example:

John: We need to finish the testing.
Sarah: I can take care of it.

The system must determine the relationship using context rather than treating the word "it" independently.

If the relationship is uncertain, mark the extraction as uncertain.

5. Action-Item Memory

Each extracted action item should ideally retain:

Task
Responsible Person
Deadline
Supporting Context
Source Sentence
Confidence

Example:

Task:
Prepare testing report

Responsible:
Mike

Deadline:
Friday

Source:
"Mike, please prepare the testing report by Friday."

Confidence:
High
6. Decision Memory

For every extracted decision:

Decision
Supporting Sentence
Context
Confidence

A discussion or suggestion must not automatically be treated as a decision.

7. Deadline Memory

Meeting date should be preserved.

This is important for expressions such as:

tomorrow
next Friday
next week
by Monday

The system should preserve the original expression.

It may normalize relative dates only when enough context exists to determine the exact date.

8. Summary Memory

The final summary should preserve:

Major decisions
Action items
Deadlines
Important discussion points
Relevant supporting context

The summary must remain faithful to the transcript.

9. Source Traceability

Whenever possible, extracted information should maintain a link to the original sentence.

Example internal structure:

{
  "item": "Prepare testing report",
  "source_sentence_ids": [14, 15],
  "confidence": 0.91
}

This is useful for:

Debugging
Evaluation
Error analysis
Human verification
10. Confidence

If confidence scoring is implemented, use:

High
Medium
Low

Low-confidence information should be flagged rather than presented as a confirmed fact.

11. Missing Information

If information does not exist in the transcript:

Not specified

Do not generate a value.

Never invent:

Participant names
Deadlines
Decisions
Action items
Organizations
Dates
12. Long-Term Context

For long meetings:

Transcript
    ↓
Chunks
    ↓
Chunk-level analysis
    ↓
Combined context
    ↓
Final meeting minutes

Important information from all parts of the transcript should be considered.