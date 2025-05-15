import os
import streamlit as st
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from app.resume_parser import extract_text
from sentence_transformers import SentenceTransformer, util
import requests

# Enhanced URL Text Extractor with Playwright
def extract_text_from_url(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)
        page.evaluate("() => { window.scrollBy(0, document.body.scrollHeight); }")
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")

    # Try to target specific container first
    target_div = soup.find('div', class_='job-description')
    if target_div:
        return target_div.get_text(separator="\n", strip=True)

    # Fallback to all visible text
    st.warning("⚠️ Specific job description container not found, showing all visible text.")
    text_elements = soup.find_all(text=True)
    visible_texts = filter(lambda e: e.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]'], text_elements)
    return "\n".join(t.strip() for t in visible_texts if t.strip())

# Keyword Matching Function
def find_missing_keywords(job_text, resume_text):
    job_words = set(job_text.lower().split())
    resume_words = set(resume_text.lower().split())
    return sorted([w for w in (job_words - resume_words) if len(w) > 3])

# LinkedIn Job Search Function
def fetch_linkedin_jobs(query):
    try:
        url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('div', class_='base-search-card__info')
        return [job.text.strip() for job in jobs[:10]]
    except Exception as e:
        st.error(f"Failed to fetch jobs: {e}")
        return []

# Streamlit Setup
st.set_page_config(page_title="AI Resume Scanner", layout="centered")
st.title("Cloud Resume Parser and Job Matcher System")
st.caption("Upload your resume and provide a job description file or link to compare")

st.write("🔄 Loading AI Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
st.success("✅ AI Model Loaded")

# User Inputs
resume_file = st.file_uploader("Upload your Resume", type=["pdf", "docx", "txt"])
job_file = st.file_uploader("Upload Job Description File (Optional)", type=["pdf", "docx", "txt"])
job_link = st.text_input("Or Paste Job Posting URL (Optional)")

if resume_file and (job_file or job_link):
    resume_path = f"temp_resume.{resume_file.name.split('.')[-1]}"
    with open(resume_path, "wb") as f:
        f.write(resume_file.read())
    resume_text = extract_text(resume_path)

    if job_file:
        job_path = f"temp_job.{job_file.name.split('.')[-1]}"
        with open(job_path, "wb") as f:
            f.write(job_file.read())
        job_text = extract_text(job_path)
    else:
        job_text = extract_text_from_url(job_link)

    if not job_text.strip():
        st.error("Could not extract meaningful text from the job description.")
    else:
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        job_embedding = model.encode(job_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(resume_embedding, job_embedding)[0][0].item()
        match_score = round(similarity * 100, 2)

        # Display Semantic Match Score with Meter
        st.markdown("### 🤖 Semantic Match Score")
        st.progress(match_score / 100)
        st.write(f"**Score: {match_score}%**")

        # Display Missing Keywords
        missing_keywords = find_missing_keywords(job_text, resume_text)
        st.markdown("### 🧩 Missing Keywords from Resume")
        if missing_keywords:
            st.write(", ".join(missing_keywords[:20]))
        else:
            st.success("No major keywords missing. Your resume looks great!")

        # Display LinkedIn Job Suggestions
        st.markdown("### 🧑‍💼 **LinkedIn Job Listings**")
        search_query = " ".join(missing_keywords[:5]) or "Data Scientist"
        jobs = fetch_linkedin_jobs(search_query)
        if jobs:
            for job in jobs:
                st.write(job)
        else:
            st.write("No jobs found or LinkedIn blocked the request.")
