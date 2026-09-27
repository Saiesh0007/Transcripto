"""
discussion_segmenter.py
Groups parsed speaker turns into coherent discussion topics using
TF-IDF cosine similarity + a greedy boundary detector.

No hard-coded topics — topics are derived entirely from the transcript.
"""

import re
from typing import List, Dict, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _turn_text(turn: Dict) -> str:
    return turn.get('text', '')


def _window_similarity(tfidf_matrix, i: int, j: int) -> float:
    """Cosine similarity between two turn vectors."""
    return float(cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])[0][0])


def _derive_topic_label(turns: List[Dict], max_words: int = 8) -> str:
    """Generate a short topic label from the most TF-IDF-prominent terms in a segment."""
    texts = [_turn_text(t) for t in turns if _turn_text(t).strip()]
    if not texts:
        return "Discussion"
    try:
        vec = TfidfVectorizer(stop_words='english', max_features=max_words)
        vec.fit(texts)
        terms = vec.get_feature_names_out()
        return ', '.join(terms[:5]).title()
    except Exception:
        return "Discussion"


def _detect_question_answer_pairs(turns: List[Dict]) -> List[Dict]:
    """
    Mark turns that end with '?' as questions and the immediately
    following non-empty turn as a potential answer.
    Adds 'is_question' and 'answers_turn_index' fields.
    """
    q_pattern = re.compile(r'\?\s*$')
    for i, turn in enumerate(turns):
        turn['is_question'] = bool(q_pattern.search(turn['text']))
        turn['answered_by'] = None
        if turn['is_question']:
            # Find next turn from a different speaker
            for j in range(i + 1, min(i + 4, len(turns))):
                if turns[j]['speaker'] != turn['speaker'] and turns[j]['text'].strip():
                    turn['answered_by'] = j
                    break
    return turns


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────

def segment_discussion(
    turns: List[Dict],
    min_segment_turns: int = 15,
    similarity_threshold: float = 0.05,
) -> List[Dict]:
    """
    Group turns into topical segments.

    Returns a list of segment dicts:
        {
          "topic":   str,
          "turns":   List[Dict],
          "start":   int,   # turn_index of first turn
          "end":     int,   # turn_index of last turn
        }
    """
    turns = _detect_question_answer_pairs(turns)

    texts = [_turn_text(t) for t in turns]
    if len(texts) < 2:
        label = _derive_topic_label(turns)
        return [{"topic": label, "turns": turns, "start": 0, "end": len(turns) - 1}]

    try:
        vec = TfidfVectorizer(stop_words='english', min_df=1)
        matrix = vec.fit_transform(texts)
    except Exception:
        # Fallback: single segment
        label = _derive_topic_label(turns)
        return [{"topic": label, "turns": turns, "start": 0, "end": len(turns) - 1}]

    # Greedy segmentation: insert boundary when similarity drops below threshold
    boundaries = [0]
    window = 3
    for i in range(window, len(turns) - window):
        left_avg = np.mean([
            _window_similarity(matrix, i, j)
            for j in range(max(0, i - window), i)
        ])
        right_avg = np.mean([
            _window_similarity(matrix, i, j)
            for j in range(i + 1, min(len(turns), i + window + 1))
        ])
        if left_avg < similarity_threshold and right_avg > left_avg:
            boundaries.append(i)

    boundaries.append(len(turns))

    # Build segments; merge very small ones into the next
    segments = []
    for b in range(len(boundaries) - 1):
        seg_turns = turns[boundaries[b]:boundaries[b + 1]]
        if len(seg_turns) < min_segment_turns and segments:
            segments[-1]['turns'].extend(seg_turns)
            segments[-1]['end'] = seg_turns[-1]['turn_index'] if seg_turns else segments[-1]['end']
        else:
            label = _derive_topic_label(seg_turns)
            segments.append({
                "topic": label,
                "turns": seg_turns,
                "start": seg_turns[0]['turn_index'] if seg_turns else boundaries[b],
                "end":   seg_turns[-1]['turn_index'] if seg_turns else boundaries[b + 1] - 1,
            })

    # Refresh topic labels after merging
    for seg in segments:
        seg['topic'] = _derive_topic_label(seg['turns'])

    return segments


def segment_to_text(segment: Dict) -> str:
    """Convert a segment dict to a clean readable block for the model."""
    lines = []
    for t in segment['turns']:
        label = t['speaker']
        if t.get('role'):
            label += f" ({t['role']})"
        lines.append(f"{label}: {t['text']}")
    return '\n'.join(lines)
