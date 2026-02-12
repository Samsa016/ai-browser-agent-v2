from pydantic import Field, BaseModel
from typing import Literal, Optional

class AgentAction(BaseModel):
    reasoning: str = Field(description="A brief explanation of why this action is selected")
    action_type: Literal['click', 'type', 'scroll', 'wait', 'finish', 'fail']
    element_id: Optional[int] = None
    text_input: Optional[str] = Field(description="The text that needs to be entered. For example, the user's search query. Make sure to fill this field if action_type='type'")