import anthropic
import json
from config import ANTHROPIC_API_KEY, CLAUDE_TEXT_MODEL, CLAUDE_VISION_MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

async def analyze_text_meal(text: str):
    prompt = f"""Проанализируй описание еды и верни JSON с КБЖУ.
Описание: {text}
Верни JSON в формате:
{{"name": "название", "weight": 100, "calories": 250, "protein": 15, "fat": 8, "carbs": 30}}
"""
    message = client.messages.create(
        model=CLAUDE_TEXT_MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        response = message.content[0].text
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(response[start:end])
    except:
        pass
    return None

async def analyze_photo(image_base64: str, media_type: str = "image/jpeg"):
    prompt = """Определи блюдо на фото, вес порции и КБЖУ.
Верни JSON: {"name": "название", "weight": 250, "calories": 450, "protein": 25, "fat": 18, "carbs": 45}"""
    message = client.messages.create(
        model=CLAUDE_VISION_MODEL,
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_base64}},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    try:
        response = message.content[0].text
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(response[start:end])
    except:
        pass
    return None