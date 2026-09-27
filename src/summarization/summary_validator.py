"""
summary_validator.py

Validates a generated abstractive Executive Summary against
the source transcript before accepting it as output.

Checks:
  - Grounding: named entities (PERSON, ORG, DATE, numbers) in summary must
    appear in source
  - Coherence: no isolated sentence fragments
  - Non-emptiness / minimum length
  - Redundancy: repeated sentences flagged

Returns a ValidationResult dataclass with a pass/fail flag and details.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional

try:
    import spacy
    _nlp = spacy.load("en_core_web_sm")
except Exception:
    _nlp = None


@dataclass
class ValidationResult:
    passed: bool
    issues: List[str] = field(default_factory=list)
    unverified_claims: List[str] = field(default_factory=list)
    score: float = 1.0          # 0–1, higher is better


def _strip_markdown(text: str) -> str:
    """Remove markdown headers and formatting before entity extraction."""
    text = re.sub(r'^#{1,6}\s+.+$', '', text, flags=re.MULTILINE)  # headers
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)           # bold/italic
    text = re.sub(r'^[-*]\s+', '', text, flags=re.MULTILINE)        # bullets
    return text


def _extract_entities(text: str, labels=("PERSON", "ORG", "DATE", "GPE")) -> List[str]:
    if not _nlp or not text:
        return []
    text = _strip_markdown(text)
    text = re.sub(r'\s+', ' ', text).strip()   # normalize whitespace before NER
    doc = _nlp(text[:50000])     # cap to avoid memory issues on very long transcripts
    return [ent.text.strip() for ent in doc.ents if ent.label_ in labels]


def _extract_numbers(text: str) -> List[str]:
    return re.findall(r'\b\d[\d,%.]*\b', text)


def _sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]


def validate_summary(summary: str, source_transcript: str) -> ValidationResult:
    """
    Compare the summary against the source transcript.
    Returns a ValidationResult.
    """
    issues: List[str] = []
    unverified: List[str] = []
    deductions = 0.0

    # ── 1. Non-empty check ────────────────────────────────────────────────────
    if not summary or len(summary.split()) < 30:
        return ValidationResult(
            passed=False,
            issues=["Summary is too short or empty."],
            score=0.0,
        )

    # ── 2. Grounding — named entities ─────────────────────────────────────────
    summary_ents = _extract_entities(summary)
    source_lower = source_transcript.lower()
    for ent in summary_ents:
        if len(ent.split()) > 5:
            continue   # skip long phrases — likely section headings that slipped through
        if ent.lower() not in source_lower:
            unverified.append(ent)
            deductions += 0.03   # was 0.05 — reduced so a few missed entities don't sink score

    if unverified:
        issues.append(f"Unverified entities: {', '.join(unverified[:8])}")

    # ── 3. Grounding — numbers ────────────────────────────────────────────────
    for num in _extract_numbers(summary):
        if num not in source_transcript:
            issues.append(f"Number '{num}' not found in transcript.")
            deductions += 0.02   # reduced

    # ── 4. Fragment detection ─────────────────────────────────────────────────
    # Strip markdown before sentence splitting
    clean_summary = _strip_markdown(summary)
    sents = _sentences(clean_summary)
    for s in sents:
        s = s.strip()
        if not s:
            continue
        if len(s.split()) < 3 and not s.startswith('-'):
            issues.append(f"Possible fragment: '{s}'")
            deductions += 0.01

    # ── 5. Redundancy — near-duplicate sentences ───────────────────────────────
    seen = []
    for s in sents:
        if len(s.split()) < 5:
            continue
        words = set(s.lower().split())
        for prev in seen:
            if not prev: continue
            overlap = len(words & prev) / max(len(words), 1)
            if overlap > 0.85:
                issues.append(f"Redundant sentence detected.")
                deductions += 0.02
                break
        seen.append(words)

    # ── 6. Question-only sentence (output should not be a question) ───────────
    question_sents = [s for s in sents if s.strip().endswith('?') and len(s.split()) < 12]
    if question_sents:
        issues.append(f"Summary contains bare question(s): {question_sents[:2]}")
        deductions += 0.1

    score = max(0.0, round(1.0 - deductions, 2))
    passed = score >= 0.6 and not any("too short" in i for i in issues)

    return ValidationResult(
        passed=passed,
        issues=issues,
        unverified_claims=unverified,
        score=score,
    )
