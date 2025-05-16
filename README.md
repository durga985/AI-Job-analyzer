# AI Job Analyzer – Resume Screening & Live Job Matching on AWS

AI Job Analyzer is a cloud-native, AI-powered resume screening and job matching platform. It intelligently compares user-uploaded resumes against job descriptions using Sentence-BERT and Natural Language Processing (NLP), scoring the semantic similarity.
Additionally, it scrapes live job listings from LinkedIn based on the parsed skills or job role, providing actionable job recommendations.

This project is fully deployable on AWS with Terraform and scalable using Application Load Balancer (ALB).

## 🎯 Problem Statement

Traditional HR systems require manual resume screening, which is time-consuming and error-prone. Job seekers also face challenges in tailoring resumes to specific job descriptions and identifying relevant open positions. This project solves these problems by:

- Automating semantic resume-job matching.

- Identifying missing keywords for better alignment.

- Providing real-time job search powered by LinkedIn scraping.

- Offering cloud-deployment with auto-scaling via AWS services.

## 🔍 Key Features

- Streamlit UI: For interactive resume upload and scoring.

- Sentence-BERT Model: For semantic similarity calculation.

- LinkedIn Scraper: For fetching real-time job listings.

- Playwright & BeautifulSoup: For web scraping and parsing.

- AWS EC2 + ALB + Terraform: For scalable deployment. 

## 📁 Project Structure

```
AI-Resume-Scanner/
├── app/
│   ├── resume_parser.py
│   ├── job_parser.py
│   └── __init__.py
├── data/
│   ├── resumes/
│   └── job_descriptions/
├── app.py
├── main.py                 
├── requirements.txt
└── README.md
```

## ⚙️ Local Setup

1. Clone the repository:
```bash
git clone https://github.com/durga985/AI-Job-analyzer.git
cd AI-Resume-Scanner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install --with-deps
```
3. Input your resume and job link or job description file

4. Run the script:
```bash
python3 main.py
streamlit run app.py
```

## 🧠 AI & NLP Details

•	Model: Sentence-BERT (all-MiniLM-L6-v2)
•	Similarity: Cosine Similarity on Embeddings
•	Keyword Extraction: Basic Regex + NLP Tokenization
•	Job Scraping: LinkedIn (via Playwright + BeautifulSoup)


### Example Output:
```
🤖 Semantic Match Score: 85.17%
🧩 Missing Keywords from Resume:
aws, scalable, cloud, communication, nlp, deployment
```

## ☁️ Cloud Deployment with Terraform and Load Balancer

1.	# Navigate to Terraform Directory

```bash
cd ai-job-analyzer-tf
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
 # Streamlit UI lauching after Deployment 
 ```bash
 http://<your-ec2-public-ip>:8501
 ```
2.	# Terraform AWS Implementation

```bash
Create main.tf file with terraform code
terraform init
terraform plan
terraform apply
```
3. # Access via Load Balancer DNS

```bash
Update the main.tf file with load balancer code along with terraform code
Example usage: http://<alb-dns>.amazonaws.com
```

4. # What’s Deployed

 - EC2 instance with Streamlit App.

 - Security Groups for HTTP/8501 via Load Balancer.
 
 - Load Balancer routing traffic to EC2.

 - Scalable Infrastructure as Code (IaC).


# ✅ Project Highlights

 - AI-Powered Resume Scoring

 - Real-time Job Scraping from LinkedIn

 - Cloud-Native, Scalable Architecture

 - Infrastructure as Code with Terraform

 - Interactive Web UI with Streamlit

## 🚀 Future Extensions

- Enhanced Job Scraper
- API-as-a-Service
- Containerization and Orchestration
- Multi-Job Role Matching

## 👩‍💻 Built By

 - Durga Phani Teja Pasupuleti
 - Sathwik Nellikoppa Basavaraja
 - Karthik Maganahalli Prakash
---
