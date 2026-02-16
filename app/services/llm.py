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
            "You are a state-aware web automation agent. "
            "Your goal is to manage your internal state to complete tasks efficiently.\n"
            f"There are {element_count} interactive elements detected.\n\n"
            
            "STATE MACHINE (MENTAL MODEL):\n"
            "1. **SEARCHING**: You are looking for a list of results. Focus on BLUE Inputs. Ignore content text.\n"
            "2. **SELECTING**: You see a list of results. Focus on RED Links. Ignore the Search Bar.\n"
            "3. **VIEWING/EXTRACTING**: You opened a specific item. **CRITICAL: IGNORE THE SEARCH BAR.** Focus on reading content or saving data.\n"
            "4. **DONE**: Data is saved. Stop.\n\n"

            "VISUALS:\n"
            " - **BLUE** = Inputs. **RED** = Links/Buttons. Tags at TOP-RIGHT.\n\n"

            "GUIDELINES:\n"
            "1. **State Consistency**: If you just clicked a link in a list, your next state MUST be 'VIEWING'.\n"
            "2. **No Backtracking**: If you are in 'VIEWING' phase, DO NOT go back to 'SEARCHING' unless the page is wrong.\n"
            "3. **Extraction**: Use action_type='extract' ONLY in 'VIEWING' phase.\n"
            "4. **Direct Nav**: Use 'goto' for 'hh.ru' if requested.\n"
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
    