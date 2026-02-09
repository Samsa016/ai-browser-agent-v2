import base64
from openai import AsyncOpenAI
from app.services.models import AgentAction
from app.config import settings

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key = settings.openai_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    async def get_action(self, screenshot_path: str, element_count: int) -> AgentAction:
        base64_image = self._encode_image(screenshot_path)
        messages = [
            {
                "role": "system",
                "content": (
                    "Ты — автономный браузерный агент. Твоя цель — выполнить задачу пользователя. "
                    "На изображении ты видишь интерфейс с красными метками (ID). "
                    f"Всего меток на экране: {element_count}. "
                    "Анализируй интерфейс и верни действие в формате JSON. "
                    "Не выдумывай ID, которых нет."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "Что мне делать дальше? Проанализируй скриншот."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        response = await self.client.beta.chat.completions.parse(
            model=settings.model_name,
            messages=messages,
            response_format=AgentAction 
        )

        return response.choices[0].message.parsed
    