"""
summarizer.py

Provides both summarisation strategies:

  extractive_summary(text, num_sentences)
      Original TF-IDF baseline. Retained for comparison/evaluation.

  abstractive_summary(raw_transcript)
      New production pipeline:
        1. Parse speaker turns
        2. Segment into discussion topics
        3. Summarise each chunk with T5 (t5-base)
        4. Merge chunk summaries
        5. Final synthesis pass
        6. Return structured Executive Summary

Long transcripts are handled via hierarchical chunking.
The model is loaded lazily and cached after the first call.
"""

import logging
import re
from typing import List

import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)

# ─── lazy model cache ────────────────────────────────────────────────────────
_MODEL = None
_TOKENIZER = None
_MODEL_NAME = "t5-base"
_MAX_INPUT_TOKENS = 450   # safe margin under T5's 512 token limit
_MAX_SUMMARY_TOKENS = 200
_MIN_SUMMARY_TOKENS = 60


def _get_model_and_tokenizer():
    global _MODEL, _TOKENIZER
    if _MODEL is None or _TOKENIZER is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        logger.info(f"Loading summarisation model: {_MODEL_NAME} ...")
        _TOKENIZER = AutoTokenizer.from_pretrained(_MODEL_NAME)
        _MODEL = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_NAME)
        _MODEL.eval()
        logger.info("Model loaded.")
    return _MODEL, _TOKENIZER


# ─── word-level token estimator (no tokenizer required) ─────────────────────
def _approx_tokens(text: str) -> int:
    """Rough estimate: 1 token ≈ 0.75 words."""
    return int(len(text.split()) * 1.33)


# ─────────────────────────────────────────────────────────────────────────────
# 1. EXTRACTIVE BASELINE (unchanged TF-IDF)
# ─────────────────────────────────────────────────────────────────────────────

def extractive_summarize(text: str, num_sentences: int = 5) -> str:
    """Original TF-IDF extractive baseline. Preserved for comparison."""
    if not isinstance(text, str) or not text.strip():
        return ""
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        matrix = vectorizer.fit_transform(sentences)
        scores = np.array(matrix.sum(axis=1)).flatten()
        top_idx = sorted(scores.argsort()[-num_sentences:][::-1])
        return " ".join(sentences[i] for i in top_idx)
    except Exception as e:
        logger.error(f"extractive_summarize error: {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# 2. ABSTRACTIVE PIPELINE (new production path)
# ─────────────────────────────────────────────────────────────────────────────

def _summarise_chunk(model, tokenizer, text: str) -> str:
    """Run T5 on a single chunk of text using model.generate()."""
    import torch
    text = text.strip()
    if not text or len(text.split()) < 10:
        return text   # too short to summarise meaningfully
        
    # T5 requires the task prefix
    text = "summarize: " + text
    
    word_count = len(text.split())
    # Max output is 1/3 of input length, capped at 200. No forced minimum —
    # T5 hallucinates padding when min_length exceeds actual content.
    max_out = min(200, max(40, word_count // 3))
    try:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            max_length=512,
            truncation=True,
        )
        input_len = inputs["input_ids"].shape[-1]
        abs_max = min(input_len + max_out, 512)
        with torch.no_grad():
            ids = model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=abs_max,
                num_beams=4,
                length_penalty=1.0,
                early_stopping=True,
                no_repeat_ngram_size=3,
            )
        return tokenizer.decode(ids[0], skip_special_tokens=True).strip()
    except Exception as e:
        logger.error(f"T5 chunk error: {e}")
        return ""


def _split_into_chunks(text: str, max_tokens: int = _MAX_INPUT_TOKENS) -> List[str]:
    """
    Split text into chunks that stay within max_tokens.
    Splits on sentence boundaries where possible.
    """
    sentences = sent_tokenize(text)
    chunks, current, current_tokens = [], [], 0
    for sent in sentences:
        t = _approx_tokens(sent)
        if current_tokens + t > max_tokens and current:
            chunks.append(" ".join(current))
            current, current_tokens = [], 0
        current.append(sent)
        current_tokens += t
    if current:
        chunks.append(" ".join(current))
    return chunks


def _format_section(title: str, content: str) -> str:
    if not content.strip():
        return ""
    return f"### {title}\n{content.strip()}\n"


def abstractive_summary(
    raw_transcript: str,
    extractive_fallback_sentences: int = 6,
) -> str:
    """
    Full abstractive pipeline.
    Returns a structured Executive Summary string.
    Falls back gracefully if T5 is unavailable.
    """
    from src.summarization.transcript_parser import parse_transcript, turns_to_text
    from src.summarization.discussion_segmenter import segment_discussion, segment_to_text
    from src.extraction.extractor import extract_action_items, extract_persons, extract_dates

    try:
        model, tokenizer = _get_model_and_tokenizer()
    except Exception as e:
        logger.warning(f"Could not load T5 — using enhanced extractive fallback. ({e})")
        return _enhanced_extractive_fallback(raw_transcript, extractive_fallback_sentences)

    # ── Step 0: clean transcript before any parsing ──────────────────────────
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    try:
        from src.preprocessing.preprocessor import preprocess_transcript
        cleaned_for_parsing = preprocess_transcript(raw_transcript)
    except Exception:
        cleaned_for_parsing = raw_transcript

    # ── Step 1: parse turns ──────────────────────────────────────────────────
    turns = parse_transcript(cleaned_for_parsing)
    if not turns:
        return _enhanced_extractive_fallback(raw_transcript, extractive_fallback_sentences)

    # ── Step 2: segment into topics ──────────────────────────────────────────
    segments = segment_discussion(turns)

    # ── Step 3: summarise each segment ───────────────────────────────────────
    segment_summaries: List[str] = []
    topics: List[str] = []
    for seg_idx, seg in enumerate(segments):
        seg_text = segment_to_text(seg)
        chunks = _split_into_chunks(seg_text)
        chunk_sums = []
        for c_idx, c in enumerate(chunks):
            if c.strip():
                logger.info(f"Summarising segment {seg_idx+1}/{len(segments)}, chunk {c_idx+1}/{len(chunks)}...")
                chunk_sums.append(_summarise_chunk(model, tokenizer, c))
                
        merged = " ".join(s for s in chunk_sums if s)
        if merged:
            # Second pass if merged chunk sums are still long
            if _approx_tokens(merged) > _MAX_INPUT_TOKENS:
                logger.info(f"Running second pass synthesis for segment {seg_idx+1}...")
                merged = _summarise_chunk(model, tokenizer, merged)
            segment_summaries.append(merged)
            topics.append(seg['topic'])

    if not segment_summaries:
        return _enhanced_extractive_fallback(raw_transcript, extractive_fallback_sentences)

    # ── Step 4: final synthesis ───────────────────────────────────────────────
    combined = " ".join(segment_summaries)
    if _approx_tokens(combined) > _MAX_INPUT_TOKENS:
        final_summary = _summarise_chunk(model, tokenizer, combined)
    else:
        final_summary = combined

    # ── Step 5: extract structured information ────────────────────────────────
    clean_text = turns_to_text(turns)
    action_items = extract_action_items(clean_text)
    persons      = extract_persons(clean_text)
    dates        = extract_dates(clean_text)

    # ── Step 6: build structured output ──────────────────────────────────────
    sections = []

    # Overall summary
    if final_summary:
        sections.append(_format_section("Overall Summary", final_summary))

    # Key Discussion Points (per topic)
    if topics and segment_summaries and len(topics) > 1:
        bullet_points = "\n".join(
            f"- **{topic}**: {summary}"
            for topic, summary in zip(topics, segment_summaries)
            if summary.strip()
        )
        sections.append(_format_section("Key Discussion Points", bullet_points))

    # Responsible persons
    if persons and persons != "Not specified":
        sections.append(_format_section("Participants / Mentioned Persons", persons))

    # Decisions & Actions
    if action_items and action_items != "Not specified":
        sections.append(_format_section("Actions and Commitments", action_items))

    # Dates
    if dates and dates != "Not specified":
        sections.append(_format_section("Important Dates", dates))

    return "\n".join(s for s in sections if s)


# ─────────────────────────────────────────────────────────────────────────────
# 3. ENHANCED EXTRACTIVE FALLBACK
# ─────────────────────────────────────────────────────────────────────────────

def _enhanced_extractive_fallback(raw: str, n: int) -> str:
    """
    A better extractive fallback than the raw TF-IDF baseline:
    - Parses speaker turns
    - Groups into segments
    - Picks the top-scoring sentence from each segment
    - Returns paragraph-style prose (not a list of fragments)
    """
    from src.summarization.transcript_parser import parse_transcript, turns_to_text
    from src.summarization.discussion_segmenter import segment_discussion, segment_to_text

    turns = parse_transcript(raw)
    if not turns:
        return extractive_summarize(raw, n)

    segments = segment_discussion(turns)
    selected = []
    for seg in segments:
        seg_text = segment_to_text(seg)
        sentences = sent_tokenize(seg_text)
        # Filter out very short / question-only sentences
        candidates = [s for s in sentences if len(s.split()) > 8 and not s.strip().endswith('?')]
        if not candidates:
            candidates = sentences
        if candidates:
            try:
                vec = TfidfVectorizer(stop_words='english')
                mat = vec.fit_transform(candidates)
                scores = np.array(mat.sum(axis=1)).flatten()
                best = candidates[int(scores.argmax())]
                selected.append(best.strip())
            except Exception:
                selected.append(candidates[0].strip())

    if not selected:
        return extractive_summarize(raw, n)

    prose = " ".join(selected[:n])
    return f"[Fallback Summary]\n{prose}"
