"""
Quick smoke-test for the new summarization pipeline.
Run from the repo root with:
    .\\venv\\Scripts\\activate
    python test_pipeline.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

SAMPLE = """
Project Manager: Okay, so let's start. We need to finish the remote control design by end of month.
Industrial Designer: I think we should go with rubber casing. It's more durable and cheaper.
Marketing: Our research shows customers prefer a premium look. Metal or hard plastic might be better.
User Interface: What about the number of buttons? We have 12 right now.
Project Manager: That's too many. We decided last time to keep it under eight.
Industrial Designer: Right. I'll redesign the layout and send it over by Thursday.
Marketing: Can we also consider adding a scroll wheel? Users asked for it in surveys.
Project Manager: Good point. Let's vote. All in favour?
Industrial Designer: Yes.
User Interface: Yes.
Marketing: Yes.
Project Manager: Agreed. Scroll wheel is in. Sarah will draft the updated spec by Friday.
Industrial Designer: I'll take care of the button reduction.
Project Manager: Great. So to summarise: rubber casing chosen, buttons reduced to eight, scroll wheel added. Next meeting is Monday at 10am.
"""

print("=" * 60)
print("TRANSCRIPT PARSER")
print("=" * 60)
from src.summarization.transcript_parser import parse_transcript, speakers_summary
turns = parse_transcript(SAMPLE)
print(f"Turns detected: {len(turns)}")
print("Speakers:", speakers_summary(turns))

print()
print("=" * 60)
print("DISCUSSION SEGMENTER")
print("=" * 60)
from src.summarization.discussion_segmenter import segment_discussion
segments = segment_discussion(turns)
print(f"Segments: {len(segments)}")
for s in segments:
    print(f"  Topic: {s['topic']}  |  Turns: {len(s['turns'])}")

print()
print("=" * 60)
print("EXTRACTIVE SUMMARY (TF-IDF Baseline)")
print("=" * 60)
from src.preprocessing.preprocessor import preprocess_transcript
from src.summarization.summarizer import extractive_summarize
cleaned = preprocess_transcript(SAMPLE)
ext = extractive_summarize(cleaned)
print(ext)

print()
print("=" * 60)
print("SUMMARY VALIDATOR (on sample text)")
print("=" * 60)
from src.summarization.summary_validator import validate_summary
vr = validate_summary(ext, SAMPLE)
print(f"Passed: {vr.passed}  |  Score: {vr.score}")
if vr.issues:
    for i in vr.issues:
        print(f"  Issue: {i}")

print()
print("=" * 60)
print("GENERATE_MINUTES PIPELINE (abstractive will download T5 on first run)")
print("=" * 60)
from src.evaluation.generate_minutes import run_pipeline
result = run_pipeline(SAMPLE)
print("Topics:", result["topics"])
print("Action items:", result["action_items"])
print("Persons:", result["persons"])
print("Dates:", result["dates"])
print()
print("--- ABSTRACTIVE SUMMARY ---")
print(result["abstractive_summary"])
print()
print(f"Quality score: {result['validation'].score}")
print("DONE.")
