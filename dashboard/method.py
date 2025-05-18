from typing import List

from shared.utils import graph_data
from core.ai.prompts import PROMPT_GENERATE_INSIGHT
from core.ai.promt_manager import PromptManager

def generate_insight(data : List[graph_data]):
    pm = PromptManager()
    pm.add_system_message(PROMPT_GENERATE_INSIGHT)
    pm.add_message_with_images(
        "analyze this graphs and provide insights about the trends, anomalies, and inflection points in the data.",
        data
    )
    result = pm.generate()
    return result
