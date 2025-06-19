import os
import fitz                    
from PIL import Image
from paddleocr import PaddleOCR
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Initialize OCR
ocr = PaddleOCR(use_textline_orientation=True, lang="en")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

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
    return text, pil_images


def ocr_images(images):
    """
    Runs OCR on each PIL image, concatenates results.
    """
    ocr_texts = []
    for img in images:
        result = ocr.ocr(img, cls=True)
        for line in result:
            ocr_texts.append(line[1][0])
    return "\n".join(ocr_texts)


def local_chat_completion(prompt):
    """
    Using Flan-T5-Small locally to generate a simple explanation.
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def explain_pdf_page(pdf_path, page_num):
    raw_text, images = extract_text_and_images(pdf_path, page_num)

    # If no text extracted, fallback to OCR
    if not raw_text.strip() and images:
        print("[i] No text found—running OCR on images…")
        raw_text = ocr_images(images)
    # If images also present, append OCR text
    elif images:
        ocr_text = ocr_images(images)
        if ocr_text.strip():
            raw_text += "\n\n[OCR]:\n" + ocr_text

    prompt = f"Please explain this PDF page in simple terms:\n\n{raw_text[:1000]}"
    return local_chat_completion(prompt)

if __name__ == "__main__":
    pdf_path = input("PDF path: ").strip()
    page_str = input("Page number to explain: ").strip()
    try:
        page_idx = int(page_str) - 1
        explanation = explain_pdf_page(pdf_path, page_idx)
        print("\n— Explanation —\n")
        print(explanation)
    except Exception as e:
        print("Error:", e)
