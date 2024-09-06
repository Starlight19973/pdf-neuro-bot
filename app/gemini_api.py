import google.generativeai as genai
from app.config import settings


genai.configure(api_key=settings.gemini_api_key)


def generate_summary(text: str) -> str:
    """
    Генерация суммаризации текста с использованием модели Gemini.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Summarize the following text:\n\n{text}")
    return response.text


def answer_question(document_summary: str, question: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Here is the document summary: {document_summary}. Now, answer the following question: {question}"
    response = model.generate_content(prompt)
    return response.text
