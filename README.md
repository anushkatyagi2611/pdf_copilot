
# 📚 PDF Copilot – Your Page-Aware PDF Assistant

**Ever scrolled through a dense PDF and wished it could just *talk back*?**
**PDF Copilot** is your AI-powered, page-sensitive PDF assistant. It doesn’t just read your documents — it *understands* them, one page at a time.

Whether you're studying a textbook, scanning a research paper, analyzing scanned invoices, or decoding handwritten forms, PDF Copilot allows you to upload any PDF and interact with it through natural language questions — contextually grounded to the **current page** you’re viewing.

---

## 🔍 What makes PDF Copilot special?

🧠 **Context-Aware Q\&A**
Unlike traditional PDF search tools, this assistant understands **semantic meaning**, not just keywords. Ask questions like “What equation is being derived here?” or “What is the author explaining on this page?” — and get grounded answers.

🖼️ **Live PDF Scrolling with Page Sync**
As you scroll through your PDF in the frontend, the visible page number is tracked. Ask questions, and the backend knows *exactly* which page’s content to use for retrieval.

📄 **Handles Both Digital and Scanned PDFs**
Can’t extract text from a scanned page? No problem. The backend switches to **EasyOCR** when needed, ensuring no page goes unread.

⚡ **Super Fast Inference with Groq API**
Using LLaMA 3 hosted via **Groq**, your questions are answered with ultra-low latency and high accuracy.

🔍 **Retrieval-Augmented Generation (RAG)**
Smart document chunking and embedding ensure that answers are generated based on the most relevant page content — and not hallucinated from scratch.

---

## 🏗️ Tech Stack

| Layer      | Technology                   | Role                                                                |
| ---------- | ---------------------------- | ------------------------------------------------------------------- |
| Frontend   | HTML + JS + PDF.js           | Render full PDF, track visible page, ask AI                         |
| Backend    | FastAPI                      | File upload, text extraction, OCR, embedding, Q\&A routing          |
| OCR        | EasyOCR                      | For scanned/handwritten PDFs where text can't be directly extracted |
| Embeddings | Sentence Transformers        | For chunk-wise semantic search across PDF pages                     |
| LLM        | Groq API (LLaMA 3)           | Final answer generation using retrieved content                     |
| Storage    | In-memory / local file store | Store PDFs and page-wise extracted content                          |

---

## ⚙️ How It Works (End-to-End)

1. **PDF Upload**

   * You upload a PDF through the interface.
   * It gets stored and assigned a unique `pdf_id`.

2. **Page-wise Text Extraction**

   * For each page:

     * If it’s digital, extract using `fitz` (PyMuPDF).
     * If it’s scanned or image-only, fallback to OCR using EasyOCR.

3. **Chunking and Embedding**

   * The extracted content is chunked smartly (by sentence, lines, etc.).
   * Each chunk is embedded using Sentence Transformers and stored with the page number.

4. **Frontend Integration**

   * The frontend renders the entire PDF using PDF.js.
   * It detects the **currently visible page** and keeps it in sync with the backend.

5. **Q\&A Workflow**

   * User asks a question.
   * The frontend sends the question + visible `page_num` + `pdf_id`.
   * Backend:

     * Retrieves top-k chunks from that page (via semantic similarity).
     * Feeds them as context to Groq LLM along with the question.
     * Returns a thoughtful, page-aware answer.

---

### 🧪 Example Usage

* 💬 **General Questions**:  
  “What is being discussed on this page?”

* 📚 **Lecture Slides**:  
  “Summarize the bullet points shown here.”

* 🧾 **Financial Reports**:  
  “Is there any loss or profit reported on this page?”

* 🌐 **Research Papers**:  
  “What is the key conclusion of this experiment?”

* 📖 **Textbooks**:  
  “Explain this derivation in simpler terms.”


---

## 🚀 Getting Started (Local Dev Setup)

### 1. Clone the repo

```bash
git clone https://github.com/anushkatyagi2611/pdf_copilot.git
cd backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI backend

```bash
uvicorn main:app --reload
```

### 4. Launch the frontend

Just open `frontend/index.html` in your browser.
Make sure it’s allowed to talk to your backend (`http://localhost:8000`).

---

## 🛠️ Folder Structure
```bash
├── backend/                # FastAPI backend for file handling, page-wise extraction, and LLM-based Q&A
│   ├── main.py             # Core backend logic (upload, OCR, RAG, Groq API integration)
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Lightweight frontend powered by PDF.js and vanilla JS
│   ├── index.html          # Web UI structure
│   ├── app.js              # Handles page detection and communication with backend
│   ├── pdf.js              # PDF.js viewer engine
│   ├── pdf.worker.js       # PDF.js worker
│   └── style.css           # Aesthetic styling (Inter font, modern layout)
│
├── venv/                   # Virtual environment (not pushed to GitHub)
├── .env                    # API keys and secrets (excluded via .gitignore)
├── .gitattributes          # Git configuration
└── README.md               # You’re here!

```
---


## 🧑‍💻 Contributing

Contributions are welcome!
Want to improve chunking strategies? OCR fallback? Add a UI chat thread?
Create a branch and send in a PR 🚀

---


## 👩‍💻 Made by Anushka

Crafted with ❤️, caffeine, and a passion for beautiful, fast AI interfaces.

---

