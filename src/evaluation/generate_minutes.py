"""
generate_minutes.py  (v2)

Full end-to-end meeting-minutes generator.

Returns a dict with:
  - extractive_summary      (TF-IDF baseline — for evaluation/comparison)
  - abstractive_summary     (T5-synthesized — primary user-facing output)
  - validation              (ValidationResult)
  - action_items
  - persons
  - dates
  - topics
  - formatted_minutes       (human-readable text)
"""

import logging
import os
from typing import Dict

logger = logging.getLogger(__name__)


def run_pipeline(raw_transcript: str) -> Dict:
    """
    Run the complete pipeline on a single transcript.
    Returns a results dict.
    """
    from src.preprocessing.preprocessor import preprocess_transcript
    from src.summarization.summarizer import extractive_summarize, abstractive_summary
    from src.summarization.summary_validator import validate_summary
    from src.summarization.transcript_parser import parse_transcript
    from src.summarization.discussion_segmenter import segment_discussion
    from src.extraction.extractor import extract_action_items, extract_persons, extract_dates

    if not isinstance(raw_transcript, str) or not raw_transcript.strip():
        return _empty_result()

    # ── Preprocessing ─────────────────────────────────────────────────────────
    cleaned = preprocess_transcript(raw_transcript)

    # ── Extractive baseline ───────────────────────────────────────────────────
    ext_summary = extractive_summarize(cleaned, num_sentences=5)

    # ── Abstractive summary ───────────────────────────────────────────────────
    abs_summary = abstractive_summary(raw_transcript)

    # ── Validate ──────────────────────────────────────────────────────────────
    validation = validate_summary(abs_summary, raw_transcript)
    if not validation.passed:
        logger.warning(f"Summary failed validation (score={validation.score}). Issues: {validation.issues[:3]}")

    # ── Information extraction ────────────────────────────────────────────────
    action_items = extract_action_items(cleaned)
    persons      = extract_persons(cleaned)
    dates        = extract_dates(cleaned)

    # ── Topic list ────────────────────────────────────────────────────────────
    turns    = parse_transcript(raw_transcript)
    segments = segment_discussion(turns)
    topics   = [s['topic'] for s in segments]

    # ── Format final minutes text ──────────────────────────────────────────────
    formatted = _format_minutes(
        abs_summary=abs_summary,
        ext_summary=ext_summary,
        action_items=action_items,
        persons=persons,
        dates=dates,
        topics=topics,
        validation=validation,
    )

    return {
        "extractive_summary": ext_summary,
        "abstractive_summary": abs_summary,
        "validation": validation,
        "action_items": action_items,
        "persons": persons,
        "dates": dates,
        "topics": topics,
        "formatted_minutes": formatted,
    }


def _format_minutes(
    abs_summary, ext_summary, action_items,
    persons, dates, topics, validation
) -> str:
    lines = ["# MEETING MINUTES", ""]

    # Primary Executive Summary
    lines += ["## EXECUTIVE SUMMARY", abs_summary or "Not available.", ""]

    # Topics
    if topics:
        lines += ["## KEY DISCUSSION TOPICS"]
        for t in topics:
            lines.append(f"- {t}")
        lines.append("")

    # Persons
    if persons and persons != "Not specified":
        lines += ["## PARTICIPANTS / MENTIONED PERSONS", persons, ""]

    # Actions
    if action_items and action_items != "Not specified":
        lines += ["## ACTION ITEMS & DECISIONS", action_items, ""]

    # Dates
    if dates and dates != "Not specified":
        lines += ["## IMPORTANT DATES", dates, ""]

    # Baseline comparison (collapsible in UI, always present for evaluation)
    lines += [
        "---",
        "## BASELINE (TF-IDF Extractive Summary — for comparison only)",
        ext_summary or "Not available.",
        "",
    ]

    # Validation metadata
    lines += [
        "---",
        f"**Summary Quality Score**: {validation.score:.2f}  |  "
        f"**Validation**: {'✅ Passed' if validation.passed else '⚠️ Issues detected'}",
    ]
    if validation.issues:
        lines.append("**Issues**: " + "; ".join(validation.issues[:5]))

    return "\n".join(lines)


def _empty_result() -> Dict:
    from src.summarization.summary_validator import ValidationResult
    return {
        "extractive_summary": "",
        "abstractive_summary": "",
        "validation": ValidationResult(passed=False, issues=["Empty transcript"], score=0.0),
        "action_items": "Not specified",
        "persons": "Not specified",
        "dates": "Not specified",
        "topics": [],
        "formatted_minutes": "No transcript provided.",
    }
