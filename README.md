# Resume–JD Matching Tool (with AI-style Scoring)

A Streamlit app that compares a resume against a job description, extracts
relevant skills, and produces a match score with a full explanation —
matched skills, missing skills, and improvement suggestions.

## How it works

1. **Input** — paste text or upload a `.txt`, `.pdf`, or `.docx` file for
   both the resume and the job description.
2. **Skill extraction** — a curated taxonomy of ~70 technical and soft
   skills (`skills_data.py`) is matched against both documents using
   whole-word regex matching, so `Node.js`, `NodeJS`, and `node` all
   resolve to the same skill.
3. **Weighting** — for each skill found in the JD, the surrounding text is
   scanned for language like *"required"*, *"must have"* vs.
   *"preferred"*, *"nice to have"* to classify it as **must-have**
   (weight 2.0) or **nice-to-have** (weight 1.0).
4. **Scoring**:
   - **Skill Overlap Score** = (sum of weights of matched skills) / (sum of
     weights of all JD skills) × 100
   - **Semantic Similarity Score** = TF-IDF cosine similarity between the
     full resume and JD text × 100 (catches phrasing/synonyms the keyword
     matcher misses)
   - **Overall Score** = 0.7 × Skill Overlap + 0.3 × Semantic Similarity
5. **Explanation** — matched skills, missing must-have/nice-to-have
   skills, a narrative summary, and concrete suggestions for improving
   the resume against this specific JD.
6. **Highlighting** — both documents are rendered with matched skills
   highlighted in green and missing skills highlighted in red (JD only).

## Why this stack

Pure Python + `scikit-learn` (TF-IDF) means the tool runs **entirely
offline with no external LLM API key required**, while still using an
"AI/NLP-style" semantic similarity signal — a good fit for a fast,
dependency-light take-home assessment. If you do have access to an LLM
API, you can swap `compute_semantic_similarity()` in `matcher.py` for an
LLM call that judges semantic fit and returns a 0–100 score plus a
free-text rationale.

## Setup & running

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI |
| `matcher.py` | Text extraction, skill extraction, scoring, explanation logic |
| `skills_data.py` | Curated skills taxonomy + must-have/nice-to-have marker phrases |
| `sample_resume.txt`, `sample_jd.txt` | Sample inputs to try the app immediately |
| `requirements.txt` | Python dependencies |

## Possible extensions

- Swap the TF-IDF similarity for embeddings (e.g. `sentence-transformers`)
  or a real LLM call for richer semantic scoring.
- Expand `skills_data.py` or load a larger external skills taxonomy (e.g.
  ESCO/O*NET) for broader coverage.
- Add resume-side "must-have" detection (e.g., years of experience,
  degree requirements) beyond skill keywords.
- Persist results and allow batch-scoring multiple resumes against one JD.
