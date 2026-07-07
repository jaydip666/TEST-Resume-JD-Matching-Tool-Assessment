"""
Core logic for the Resume-JD Matching Tool.

This module is UI-agnostic on purpose: app.py (Streamlit) imports the
functions below and only worries about layout/rendering.
"""

import re
import io
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills_data import SKILLS_TAXONOMY, MUST_HAVE_MARKERS, NICE_TO_HAVE_MARKERS

# --------------------------------------------------------------------------
# File / text extraction
# --------------------------------------------------------------------------

def extract_text_from_file(uploaded_file) -> str:
    """Extract raw text from an uploaded .txt, .pdf, or .docx file."""
    name = uploaded_file.name.lower()
    data = uploaded_file.read()

    if name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
        return "\n".join(text_parts)

    if name.endswith(".docx"):
        import docx
        doc = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)

    # Fallback: try decoding as plain text
    return data.decode("utf-8", errors="ignore")


# --------------------------------------------------------------------------
# Skill extraction
# --------------------------------------------------------------------------

def _find_skill_spans(text: str) -> Dict[str, List[Tuple[int, int]]]:
    """Return {canonical_skill: [(start, end), ...]} for every occurrence found in text."""
    text_lower = text.lower()
    found = {}
    for canonical, aliases in SKILLS_TAXONOMY.items():
        spans = []
        for alias in aliases:
            # Aliases may already be regex fragments (e.g. r"\bc\b"); otherwise
            # treat as a literal phrase with word boundaries.
            if alias.startswith(r"\b") or "\\" in alias:
                pattern = alias
            else:
                pattern = r"\b" + re.escape(alias) + r"\b"
            for m in re.finditer(pattern, text_lower):
                spans.append((m.start(), m.end()))
        if spans:
            found[canonical] = spans
    return found


def extract_skills(text: str) -> List[str]:
    """Simple presence-based skill extraction (used for the resume)."""
    return sorted(_find_skill_spans(text).keys())


def classify_jd_skill_weight(skill: str, jd_text: str) -> Tuple[str, float]:
    """
    Decide whether a JD skill is must-have / nice-to-have / neutral by
    looking at the words surrounding each occurrence of the skill.
    Returns (label, weight).
    """
    text_lower = jd_text.lower()
    spans = _find_skill_spans(jd_text).get(skill, [])
    if not spans:
        return ("neutral", 1.0)

    window = 60  # characters of context on each side
    context_snippets = []
    for start, end in spans:
        lo = max(0, start - window)
        hi = min(len(text_lower), end + window)
        context_snippets.append(text_lower[lo:hi])

    joined_context = " | ".join(context_snippets)

    is_must = any(marker in joined_context for marker in MUST_HAVE_MARKERS)
    is_nice = any(marker in joined_context for marker in NICE_TO_HAVE_MARKERS)

    if is_must and not is_nice:
        return ("must-have", 2.0)
    if is_nice and not is_must:
        return ("nice-to-have", 1.0)
    # Skills mentioned early in the JD (e.g., in a bullet list of core
    # requirements) are nudged toward must-have as a reasonable default.
    first_occurrence = spans[0][0]
    relative_position = first_occurrence / max(1, len(text_lower))
    if relative_position < 0.5:
        return ("must-have", 1.5)
    return ("nice-to-have", 1.0)


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------

@dataclass
class MatchResult:
    overall_score: float
    skill_score: float
    semantic_score: float
    matched_skills: List[Tuple[str, str, float]]      # (skill, weight_label, weight)
    missing_must_have: List[str]
    missing_nice_to_have: List[str]
    jd_skill_weights: Dict[str, Tuple[str, float]]
    resume_skills: List[str]
    suggestions: List[str] = field(default_factory=list)


def compute_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """TF-IDF cosine similarity between the two full documents, scaled 0-100."""
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform([resume_text, jd_text])
    except ValueError:
        # Happens if both texts contain only stop words / are empty after cleaning
        return 0.0
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(float(sim) * 100, 1)


def match_resume_to_jd(resume_text: str, jd_text: str) -> MatchResult:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    jd_skill_weights = {
        skill: classify_jd_skill_weight(skill, jd_text) for skill in jd_skills
    }

    resume_skill_set = set(resume_skills)

    matched = []
    missing_must, missing_nice = [], []

    total_weight = 0.0
    matched_weight = 0.0

    for skill, (label, weight) in jd_skill_weights.items():
        total_weight += weight
        if skill in resume_skill_set:
            matched.append((skill, label, weight))
            matched_weight += weight
        else:
            if label == "must-have":
                missing_must.append(skill)
            else:
                missing_nice.append(skill)

    skill_score = round((matched_weight / total_weight) * 100, 1) if total_weight > 0 else 0.0
    semantic_score = compute_semantic_similarity(resume_text, jd_text)

    # Blend: skill overlap is the primary signal, semantic similarity smooths
    # over synonyms / phrasing the keyword matcher can't catch.
    overall_score = round(0.7 * skill_score + 0.3 * semantic_score, 1)
    overall_score = max(0.0, min(100.0, overall_score))

    suggestions = _build_suggestions(missing_must, missing_nice, skill_score)

    return MatchResult(
        overall_score=overall_score,
        skill_score=skill_score,
        semantic_score=semantic_score,
        matched_skills=sorted(matched, key=lambda t: -t[2]),
        missing_must_have=sorted(missing_must),
        missing_nice_to_have=sorted(missing_nice),
        jd_skill_weights=jd_skill_weights,
        resume_skills=resume_skills,
        suggestions=suggestions,
    )


def _build_suggestions(missing_must: List[str], missing_nice: List[str], skill_score: float) -> List[str]:
    suggestions = []
    if missing_must:
        suggestions.append(
            "Add clear, specific evidence (projects, work experience, or certifications) for these "
            f"core requirements the JD emphasizes: {', '.join(missing_must)}."
        )
    if missing_nice:
        suggestions.append(
            f"Consider mentioning these preferred/nice-to-have skills if you have any exposure to them: "
            f"{', '.join(missing_nice)}."
        )
    if skill_score < 50:
        suggestions.append(
            "Overall skill overlap is low — tailor the resume's skills section and bullet points to "
            "mirror the exact terminology used in the job description."
        )
    elif skill_score < 80:
        suggestions.append(
            "Good partial match — quantify achievements (metrics, scale, impact) tied to the matched "
            "skills to strengthen the application further."
        )
    else:
        suggestions.append(
            "Strong match — focus the resume summary on the top must-have skills so they are visible "
            "at a glance."
        )
    if not suggestions:
        suggestions.append("No specific gaps detected.")
    return suggestions
