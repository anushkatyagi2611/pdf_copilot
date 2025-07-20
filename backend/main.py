from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import fitz
from PIL import Image
import easyocr
import numpy as np
from groq import Groq
import tempfile
import shutil
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")  # Replace with your actual API key
reader = easyocr.Reader(['en'])
embedder = SentenceTransformer('all-MiniLM-L6-v2')

pdf_store = {}

# @app.post("/upload_pdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         shutil.copyfileobj(file.file, tmp)
#         tmp_path = tmp.name

#     pdf_id = os.path.basename(tmp_path)
#     pdf_store[pdf_id] = tmp_path
#     return {"pdf_id": pdf_id}

# pdf_store = {}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save PDF to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    pdf_id = os.path.basename(tmp_path)
    pdf_store[pdf_id] = tmp_path
    return {"pdf_id": pdf_id}

# @app.get("/get_pdf/")
# def get_pdf(pdf_id: str = Query(...)):
#     path = pdf_store.get(pdf_id)
#     if not path or not os.path.exists(path):
#         return {"error": "PDF not found"}
#     return FileResponse(path, media_type='application/pdf', filename=pdf_id)

# @app.get("/view_pdf/")
# def view_pdf(pdf_id: str = Query(...)):
#     # Just a helper endpoint to preview the PDF in the browser
#     return HTMLResponse(f"""
#         <html>
#         <body style='margin:0;padding:0'>
#             <embed src="/get_pdf/?pdf_id={pdf_id}" type="application/pdf" width="100%" height="100%" />
#         </body>
#         </html>
#     """)

@app.get("/get_page_text/")
def get_page_text(pdf_id: str = Query(...), page_num: int = Query(...)):
    pdf_path = pdf_store.get(pdf_id)
    if not pdf_path:
        return {"error": "PDF not found."}

    text, images = extract_text_and_images(pdf_path, page_num)
    if not text.strip() and images:
        text = ocr_images(images)
    elif images:
        text += "\n\n[OCR]:\n" + ocr_images(images)

    return {"page_text": text}

@app.post("/ask/")
async def ask_question(
    pdf_id: str = Form(...),
    page_num: int = Form(...),
    question: str = Form(...)
):
    pdf_path = pdf_store.get(pdf_id)
    if not pdf_path:
        return {"error": "PDF not found."}

    context_chunks = []

    for i in range(max(0, page_num - 2), page_num + 1):
        raw_text, images = extract_text_and_images(pdf_path, i)
        if not raw_text.strip() and images:
            raw_text = ocr_images(images)
        elif images:
            raw_text += "\n\n[OCR]:\n" + ocr_images(images)

        chunks = chunk_text(raw_text)
        context_chunks.extend(chunks)

    if not context_chunks:
        return {"error": "No content found in the selected pages."}

    chunk_embeddings = embedder.encode(context_chunks, convert_to_tensor=True)
    query_embedding = embedder.encode(question, convert_to_tensor=True)

    similarities = util.cos_sim(query_embedding, chunk_embeddings)[0]
    top_k = 5
    k = min(top_k, similarities.size(0))
    top_results = similarities.topk(k=k)
    # top_results = similarities.topk(k=top_k)
    retrieved_chunks = [context_chunks[i] for i in top_results[1]]

    prompt = f"""Use the following retrieved content to answer the user's question.

    Context:{chr(10).join(retrieved_chunks)}

    User's question:{question}

    Answer the question using the given text only if the answer is clearly present.
    If not, use your own knowledge to answer it briefly and accurately.
    Do not write any other thing except the answer like: "According to the given content" or "The text is not mentioned".
    In every answer try enhancing or simplifying the answer using your own knowledge."""

    result = groq_chat_completion(prompt)
    return {"answer": result}

# ---------- Helper Functions ----------

def extract_text_and_images(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    text = ""
    images = []
    try:
        page = doc.load_page(page_num)
        text = page.get_text().strip()
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            pix = fitz.Pixmap(base_image["image"])
            mode = "RGB" if pix.n < 4 else "RGBA"
            img_pil = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            images.append(img_pil)
    except Exception:
        pass
    doc.close()
    return text, images

def ocr_images(images):
    ocr_texts = []
    for img in images:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_array = np.array(img)
        results = reader.readtext(img_array)
        image_text = [res[1] for res in results if res[2] > 0.3]
        if image_text:
            ocr_texts.append(" ".join(image_text))
    return "\n".join(ocr_texts)

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def groq_chat_completion(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=500,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
