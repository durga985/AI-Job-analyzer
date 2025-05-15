import os
import requests
from bs4 import BeautifulSoup
from app.resume_parser import extract_text
from app.job_parser import extract_job_description
from sentence_transformers import SentenceTransformer, util
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Utility to extract text from a URL
def extract_text_from_url(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        # Scroll to load dynamic content
        page.evaluate("() => { window.scrollBy(0, document.body.scrollHeight); }")
        page.wait_for_timeout(3000)

        content = page.content()
        browser.close()

    # Parse page content
    soup = BeautifulSoup(content, "html.parser")

    # Example: Target div with specific class, adjust based on your target page structure
    target_div = soup.find('div', class_='job-description')
    if target_div:
        return target_div.get_text(separator="\n", strip=True)

    # Fallback: extract all visible text if target not found
    print("⚠️ Specific job description container not found, falling back to all visible text.")
    text_elements = soup.find_all(text=True)
    def is_visible(element):
        return element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']
    visible_texts = filter(is_visible, text_elements)
    return "\n".join(t.strip() for t in visible_texts if t.strip())

# Function to find missing keywords
def find_missing_keywords(job_text, resume_text):
    job_keywords = set(job_text.lower().split())
    resume_keywords = set(resume_text.lower().split())
    missing = job_keywords - resume_keywords
    missing_filtered = [word for word in missing if len(word) > 3]
    return sorted(missing_filtered)

# Get resume file input
resume_path = input("Enter the path to your resume (pdf, docx, or txt): ").strip()
if not os.path.exists(resume_path):
    print(f"Error: File '{resume_path}' not found.")
    exit(1)

# Extract resume text
resume_text = extract_text(resume_path)
print("\n--- RESUME TEXT (Preview) ---\n")
print(resume_text[:500])

# Get job description input method
job_input_choice = input("\nDo you want to provide (1) a file or (2) a URL for the job description? Enter 1 or 2: ").strip()

job_text = ""
if job_input_choice == "1":
    job_path = input("Enter the path to the job description file (txt, docx, or pdf): ").strip()
    if not os.path.exists(job_path):
        print(f"Error: File '{job_path}' not found.")
        exit(1)
    job_text = extract_job_description(job_path)
elif job_input_choice == "2":
    job_url = input("Enter the job posting URL: ").strip()
    job_text = extract_text_from_url(job_url)
else:
    print("Invalid choice. Please enter 1 or 2.")
    exit(1)

if not job_text.strip():
    print("Error: Failed to extract text from the provided job description source.")
    exit(1)

print("\n--- JOB DESCRIPTION TEXT (Preview) ---\n")
print(job_text[:500])

# Load Sentence-BERT model
print("\nLoading AI Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ AI Model Loaded")

def display_accuracy_meter(score, width=20):
    """
    Displays a console-based accuracy meter for the given score.
    :param score: Percentage score (0 to 100)
    :param width: Width of the meter in characters
    """
    filled_length = int(width * score // 100)
    bar = '█' * filled_length + '-' * (width - filled_length)
    print(f"[{bar}] {score}%")
    
# Encode both texts
resume_embedding = model.encode(resume_text, convert_to_tensor=True)
job_embedding = model.encode(job_text, convert_to_tensor=True)

# Compute similarity
similarity = util.pytorch_cos_sim(resume_embedding, job_embedding)[0][0].item()
match_score = round(similarity * 100, 2)

print(f"\n🤖 Semantic Match Score: {match_score}%")
display_accuracy_meter(match_score)

# Find and display missing keywords
missing_keywords = find_missing_keywords(job_text, resume_text)
print("\n🧩 Missing Keywords from Resume:")
print(", ".join(missing_keywords[:15]) or "No major keywords missing.")