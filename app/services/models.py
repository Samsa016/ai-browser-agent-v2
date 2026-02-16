from pydantic import Field, BaseModel, Phase
from typing import Literal, Optional

class AgentAction(BaseModel):
    reasoning: str = Field(description="A brief explanation of why this action is selected")
    action_type: Literal['click', 'type', 'scroll', 'wait', 'finish', 'fail', 'extract', 'goto']
    element_id: Optional[int] = None
    text_input: Optional[str] = Field(description="The text that needs to be entered. For example, the user's search query. Make sure to fill this field if action_type='type'")
    extracted_content: Optional[str] = Field(description="ONLY use this if action_type='extract'. Return the data you found in JSON format. Example: {'title': 'Python Junior', 'salary': '100 000', 'url': '...'}")
    url: Optional[str] = Field(description="The full URL to navigate to (e.g. 'https://hh.ru'). Use ONLY for action_type='goto'")
    current_phase: Phase = Field(description="The current stage of the task. SEARCHING (finding list), SELECTING (choosing item), VIEWING (reading details), EXTRACTING (saving data), DONE (finished).")