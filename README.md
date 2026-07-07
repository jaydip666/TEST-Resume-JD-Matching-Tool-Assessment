# 🤖 E2M Solutions – AI Resume–JD Matching Tool

An AI-powered Resume–Job Description Matching Tool developed as part of the **E2M Solutions AI Intern Practical Assessment**.

The application analyzes a candidate's resume against a job description, extracts relevant skills, calculates an ATS-style match score, and generates an explainable hiring report using NLP techniques and semantic similarity. Similar resume-matching tools commonly combine text parsing, NLP, and semantic scoring for recruiter-friendly insights. :contentReference[oaicite:0]{index=0}
---

# 📌 Features

- 📄 Upload Resume (.pdf, .docx, .txt)
- 📝 Paste or Upload Job Description
- 🧠 Automatic Resume Text Extraction
- 🔍 Skill Extraction using NLP
- 📊 ATS Match Score (0–100)
- 📈 Skill Overlap Analysis
- 🤝 Semantic Similarity Score
- ✅ Matched Skills
- ❌ Missing Skills
- 💡 Resume Improvement Suggestions
- 📝 AI-style Narrative Explanation
- 🎨 Highlighted Resume & JD Skills
- 🏆 Candidate Ranking (Upload up to 5 resumes and rank candidates)

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

```text
Upload Resume
        │
        ▼
Extract Resume Text
        │
        ▼
Upload/Paste Job Description
        │
        ▼
Extract Skills
        │
        ▼
Semantic Similarity
        │
        ▼
Calculate ATS Score
        │
        ▼
Generate Explanation
        │
        ▼
Display Results
```

---

# 📊 Scoring Method

The final score is calculated using:

| Component | Weight |
|-----------|--------|
| Skill Overlap | 70% |
| Semantic Similarity | 30% |

Final Score

```
ATS Score =
(0.70 × Skill Score)
+
(0.30 × Semantic Similarity)
```

---

# 📂 Project Structure

```
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
git clone https://github.com/yourusername/resume-jd-matching-tool.git
```

Go inside project

```bash
cd resume-jd-matching-tool
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run app.py
```

---

# 📖 How to Use

### Step 1

Upload your Resume

Supported formats

- PDF
- TXT

### Step 2

Paste or Upload the Job Description.

### Step 3

Click **Analyze Match**.

### Step 4

View

- ATS Match Score
- Skill Overlap
- Semantic Similarity
- Matched Skills
- Missing Skills
- Suggestions
- Narrative Explanation

### Step 5 (Bonus)

Upload up to **5 resumes** to compare candidates and generate a ranked leaderboard.

---

# 📷 Screenshots

- Home Page
- Resume Upload
- Results Dashboard
- Candidate Ranking
- Match Analysis

---

# 📈 Future Improvements

- OpenAI/Gemini Integration
- Resume Section Detection
- OCR Support for Scanned PDFs
- GitHub Profile Analysis
- LinkedIn Profile Import
- Job URL Parsing
- Download PDF Report
- Resume Rewrite Suggestions
- Multi-language Support

---

# 🎯 Assessment Coverage

✔ Resume Parsing

✔ Job Description Parsing

✔ Skill Extraction

✔ ATS Match Score

✔ Semantic Similarity

✔ Matched Skills

✔ Missing Skills

✔ Narrative Explanation

✔ Resume Suggestions

✔ Candidate Ranking (Bonus)

---

# 👨‍💻 Author

Developed as part of the **E2M Solutions AI Intern Practical Assessment**.

---

# 📄 License

This project is intended for educational and assessment purposes only.
