# 🤖 AI HR Recruitment Assistant

An AI-powered HR Recruitment Assistant that uses **Qwen3:4B**, **Ollama**, and a lightweight **RAG-based retrieval system** to analyze resumes, compare candidates with job descriptions, and answer questions about uploaded resumes.

## 📌 Project Overview

Recruiters often need to manually review resumes and compare candidate skills with job requirements. This project simplifies the initial screening process by extracting information from resumes and using AI to provide recruitment insights.

The system analyzes a candidate's resume against a job description and allows recruiters to ask questions directly about the uploaded resume.

## ✨ Features

- 📄 Upload candidate resumes in PDF or TXT format
- 💼 Upload or enter external job descriptions
- 🔍 Analyze candidate suitability for a job
- 📊 Generate estimated job-match percentage
- 🧠 Identify matching and missing skills
- 💪 Analyze candidate strengths and concerns
- 👨‍💼 Generate recruitment recommendations
- ❓ Generate interview questions/areas
- 💬 Ask questions about the uploaded resume
- 🔎 Retrieve relevant resume information before generating answers
- 🛡️ Reduce AI hallucination by restricting answers to resume information
- 💻 Run Qwen3 locally using Ollama
- 🗨️ Maintain previous questions and answers during the session

## 🏗️ System Architecture

```text
                 HR / Recruiter
                       |
                       v
              Streamlit Interface
                 /           \
                /             \
               v               v
        Candidate Resume    Job Description
               |
               v
        Text Extraction
               |
               v
      Resume Information
          Organization
               |
               v
    Relevant Information Retrieval
               |
               v
            Qwen3:4B
               |
               v
       Recruitment Analysis
               |
               v


Uploaded Resume
      ↓
Text Extraction
      ↓
Resume Section Detection
      ↓
Relevant Information Retrieval
      ↓
Retrieved Resume Context
      ↓
Qwen3:4B
      ↓
Grounded Answer
        Resume Q&A Chat



````markdown
## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/pavindoss/AI-HR-Recruitment-Assistant
cd ai-hr-recruitment-assistant
````

### 2. Install Required Python Packages

```bash
pip install -r requirements.txt
```

### 3. Install and Setup Ollama

Download and install Ollama on your system.

Then download the Qwen3:4B model:

```bash
ollama pull qwen3:4b
```

### 4. Start Qwen3:4B

```bash
ollama run qwen3:4b
```

Keep Ollama running while using the application.

## ▶️ Run the Application

Open a **new terminal** in the project folder and run:

```bash
python -m streamlit run ibm.py
```

The application will start in the browser at:

```text
http://localhost:8501
```

## 📝 Usage

1. Upload the candidate resume in PDF or TXT format.
2. Upload an external Job Description or enter it manually.
3. Click **Evaluate Candidate**.
4. View the AI-based recruitment analysis.
5. Ask questions in **Resume Intelligence Chat**.
6. Qwen3 answers using relevant information retrieved from the uploaded resume.

```
```
