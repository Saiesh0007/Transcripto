"""
transcript_parser.py
Parses raw meeting transcripts into structured speaker turns.

Each turn is represented as:
  {"speaker": str, "role": str | None, "text": str, "turn_index": int}

Supports common dialogue formats:
  - "Speaker Name: text"
  - "Speaker Name (Role): text"
  - AMI/ICSI speaker tags like "PM:", "ME:", "UI:"
  - Generic turn detection when no speaker labels exist
"""

import re
from typing import List, Dict, Optional


# ─────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────

# Pattern: "Speaker Name (optional role): rest of utterance"
_SPEAKER_LINE = re.compile(
    r'^(?P<speaker>[A-Z][A-Za-z .\'/-]{0,40}?)'
    r'(?:\s*\((?P<role>[^)]{1,60})\))?'
    r'\s*:\s*(?P<text>.+)',
    re.MULTILINE
)

# AMI-style abbreviated tags: "PM:", "ME:", "UI:", "ID:"
_ABBREV_TAG = re.compile(
    r'^(?P<speaker>[A-Z]{2,4})\s*:\s*(?P<text>.+)',
    re.MULTILINE
)

# Transcription disfluencies to strip from turn text
_DISFLUENCY = re.compile(r'\{[^}]+\}')  # e.g. {vocalsound}, {disfmarker}
_REPEATED_PUNCT = re.compile(r'([.!?,])\1+')


def _clean_turn_text(text: str) -> str:
    text = _DISFLUENCY.sub('', text)
    text = _REPEATED_PUNCT.sub(r'\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _detect_format(raw: str) -> str:
    """Return 'named', 'abbrev', or 'plain'."""
    named_hits = len(_SPEAKER_LINE.findall(raw))
    abbrev_hits = len(_ABBREV_TAG.findall(raw))
    if named_hits > 3:
        return 'named'
    if abbrev_hits > 3:
        return 'abbrev'
    return 'plain'


def _parse_named(raw: str) -> List[Dict]:
    turns = []
    for i, m in enumerate(_SPEAKER_LINE.finditer(raw)):
        text = _clean_turn_text(m.group('text'))
        if not text:
            continue
        turns.append({
            'speaker': m.group('speaker').strip(),
            'role': (m.group('role') or '').strip() or None,
            'text': text,
            'turn_index': i,
        })
    return turns


def _parse_abbrev(raw: str) -> List[Dict]:
    turns = []
    for i, m in enumerate(_ABBREV_TAG.finditer(raw)):
        text = _clean_turn_text(m.group('text'))
        if not text:
            continue
        turns.append({
            'speaker': m.group('speaker').strip(),
            'role': None,
            'text': text,
            'turn_index': i,
        })
    return turns


def _parse_plain(raw: str) -> List[Dict]:
    """Split into paragraph-level pseudo-turns when no speaker labels exist."""
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', raw) if p.strip()]
    return [
        {'speaker': 'Unknown', 'role': None, 'text': _clean_turn_text(p), 'turn_index': i}
        for i, p in enumerate(paragraphs)
        if _clean_turn_text(p)
    ]


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────

def parse_transcript(raw: str) -> List[Dict]:
    """
    Parse a raw transcript string into a list of speaker turns.

    Returns a list of dicts:
        {speaker, role, text, turn_index}
    """
    fmt = _detect_format(raw)
    if fmt == 'named':
        turns = _parse_named(raw)
    elif fmt == 'abbrev':
        turns = _parse_abbrev(raw)
    else:
        turns = _parse_plain(raw)
    return turns


def speakers_summary(turns: List[Dict]) -> Dict[str, int]:
    """Return {speaker: turn_count} for quick inspection."""
    counts: Dict[str, int] = {}
    for t in turns:
        counts[t['speaker']] = counts.get(t['speaker'], 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def turns_to_text(turns: List[Dict]) -> str:
    """Reconstruct a clean readable representation from parsed turns."""
    lines = []
    for t in turns:
        label = t['speaker']
        if t.get('role'):
            label += f" ({t['role']})"
        lines.append(f"{label}: {t['text']}")
    return '\n'.join(lines)
