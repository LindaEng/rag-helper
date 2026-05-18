# 📚 RAG Learning Assistant

> Turn dry textbooks into interactive conversations. Ask questions, get answers with sources, and learn faster.

## 🎯 Why I Built This

Let's be real - reading through dense textbooks and documentation is hard. It's time-consuming, boring, and for people with ADHD or other neurodivergent conditions, it can feel impossible to stay focused.

I built this tool because **learning shouldn't be a battle with text**. It should be a conversation.

This is a **Retrieval-Augmented Generation (RAG)** application that lets you:
- Upload any PDF (textbook, manual, research paper)
- Ask questions in plain English
- Get answers with **exact page references** so you can verify
- Learn at your own pace, through dialogue instead of monologue

## ✨ Features

| Feature | What It Does |
|---------|---------------|
| 📄 PDF Upload | Upload any document |
| 💬 Natural Language Q&A | Ask questions like you're talking to a tutor |
| 📍 Source Attribution | Every answer shows the page number it came from |
| 🧠 RAG Architecture | Answers are grounded in your document - no hallucinations |
| 🚀 Fast LLM | Powered by Groq's Llama 3.3 (70B) - answers in seconds |

## 🔮 Coming Soon

- 📝 Auto-generated quizzes by chapter
- 🗣️ AI discussion partner that debates the material with you
- 📊 Learning assessment that tracks your progress
- 🎯 Flashcard generation from your uploads

## 🏗️ How It Works

**Pipeline One: Upload & Index (Ingestion)**

1. User uploads a PDF file
2. PDF processor extracts text from each page
3. Text is split into chunks (~1000 characters each)
4. Each chunk is converted into a vector (384 numbers)
5. Vectors + original text are stored in Qdrant database

**Pipeline Two: Ask & Answer (Query)**

1. User asks a question in plain English
2. Question is converted into a vector (same method)
3. System searches for the 3 most similar vectors in the database
4. Those chunks become the "context" for the LLM
5. LLM generates an answer using ONLY the context + question
6. Answer is returned with source references (filename + page number)

**Why this matters:** The LLM never makes up information. It can only answer from your document. No hallucinations. No "I think so." Just grounded answers you can trust.

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Groq API key (free at console.groq.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/rag-learning-assistant.git
cd rag-learning-assistant/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo "GROQ_API_KEY=your_key_here" > .env

## 🚀 Run the Backend

```bash
uvicorn app.main:app --reload
```

Your API will be live at `http://localhost:8000`

## 💻 Run the Frontend

```bash
cd frontend
npm run dev
```

## 📤 Upload Your PDF

Use the upload button to select a PDF file (textbook, manual, research paper, etc.)

## 💬 Ask a Question

Type your question in plain English. For example:
- "What are the main topics in chapter 3?"
- "Explain how this system works"
- "Summarize the key takeaways"

The AI will respond with an answer and show you exactly which page it came from.