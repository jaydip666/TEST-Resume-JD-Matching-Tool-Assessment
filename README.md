# 🤖 E2M Solutions – AI Resume–JD Matching Tool

An AI-powered **Resume–Job Description Matching Tool** developed as part of the **E2M Solutions AI Intern Practical Assessment**.

This application analyzes a candidate's resume against a job description, extracts relevant skills, calculates an ATS-style match score, performs semantic similarity analysis, and generates an explainable hiring report using NLP techniques.

---

# ✨ Key Features

## 📄 Resume Analysis

- Upload Resume (.pdf, .docx, .txt)
- Automatic Resume Text Extraction
- Resume Preview
- Resume Skill Extraction

## 📋 Job Description Analysis

- Paste Job Description
- Upload Job Description (.pdf, .docx, .txt)
- Automatic JD Parsing
- Required Skill Detection

## 🤖 AI Matching

- ATS Match Score (0–100)
- Skill Overlap Analysis
- Semantic Similarity Score
- Matched Skills
- Missing Skills
- Narrative Explanation
- Resume Improvement Suggestions
- Highlighted Resume & JD Skills

## 🏆 Bonus Feature – Candidate Ranking

Upload **one Job Description** and **up to five resumes**.

The system automatically:

- Parses every resume
- Calculates ATS Match Score
- Compares all candidates
- Ranks candidates from best to worst
- Highlights the Top Candidate
- Displays a professional leaderboard
- Shows individual candidate analysis

---

# 🚀 Tech Stack

## Frontend

- Streamlit

## Backend

- Python 3.11+

## AI / NLP

- TF-IDF
- Cosine Similarity
- Regex-based Skill Extraction
- NLP-based Text Processing

## Libraries

- Streamlit
- pdfplumber
- python-docx

---

# ⚙️ Project Workflow

## Single Resume Analysis

```text
Upload Resume
      │
      ▼
Extract Resume Text
      │
      ▼
Upload / Paste Job Description
      │
      ▼
Extract Skills
      │
      ▼
Semantic Similarity
      │
      ▼
Calculate ATS Match Score
      │
      ▼
Generate AI Explanation
      │
      ▼
Display Results
```

## Candidate Ranking

```text
Upload One Job Description
            │
            ▼
Upload Up To 5 Resumes
            │
            ▼
Extract Resume Text
            │
            ▼
Analyze Every Resume
            │
            ▼
Calculate Individual Scores
            │
            ▼
Rank Candidates
            │
            ▼
Display Leaderboard
```

---

# 📊 Scoring Method

The overall score is calculated using:

| Component | Weight |
|-----------|--------|
| Skill Overlap | 70% |
| Semantic Similarity | 30% |

### Formula

```text
Final ATS Score

=

(0.70 × Skill Score)

+

(0.30 × Semantic Similarity)
```

---

# 🏆 Candidate Ranking

The Candidate Ranking module simulates a basic Applicant Tracking System (ATS).

### Leaderboard Includes

- 🥇 Candidate Rank
- 👤 Candidate Name
- 📊 Match Score
- 🎯 Skill Overlap
- 🤝 Semantic Similarity
- ✅ Hiring Recommendation
- 🔍 View Detailed Analysis

Hiring Recommendation:

- Strong Match
- Moderate Match
- Weak Match

---

# 📂 Project Structure

```text
Resume-JD-Matcher/

│── app.py
│── matcher.py
│── skills_data.py
│── requirements.txt
│── README.md
│── sample_resume.txt
│── sample_jd.txt
```

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/resume-jd-matching-tool.git
```

Go inside the project

```bash
cd resume-jd-matching-tool
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 📖 How To Use

## Single Resume Analysis

### Step 1

Upload a Resume

Supported formats:

- PDF
- DOCX
- TXT

### Step 2

Paste or Upload a Job Description.

### Step 3

Click **Analyze Match**.

### Step 4

View

- ATS Match Score
- Skill Overlap
- Semantic Similarity
- Matched Skills
- Missing Skills
- Narrative Explanation
- Resume Suggestions

---

## Candidate Ranking

### Step 1

Open the **Rank Candidates** tab.

### Step 2

Upload one Job Description.

### Step 3

Upload up to **5 resumes**.

### Step 4

Click **Rank Candidates**.

### Step 5

View

- Leaderboard
- Top Candidate
- ATS Match Score
- Hiring Recommendation
- Detailed Analysis

---

# 📈 Future Improvements

- OpenAI / Gemini Integration
- OCR Support for Scanned PDFs
- Resume Rewrite Suggestions
- Download PDF Report
- GitHub Profile Analysis
- LinkedIn Profile Import
- Job URL Parsing
- Multi-language Support

---

# 🎯 Assessment Coverage

✅ Resume Parsing

✅ Job Description Parsing

✅ Skill Extraction

✅ ATS Match Score

✅ Semantic Similarity

✅ Matched Skills

✅ Missing Skills

✅ Resume Improvement Suggestions

✅ Narrative Explanation

✅ Candidate Ranking

✅ Leaderboard

✅ Hiring Recommendation

✅ Individual Candidate Analysis

---

# 👨‍💻 Author - Jaydeep Gavare

Developed for the **E2M Solutions AI Intern Practical Assessment**.

---

# 📄 License

This project is intended for educational and assessment purposes only.
