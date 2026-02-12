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

    async def get_action(self, screenshot_path: str, element_count: int, prompt_context: str = "") -> AgentAction:
        base64_image = self._encode_image(screenshot_path)
        
        system_prompt = (
            "You are a focused web automation agent. "
            "Your ONLY goal is to complete the user's specific request. "
            "Do NOT get distracted by the website content (news, articles, ads) unless the user asks for them.\n"
            f"There are {element_count} interactive elements (red tags) on the screen.\n"
            "CRITICAL RULES:\n"
            "1. IF THE GOAL IS TO FIND INFORMATION (e.g., 'price', 'weather', 'who is'): "
            "   - IMMEDIATELY look for a Search Bar (input) or a Search Icon (magnifying glass). "
            "When you select the 'type' action, the text_input field should contain a specific user request, not a placeholder. \n"
            "   - DO NOT CLICK on random news articles.\n"
            "2. IF THE GOAL IS NAVIGATION: Click the relevant link.\n"
            "3. IGNORE popups asking to subscribe or sign in (look for 'X' or 'Close').\n"
            "4. Analyze the HISTORY. If you are repeating actions, STOP and try something else."
            "5. IF YOU SEE A CAPTCHA or 'I am not a robot' check: DO NOT CLICK IT. It requires human interaction. Return action_type='wait' immediately and ask the user for help in the reasoning."
        )

        user_message_content = [
            {
                "type": "text", 
                "text": f"CURRENT OBJECTIVE & HISTORY:\n{prompt_context}\n\nINSTRUCTION: Ignore the news feed. Focus ONLY on the Objective. What is the next step?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            }
        ]

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message_content}
        ]
        
        response = await self.client.beta.chat.completions.parse(
            model=settings.model_name,
            messages=messages,
            response_format=AgentAction 
        )

        return response.choices[0].message.parsed
    