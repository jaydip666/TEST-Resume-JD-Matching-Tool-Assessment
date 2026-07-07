import html
import re
from io import BytesIO
from textwrap import wrap

import streamlit as st
from matcher import match_resume_to_jd, extract_text_from_file

st.set_page_config(
    page_title="Resume-JD Matching Tool",
    page_icon="🧩",
    layout="wide",
)

# --------------------------------------------------------------------------
# Styling helpers
# --------------------------------------------------------------------------

def score_color(score: float) -> str:
    if score >= 75:
        return "#1a9850"
    if score >= 50:
        return "#fdae61"
    return "#d73027"


def hiring_recommendation(score: float) -> str:
    if score >= 75:
        return "Strong Match"
    if score >= 50:
        return "Moderate Match"
    return "Weak Match"


def skill_overlap_text(result) -> str:
    matched = len(result.matched_skills)
    total = matched + len(result.missing_must_have) + len(result.missing_nice_to_have)
    return f"{matched}/{total} skills" if total else "0/0 skills"


def extract_candidate_name(resume_text: str, filename: str) -> str:
    """Infer a readable candidate name from resume text, falling back to the file name."""
    for line in resume_text.splitlines()[:12]:
        cleaned = re.sub(r"[^A-Za-z .'-]", " ", line).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        if not cleaned:
            continue
        words = cleaned.split()
        lower = cleaned.lower()
        if 2 <= len(words) <= 4 and not any(token in lower for token in ["resume", "curriculum", "email", "phone", "linkedin"]):
            return cleaned.title()

    stem = re.sub(r"\.[^.]+$", "", filename)
    stem = re.sub(r"[_\-]+", " ", stem).strip()
    return stem.title() or "Candidate"


def highlight_skills(text: str, skills: list, color: str, escape_text: bool = True) -> str:
    """Wrap each occurrence of the given skill names in a colored <mark> span."""
    from skills_data import SKILLS_TAXONOMY

    highlighted = html.escape(text) if escape_text else text
    for skill in skills:
        aliases = SKILLS_TAXONOMY.get(skill, [skill.lower()])
        for alias in aliases:
            if alias.startswith(r"\b") or "\\" in alias:
                pattern = alias
            else:
                pattern = r"\b" + re.escape(alias) + r"\b"
            highlighted = re.sub(
                pattern,
                lambda m: f'<mark style="background-color:{color}; padding:1px 3px; border-radius:3px;">{m.group(0)}</mark>',
                highlighted,
                flags=re.IGNORECASE,
            )
    return highlighted


def build_explanation(result) -> str:
    matched_names = [s for s, _, _ in result.matched_skills]
    explanation_lines = [
        f"The candidate's resume shows an overall match of {result.overall_score:.0f}/100 against this job description, "
        f"combining a {result.skill_score:.0f}/100 weighted skill-overlap score with a {result.semantic_score:.0f}/100 "
        f"overall semantic similarity score."
    ]
    if matched_names:
        explanation_lines.append(
            f"Strong alignment was found on: {', '.join(matched_names[:8])}"
            f"{'...' if len(matched_names) > 8 else ''}."
        )
    if result.missing_must_have:
        explanation_lines.append(
            "However, the resume does not clearly demonstrate the following core/must-have requirements: "
            f"{', '.join(result.missing_must_have)}. Addressing these would meaningfully improve the match."
        )
    if result.missing_nice_to_have:
        explanation_lines.append(
            "Additionally, some preferred nice-to-have skills were not found: "
            f"{', '.join(result.missing_nice_to_have)}."
        )
    return " ".join(explanation_lines)


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _pdf_text_line(x: int, y: int, text: str, size: int = 10, font: str = "F1") -> str:
    return f"BT /{font} {size} Tf {x} {y} Td ({_pdf_escape(text)}) Tj ET\n"


def create_ranking_pdf(candidates: list) -> bytes:
    """Create a compact PDF report using built-in PDF syntax to avoid extra dependencies."""
    width, height = 612, 792
    margin, line_height = 48, 16
    pages = []
    current_lines = []
    y = height - margin

    def add_line(text: str = "", size: int = 10, font: str = "F1"):
        nonlocal y, current_lines
        if y < margin:
            pages.append(current_lines)
            current_lines = []
            y = height - margin
        current_lines.append((margin, y, text, size, font))
        y -= line_height

    add_line("Resume-JD Candidate Ranking Report", 16, "F2")
    add_line("")
    for candidate in candidates:
        result = candidate["result"]
        add_line(
            f"#{candidate['rank']} {candidate['name']} - {result.overall_score:.0f}% - {hiring_recommendation(result.overall_score)}",
            12,
            "F2",
        )
        add_line(f"Skill Overlap: {skill_overlap_text(result)} | Semantic Similarity: {result.semantic_score:.0f}%")
        add_line(f"Matched Skills: {', '.join([s for s, _, _ in result.matched_skills]) or 'None detected'}")
        add_line(f"Missing Must-Have Skills: {', '.join(result.missing_must_have) or 'None'}")
        add_line(f"Missing Nice-to-Have Skills: {', '.join(result.missing_nice_to_have) or 'None'}")
        for wrapped in wrap(f"Explanation: {build_explanation(result)}", width=92):
            add_line(wrapped)
        add_line("Suggestions:", 10, "F2")
        for suggestion in result.suggestions:
            for wrapped in wrap(f"- {suggestion}", width=92):
                add_line(wrapped)
        add_line("")

    if current_lines:
        pages.append(current_lines)

    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [{kids}] /Count {count} >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    ]
    page_object_numbers = []
    content_object_numbers = []

    for page_lines in pages:
        content = ""
        for x, line_y, text, size, font in page_lines:
            content += _pdf_text_line(x, line_y, text[:115], size, font)
        content_bytes = content.encode("latin-1", errors="replace")
        content_object_numbers.append(len(objects) + 1)
        objects.append(f"<< /Length {len(content_bytes)} >>\nstream\n{content}endstream")
        page_object_numbers.append(len(objects) + 1)
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {content_object_numbers[-1]} 0 R >>"
        )

    objects[1] = objects[1].format(
        kids=" ".join(f"{number} 0 R" for number in page_object_numbers),
        count=len(page_object_numbers),
    )

    buffer = BytesIO()
    buffer.write(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(buffer.tell())
        buffer.write(f"{index} 0 obj\n{obj}\nendobj\n".encode("latin-1", errors="replace"))
    xref_offset = buffer.tell()
    buffer.write(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    buffer.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        buffer.write(f"{offset:010d} 00000 n \n".encode("latin-1"))
    buffer.write(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode("latin-1")
    )
    return buffer.getvalue()


def render_match_details(result, explanation: str):
    st.subheader("✅ Matched Skills")
    if result.matched_skills:
        for skill, label, weight in result.matched_skills:
            badge_color = "#1a9850" if label == "must-have" else "#4575b4"
            st.markdown(
                f'<span style="background-color:{badge_color}; color:white; padding:3px 10px; '
                f'border-radius:12px; margin:3px; display:inline-block; font-size:13px;">'
                f'{skill} · {label}</span>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No overlapping skills were detected.")

    st.write("")
    st.subheader("❌ Missing Skills")
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        st.markdown("**Must-have (high priority)**")
        if result.missing_must_have:
            for s in result.missing_must_have:
                st.markdown(f"- 🔴 {s}")
        else:
            st.success("None missing - all core requirements are covered!")
    with mcol2:
        st.markdown("**Nice-to-have**")
        if result.missing_nice_to_have:
            for s in result.missing_nice_to_have:
                st.markdown(f"- 🟡 {s}")
        else:
            st.success("None missing.")

    st.divider()
    st.subheader("📝 Narrative Explanation")
    st.markdown(explanation)

    st.write("")
    st.subheader("💡 Suggestions for Improvement")
    for s in result.suggestions:
        st.markdown(f"- {s}")


st.title("E2M Solutions - Resume-JD Matching Tool")
st.caption(
    "Upload or paste a resume and a job description to get an AI-assisted match score, "
    "a skill breakdown, and a narrative explanation."
)

st.divider()

single_tab, ranking_tab = st.tabs(["Single Resume Analysis", "Rank Candidates"])

with single_tab:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Resume")
        resume_input_mode = st.radio("Input method", ["Paste text", "Upload file"], key="resume_mode", horizontal=True)
        resume_text = ""
        if resume_input_mode == "Paste text":
            resume_text = st.text_area(
                "Paste resume text",
                height=300,
                key="resume_text_area",
                placeholder="Paste the candidate's resume here...",
            )
        else:
            resume_file = st.file_uploader(
                "Upload resume (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"], key="resume_file"
            )
            if resume_file is not None:
                resume_text = extract_text_from_file(resume_file)
                with st.expander("Preview extracted resume text"):
                    st.text(resume_text[:3000])

    with col2:
        st.subheader("📋 Job Description")
        jd_input_mode = st.radio("Input method", ["Paste text", "Upload file"], key="jd_mode", horizontal=True)
        jd_text = ""
        if jd_input_mode == "Paste text":
            jd_text = st.text_area(
                "Paste job description text",
                height=300,
                key="jd_text_area",
                placeholder="Paste the job description here...",
            )
        else:
            jd_file = st.file_uploader("Upload JD (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"], key="jd_file")
            if jd_file is not None:
                jd_text = extract_text_from_file(jd_file)
                with st.expander("Preview extracted JD text"):
                    st.text(jd_text[:3000])

    st.divider()

    run = st.button("🔍 Analyze Match", type="primary", use_container_width=True)

    if run:
        if not resume_text.strip() or not jd_text.strip():
            st.warning("Please provide both a resume and a job description before analyzing.")
        else:
            with st.spinner("Analyzing resume against job description..."):
                result = match_resume_to_jd(resume_text, jd_text)

            st.divider()
            st.header("Results")

            score_col, breakdown_col = st.columns([1, 2])

            with score_col:
                color = score_color(result.overall_score)
                st.markdown(
                    f"""
                    <div style="text-align:center; padding: 20px; border-radius: 12px; background-color: {color}20; border: 2px solid {color};">
                        <div style="font-size: 14px; color: gray;">OVERALL MATCH SCORE</div>
                        <div style="font-size: 56px; font-weight: 800; color: {color};">{result.overall_score:.0f}</div>
                        <div style="font-size: 14px; color: gray;">out of 100</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(min(1.0, result.overall_score / 100))

            with breakdown_col:
                st.markdown("**Score composition**")
                c1, c2 = st.columns(2)
                c1.metric("Skill Overlap Score", f"{result.skill_score:.0f}/100", help="Weighted overlap of must-have / nice-to-have skills")
                c2.metric("Semantic Similarity Score", f"{result.semantic_score:.0f}/100", help="TF-IDF cosine similarity of full text")
                st.caption("Overall score = 70% skill overlap + 30% semantic similarity")

            st.divider()
            render_match_details(result, build_explanation(result))

            st.divider()

            st.subheader("🔦 Highlighted Text")
            hcol1, hcol2 = st.columns(2)
            matched_only = [s for s, _, _ in result.matched_skills]
            missing_all = result.missing_must_have + result.missing_nice_to_have
            with hcol1:
                st.markdown("**Resume** (matched skills highlighted in green)")
                html_resume = highlight_skills(resume_text, matched_only, "#a6d96a")
                st.markdown(
                    f'<div style="max-height:400px; overflow-y:auto; padding:12px; border:1px solid #ddd; '
                    f'border-radius:8px; white-space:pre-wrap; font-size:13px;">{html_resume}</div>',
                    unsafe_allow_html=True,
                )
            with hcol2:
                st.markdown("**Job Description** (matched = green, missing = red)")
                html_jd = highlight_skills(jd_text, matched_only, "#a6d96a")
                html_jd = highlight_skills(html_jd, missing_all, "#fca6a6", escape_text=False)
                st.markdown(
                    f'<div style="max-height:400px; overflow-y:auto; padding:12px; border:1px solid #ddd; '
                    f'border-radius:8px; white-space:pre-wrap; font-size:13px;">{html_jd}</div>',
                    unsafe_allow_html=True,
                )

    else:
        st.info("Paste or upload a resume and job description above, then click **Analyze Match**.")

    st.divider()

with ranking_tab:
    st.header("Rank Candidates")
    st.caption("Upload one job description and up to five resumes to compare candidates using the same matching logic.")

    rank_col1, rank_col2 = st.columns([1, 1])
    with rank_col1:
        ranking_jd_file = st.file_uploader(
            "Upload one job description (.txt, .pdf, .docx)",
            type=["txt", "pdf", "docx"],
            key="ranking_jd_file",
        )
    with rank_col2:
        ranking_resume_files = st.file_uploader(
            "Upload up to 5 resumes (.txt, .pdf, .docx)",
            type=["txt", "pdf", "docx"],
            accept_multiple_files=True,
            key="ranking_resume_files",
        )

    if ranking_resume_files and len(ranking_resume_files) > 5:
        st.warning("Please upload no more than 5 resumes. Only the first 5 files will be analyzed.")
        ranking_resume_files = ranking_resume_files[:5]

    rank_run = st.button("🏆 Rank Candidates", type="primary", use_container_width=True)

    if "ranking_candidates" not in st.session_state:
        st.session_state.ranking_candidates = []
    if "selected_candidate" not in st.session_state:
        st.session_state.selected_candidate = None

    if rank_run:
        if ranking_jd_file is None or not ranking_resume_files:
            st.warning("Please upload one job description and at least one resume.")
        else:
            with st.spinner("Analyzing and ranking candidates..."):
                ranking_jd_text = extract_text_from_file(ranking_jd_file)
                candidates = []
                for resume_file in ranking_resume_files:
                    resume_body = extract_text_from_file(resume_file)
                    result = match_resume_to_jd(resume_body, ranking_jd_text)
                    candidates.append(
                        {
                            "name": extract_candidate_name(resume_body, resume_file.name),
                            "filename": resume_file.name,
                            "text": resume_body,
                            "result": result,
                            "explanation": build_explanation(result),
                        }
                    )

                candidates.sort(key=lambda candidate: candidate["result"].overall_score, reverse=True)
                for index, candidate in enumerate(candidates, start=1):
                    candidate["rank"] = index

                st.session_state.ranking_candidates = candidates
                st.session_state.selected_candidate = 0 if candidates else None

    candidates = st.session_state.ranking_candidates

    if candidates:
        st.divider()
        st.subheader("Leaderboard")

        top = candidates[0]
        top_color = score_color(top["result"].overall_score)
        st.markdown(
            f"""
            <div style="padding:16px; border-radius:12px; background-color:{top_color}18; border:2px solid {top_color}; margin-bottom:16px;">
                <div style="font-size:13px; color:gray; font-weight:700;">TOP CANDIDATE</div>
                <div style="font-size:26px; font-weight:800;">🏆 {html.escape(top["name"])} · {top["result"].overall_score:.0f}%</div>
                <div style="color:gray;">{hiring_recommendation(top["result"].overall_score)} · {skill_overlap_text(top["result"])} · Semantic Similarity {top["result"].semantic_score:.0f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        header = st.columns([0.55, 2.2, 1.15, 1.25, 1.4, 1.7, 1.0])
        header[0].markdown("**Rank**")
        header[1].markdown("**Candidate Name**")
        header[2].markdown("**Match Score (%)**")
        header[3].markdown("**Skill Overlap**")
        header[4].markdown("**Semantic Similarity**")
        header[5].markdown("**Hiring Recommendation**")
        header[6].markdown("**Details**")

        for index, candidate in enumerate(candidates):
            result = candidate["result"]
            row = st.columns([0.55, 2.2, 1.15, 1.25, 1.4, 1.7, 1.0])
            row[0].markdown(f"**#{candidate['rank']}**")
            badge = " 🏆" if candidate["rank"] == 1 else ""
            row[1].markdown(f"**{candidate['name']}{badge}**")
            row[2].markdown(f"<span style='color:{score_color(result.overall_score)}; font-weight:800;'>{result.overall_score:.0f}%</span>", unsafe_allow_html=True)
            row[3].markdown(skill_overlap_text(result))
            row[4].markdown(f"{result.semantic_score:.0f}%")
            row[5].markdown(hiring_recommendation(result.overall_score))
            if row[6].button("View Details", key=f"details_{index}", use_container_width=True):
                st.session_state.selected_candidate = index

        st.download_button(
            "Download Ranking Report (PDF)",
            data=create_ranking_pdf(candidates),
            file_name="candidate_ranking_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        selected_index = st.session_state.selected_candidate
        if selected_index is not None and 0 <= selected_index < len(candidates):
            selected = candidates[selected_index]
            st.divider()
            st.header(f"Candidate Details: {selected['name']}")
            st.caption(f"Source file: {selected['filename']}")
            render_match_details(selected["result"], selected["explanation"])

    else:
        st.info("Upload one job description and up to five resumes, then click **Rank Candidates**.")