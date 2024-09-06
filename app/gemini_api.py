import google.generativeai as genai
from app.config import settings

# Настройка API ключа
genai.configure(api_key=settings.gemini_api_key)


def generate_summary(text: str) -> str:
    """
    Генерация суммаризации текста с использованием модели Gemini.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Summarize the following text:\n\n{text}")
    return response.text


def answer_question(document_summary: str, question: str) -> str:
    # Настройка API Gemini (предполагается, что API_KEY уже настроен через переменные среды)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Формируем запрос: используем суммаризацию документа и вопрос пользователя
    prompt = f"Here is the document summary: {document_summary}. Now, answer the following question: {question}"

    # Отправляем запрос в нейросеть
    response = model.generate_content(prompt)

    # Возвращаем текст ответа
    return response.text
