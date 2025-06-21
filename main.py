# import os
# import fitz                    
# from PIL import Image
# from paddleocr import PaddleOCR
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from groq import Groq
# import torch

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")  # Replace with your actual API key
# )

# # Initialize OCR
# ocr = PaddleOCR(use_textline_orientation=True, lang="en")

# # Replace your model loading with:
# # tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# # model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

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
#     return text, pil_images

# # def ocr_images(images):
# #     """
# #     Runs OCR on each PIL image, concatenates results.
# #     """
# #     ocr_texts = []
# #     for img in images:
# #         result = ocr.ocr(img)
# #         for line in result:
# #             ocr_texts.append(line[1][0])
# #     return "\n".join(ocr_texts)
# import numpy as np  # Make sure you have this import

# def ocr_images(images):
#     ocr_texts = []
#     for img in images:  # img is PIL Image
#         # Convert PIL Image to numpy array
#         img_array = np.array(img)  # This is the key line!
        
#         # Now give the numpy array to OCR
#         result = ocr.ocr(img_array)  # ✅ This will work
        
#         # Extract text from results
#         if result and result[0]:
#             for line in result[0]:
#                 if line and len(line) > 1:
#                     ocr_texts.append(line[1][0])
    
#     return "\n".join(ocr_texts)

# # def local_chat_completion(prompt):
# #     """
# #     Using Flan-T5-Small locally to generate a simple explanation.
# #     """
# #     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
# #     outputs = model.generate(**inputs, max_new_tokens=200)
# #     return tokenizer.decode(outputs[0], skip_special_tokens=True)

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
#             model="llama3-8b-8192",  # Fast Llama model
#             temperature=0.3,
#             max_tokens=500,
#         )
#         return chat_completion.choices[0].message.content
#     except Exception as e:
#         return f"Error getting explanation: {str(e)}"

# def explain_pdf_page(pdf_path, page_num):
#     raw_text, images = extract_text_and_images(pdf_path, page_num)

#     # If no text extracted, fallback to OCR
#     if not raw_text.strip() and images:
#         print("[i] No text found—running OCR on images…")
#         raw_text = ocr_images(images)
#     # If images also present, append OCR text
#     elif images:
#         ocr_text = ocr_images(images)
#         if ocr_text.strip():
#             raw_text += "\n\n[OCR]:\n" + ocr_text

#     prompt = f"""Please explain the following PDF page content in simple, clear terms. 
    
#     Focus on:
#     1. Main topic/theme
#     2. Key points or ideas
#     3. Why this information matters

#     PDF Page Content:
#     {raw_text[:]}  

#     Provide a concise but comprehensive explanation:"""
#     return groq_chat_completion(prompt)

# if __name__ == "__main__":
#     pdf_path = input("PDF path: ").strip()
#     page_str = input("Page number to explain: ").strip()
#     try:
#         page_idx = int(page_str) - 1
#         explanation = explain_pdf_page(pdf_path, page_idx)
#         print("\n— Explanation —\n")
#         print(explanation)
#     except Exception as e:
#         print("Error:", e)

import os
import fitz                    
from PIL import Image
from paddleocr import PaddleOCR
from groq import Groq
import numpy as np

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")  # Add fallback
# )
client= Groq(api_key="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")

# Initialize OCR
ocr = PaddleOCR(use_textline_orientation=True, lang="en")

def extract_text_and_images(pdf_path, page_num):
    """
    Returns (raw_text, list_of_PIL_images) for a given PDF page.
    """
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    # Extract selectable text
    text = page.get_text().strip()
    # Extract embedded images
    pil_images = []
    for img in page.get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        pix = fitz.Pixmap(base_image["image"])
        mode = "RGB" if pix.n < 4 else "RGBA"
        img_pil = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        pil_images.append(img_pil)
    doc.close()
    return text, pil_images

def ocr_images(images):
    ocr_texts = []
    for img in images:
        # Convert PIL Image to numpy array
        img_array = np.array(img)
        
        # Now give the numpy array to OCR
        result = ocr.ocr(img_array)
        
        # Extract text from results
        if result and result[0]:
            for line in result[0]:
                if line and len(line) > 1:
                    ocr_texts.append(line[1][0])
    
    return "\n".join(ocr_texts)

def groq_chat_completion(prompt):
    """
    Using Groq API for explanation
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=500,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error getting explanation: {str(e)}"

def explain_pdf_page(pdf_path, page_num):
    print(f"\n=== DEBUGGING PAGE {page_num + 1} ===")
    
    raw_text, images = extract_text_and_images(pdf_path, page_num)
    
    # DEBUG: Show what was extracted
    print(f"Extracted text length: {len(raw_text)} characters")
    print(f"Number of images found: {len(images)}")
    # print(f"Raw extracted text:")
    # print("-" * 40)
    # print(repr(raw_text))  # Use repr to see special characters
    # print("-" * 40)

    # If no text extracted, fallback to OCR
    if not raw_text.strip() and images:
        print("[i] No text found—running OCR on images…")
        ocr_text = ocr_images(images)
        print(f"OCR text length: {len(ocr_text)} characters")
        print(f"OCR extracted text:")
        print("-" * 40)
        print(repr(ocr_text))
        print("-" * 40)
        raw_text = ocr_text
    # If images also present, append OCR text
    elif images:
        print("[i] Found both text and images—also running OCR…")
        ocr_text = ocr_images(images)
        if ocr_text.strip():
            print(f"OCR text length: {len(ocr_text)} characters")
            print(f"OCR extracted text:")
            print("-" * 40)
            print(repr(ocr_text))
            print("-" * 40)
            raw_text += "\n\n[OCR]:\n" + ocr_text

    # print(f"\nFinal text being sent to Groq:")
    # print("-" * 40)
    # print(raw_text)
    # print("-" * 40)
    # print(f"Final text length: {len(raw_text)} characters")

    user_prompt = input("\nEnter your question/prompt about this content: ").strip()
    if not user_prompt:
        user_prompt = "What is this about?"  # Default if user enters nothing
    
    # Combine fixed context with user's variable prompt
    prompt = f"""Here is the PDF content:

    {raw_text}

    User's question: {user_prompt}

    Answer the question using the given text only if the answer is clearly present.
    If not, use your own knowledge to answer it briefly and accurately.
    Do not repeat or paraphrase irrelevant parts of the text.
    Do not give answers from raw text only use ypur own knowledge too.
    Just give the best possible answer to the question and not other extra things like what is given in text or not."""
    print(f"\nSending to Groq...")
    result = groq_chat_completion(prompt)
    print(f"Groq response received: {len(result)} characters")

    return result

if __name__ == "__main__":
    pdf_path = input("PDF path: ").strip()
    page_str = input("Page number to explain: ").strip()
    try:
        page_idx = int(page_str) - 1
        result = explain_pdf_page(pdf_path, page_idx)
        # print("\n" + "="*60)
        print("ANSWER:")
        # print("="*60)
        print(result)
    except Exception as e:
        print("Error:", e)