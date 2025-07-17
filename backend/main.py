# # import os
# # import fitz                    
# # from PIL import Image
# # from paddleocr import PaddleOCR
# # from groq import Groq
# # import numpy as np

# # # client = Groq(
# # #     api_key=os.getenv("GROQ_API_KEY")  # Add fallback
# # # )
# # client= Groq(api_key="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")

# # # Initialize OCR
# # ocr = PaddleOCR(use_textline_orientation=True, lang="en")

# # def extract_text_and_images(pdf_path, page_num):
# #     """
# #     Returns (raw_text, list_of_PIL_images) for a given PDF page.
# #     """
# #     doc = fitz.open(pdf_path)
# #     page = doc.load_page(page_num)
# #     # Extract selectable text
# #     text = page.get_text().strip()
# #     # Extract embedded images
# #     pil_images = []
# #     for img in page.get_images(full=True):
# #         xref = img[0]
# #         base_image = doc.extract_image(xref)
# #         pix = fitz.Pixmap(base_image["image"])
# #         mode = "RGB" if pix.n < 4 else "RGBA"
# #         img_pil = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
# #         pil_images.append(img_pil)
# #     doc.close()
# #     return text, pil_images

# # def ocr_images(images):
# #     ocr_texts = []
# #     for img in images:
# #         # Convert PIL Image to numpy array
# #         img_array = np.array(img)
        
# #         # Now give the numpy array to OCR
# #         result = ocr.ocr(img_array)
        
# #         # Extract text from results
# #         if result and result[0]:
# #             for line in result[0]:
# #                 if line and len(line) > 1:
# #                     ocr_texts.append(line[1][0])
    
# #     return "\n".join(ocr_texts)

# # def groq_chat_completion(prompt):
# #     """
# #     Using Groq API for explanation
# #     """
# #     try:
# #         chat_completion = client.chat.completions.create(
# #             messages=[
# #                 {
# #                     "role": "user",
# #                     "content": prompt,
# #                 }
# #             ],
# #             model="llama3-8b-8192",
# #             temperature=0.3,
# #             max_tokens=500,
# #         )
# #         return chat_completion.choices[0].message.content
# #     except Exception as e:
# #         return f"Error getting explanation: {str(e)}"

# # def explain_pdf_page(pdf_path, page_num):
# #     print(f"\n=== DEBUGGING PAGE {page_num + 1} ===")
    
# #     raw_text, images = extract_text_and_images(pdf_path, page_num)
    
# #     # DEBUG: Show what was extracted
# #     print(f"Extracted text length: {len(raw_text)} characters")
# #     print(f"Number of images found: {len(images)}")
# #     # print(f"Raw extracted text:")
# #     # print("-" * 40)
# #     # print(repr(raw_text))  # Use repr to see special characters
# #     # print("-" * 40)

# #     # If no text extracted, fallback to OCR
# #     if not raw_text.strip() and images:
# #         print("[i] No text found—running OCR on images…")
# #         ocr_text = ocr_images(images)
# #         print(f"OCR text length: {len(ocr_text)} characters")
# #         print(f"OCR extracted text:")
# #         print("-" * 40)
# #         print(repr(ocr_text))
# #         print("-" * 40)
# #         raw_text = ocr_text
# #     # If images also present, append OCR text
# #     elif images:
# #         print("[i] Found both text and images—also running OCR…")
# #         ocr_text = ocr_images(images)
# #         if ocr_text.strip():
# #             print(f"OCR text length: {len(ocr_text)} characters")
# #             print(f"OCR extracted text:")
# #             print("-" * 40)
# #             print(repr(ocr_text))
# #             print("-" * 40)
# #             raw_text += "\n\n[OCR]:\n" + ocr_text

# #     # print(f"\nFinal text being sent to Groq:")
# #     # print("-" * 40)
# #     # print(raw_text)
# #     # print("-" * 40)
# #     # print(f"Final text length: {len(raw_text)} characters")

# #     user_prompt = input("\nEnter your question/prompt about this content: ").strip()
# #     if not user_prompt:
# #         user_prompt = "What is this about?"  # Default if user enters nothing
    
# #     # Combine fixed context with user's variable prompt
# #     prompt = f"""Here is the PDF content:

# #     {raw_text}

# #     User's question: {user_prompt}

# #     Answer the question using the given text only if the answer is clearly present.
# #     If not, use your own knowledge to answer it briefly and accurately.
# #     Do not repeat or paraphrase irrelevant parts of the text.
# #     Do not give answers from raw text only use ypur own knowledge too.
# #     Just give the best possible answer to the question and not other extra things like what is given in text or not."""
# #     print(f"\nSending to Groq...")
# #     result = groq_chat_completion(prompt)
# #     print(f"Groq response received: {len(result)} characters")

# #     return result

# # if __name__ == "__main__":
# #     pdf_path = input("PDF path: ").strip()
# #     page_str = input("Page number to explain: ").strip()
# #     try:
# #         page_idx = int(page_str) - 1
# #         result = explain_pdf_page(pdf_path, page_idx)
# #         # print("\n" + "="*60)
# #         print("ANSWER:")
# #         # print("="*60)
# #         print(result)
# #     except Exception as e:
# #         print("Error:", e)
# import os
# import fitz                    
# from PIL import Image
# import easyocr
# from groq import Groq
# import numpy as np

# # client = Groq(
# #     api_key=os.getenv("GROQ_API_KEY")  # Add fallback
# # )
# client = Groq(api_key="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")
# # Initialize EasyOCR reader
# print("Initializing EasyOCR reader...")
# reader = easyocr.Reader(['en'])  # Initialize with English language

# def extract_text_and_images(pdf_path, page_num):
#     """
#     Returns (raw_text, list_of_PIL_images) for a given PDF page.
#     """
#     doc = fitz.open(pdf_path)
#     page = doc.load_page(page_num)
#     # Extract selectable text
#     text = page.get_text().strip()
#     # Extract embedded images
#     pil_images = []
#     for img in page.get_images(full=True):
#         xref = img[0]
#         base_image = doc.extract_image(xref)
#         pix = fitz.Pixmap(base_image["image"])
#         mode = "RGB" if pix.n < 4 else "RGBA"
#         img_pil = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
#         pil_images.append(img_pil)
#     doc.close()
#     return text, pil_images

# def ocr_images(images):
#     """
#     Perform OCR on images using EasyOCR
#     """
#     ocr_texts = []
#     for img in images:
#         # Convert PIL Image to numpy array (RGB format)
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#         img_array = np.array(img)
        
#         # EasyOCR readtext method
#         results = reader.readtext(img_array)
        
#         # Extract text from results
#         # Each result is a tuple of (bounding_box, text, confidence)
#         image_text = []
#         for result in results:
#             text = result[1]  # Get the text part
#             confidence = result[2]  # Get confidence score
#             # Only include text with reasonable confidence
#             if confidence > 0.3:  # Adjust threshold as needed
#                 image_text.append(text)
        
#         if image_text:
#             ocr_texts.append(" ".join(image_text))
    
#     return "\n".join(ocr_texts)

# def groq_chat_completion(prompt):
#     """
#     Using Groq API for explanation
#     """
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt,
#                 }
#             ],
#             model="llama3-8b-8192",
#             temperature=0.3,
#             max_tokens=500,
#         )
#         return chat_completion.choices[0].message.content
#     except Exception as e:
#         return f"Error getting explanation: {str(e)}"

# def explain_pdf_page(pdf_path, page_num):
#     print(f"\n=== DEBUGGING PAGE {page_num + 1} ===")
    
#     raw_text, images = extract_text_and_images(pdf_path, page_num)
    
#     # DEBUG: Show what was extracted
#     print(f"Extracted text length: {len(raw_text)} characters")
#     print(f"Number of images found: {len(images)}")
#     # print(f"Raw extracted text:")
#     # print("-" * 40)
#     # print(repr(raw_text))  # Use repr to see special characters
#     # print("-" * 40)

#     # If no text extracted, fallback to OCR
#     if not raw_text.strip() and images:
#         print("[i] No text found—running OCR on images…")
#         ocr_text = ocr_images(images)
#         print(f"OCR text length: {len(ocr_text)} characters")
#         print(f"OCR extracted text:")
#         print("-" * 40)
#         print(repr(ocr_text))
#         print("-" * 40)
#         raw_text = ocr_text
#     # If images also present, append OCR text
#     elif images:
#         print("[i] Found both text and images—also running OCR…")
#         ocr_text = ocr_images(images)
#         if ocr_text.strip():
#             print(f"OCR text length: {len(ocr_text)} characters")
#             print(f"OCR extracted text:")
#             print("-" * 40)
#             print(repr(ocr_text))
#             print("-" * 40)
#             raw_text += "\n\n[OCR]:\n" + ocr_text

#     # print(f"\nFinal text being sent to Groq:")
#     # print("-" * 40)
#     # print(raw_text)
#     # print("-" * 40)
#     # print(f"Final text length: {len(raw_text)} characters")

#     user_prompt = input("\nEnter your question/prompt about this content: ").strip()
#     if not user_prompt:
#         user_prompt = "What is this about?"  # Default if user enters nothing
    
#     # Combine fixed context with user's variable prompt
#     prompt = f"""Here is the PDF content:

#     {raw_text}

#     User's question: {user_prompt}

#     Answer the question using the given text only if the answer is clearly present.
#     If not, use your own knowledge to answer it briefly and accurately.
#     Do not repeat or paraphrase irrelevant parts of the text.
#     Do not give answers from raw text only use your own knowledge too.
#     Just give the best possible answer to the question and not other extra things like what is given in text or not."""
    
#     print(f"\nSending to Groq...")
#     result = groq_chat_completion(prompt)
#     print(f"Groq response received: {len(result)} characters")

#     return result

# if __name__ == "__main__":
#     pdf_path = input("PDF path: ").strip()
#     page_str = input("Page number to explain: ").strip()
#     try:
#         page_idx = int(page_str) - 1
#         result = explain_pdf_page(pdf_path, page_idx)
#         # print("\n" + "="*60)
#         print("ANSWER:")
#         # print("="*60)
#         print(result)
#     except Exception as e:
#         print("Error:", e)
# fastapi_backend.py
from fastapi import FastAPI, UploadFile, File, Form, Query
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

app = FastAPI()

# Allow frontend access (e.g., from localhost:3000 or wherever you host)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")
reader = easyocr.Reader(['en'])

# Store uploaded PDFs in temp dir (in-memory or disk)
pdf_store = {}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save PDF to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    pdf_id = os.path.basename(tmp_path)
    pdf_store[pdf_id] = tmp_path
    return {"pdf_id": pdf_id}


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

    raw_text, images = extract_text_and_images(pdf_path, int(page_num))
    if not raw_text.strip() and images:
        raw_text = ocr_images(images)
    elif images:
        raw_text += "\n\n[OCR]:\n" + ocr_images(images)

    prompt = f"""Here is the PDF content:

    {raw_text}

    User's question: {question}

    Answer the question using the given text only if the answer is clearly present.
    If not, use your own knowledge to answer it briefly and accurately.
    Just give the best possible answer to the question and not other extra things like what is given in text or not."""

    result = groq_chat_completion(prompt)
    return {"answer": result}


# Your original helpers can remain the same
def extract_text_and_images(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    text = page.get_text().strip()
    images = []
    for img in page.get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        pix = fitz.Pixmap(base_image["image"])
        mode = "RGB" if pix.n < 4 else "RGBA"
        img_pil = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        images.append(img_pil)
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
