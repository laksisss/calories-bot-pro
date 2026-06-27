from groq import Groq
import json
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

async def analyze_text_meal(text: str):
    prompt = f"""Ты эксперт по питанию. Проанализируй описание еды и верни ТОЛЬКО JSON.

Описание: {text}

Верни JSON БЕЗ пояснений:
{{
    "name": "название блюда",
    "weight": 100,
    "calories": 250,
    "protein": 15,
    "fat": 8,
    "carbs": 30
}}

Если несколько продуктов - верни массив объектов."""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "Ты помощник по питанию. Отвечай только JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        text_response = response.choices[0].message.content.strip()
        
        if '[' in text_response:
            start = text_response.find('[')
            end = text_response.rfind(']') + 1
        else:
            start = text_response.find('{')
            end = text_response.rfind('}') + 1
        
        if start != -1 and end != 0:
            data = json.loads(text_response[start:end])
            if isinstance(data, list):
                return data[0] if data else None
            return data
    except Exception as e:
        print(f"Groq error: {e}")
    
    return None

async def analyze_photo(image_bytes: bytes):
    print("Анализ фото временно недоступен")
    return None
