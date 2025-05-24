import logging
from datetime import datetime

from agents import function_tool, Runner, Agent

from core.ai.chromadb import chroma, openai_ef
from core.ai.prompts import AGENT_INSTRUCTIONS
from shared.utils import parse_date_string, date_to_timestamp

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Configure as needed


@function_tool(
    name_override="get_daily_report_tool",
    description_override="get report based on date input and type of report",
)
def get_report_tool(start_date: str, end_date: str, report_type: str, msg: str):
    """
    Fetches reports from the ChromaDB collection.

    Args:
        start_date: Start date in 'YYYY-MM-DD' format.
        end_date: End date in 'YYYY-MM-DD' format.
        report_type: Type of report to fetch. Can be 'daily' or 'weekly' or 'monthly'
        msg: User's question to answer
    Returns:
        ChromaDB query results or an error message string.
    """
    logger.info(
        f"get_report_tool called with context: {start_date}, {end_date}, {report_type}, {msg}"
    )
    query_from_timestamp = parse_date_string(start_date)
    query_to_timestamp = parse_date_string(end_date)

    date_overlap_conditions = [
        {"from_date_timestamp": {"$lte": date_to_timestamp(query_to_timestamp)}},
        {"to_date_timestamp": {"$gte": date_to_timestamp(query_from_timestamp)}},
    ]
    type_condition = {"dashboard": {"$eq": report_type}}
    final_filter = {"$and": date_overlap_conditions + [type_condition]}

    collection = chroma.get_collection(name="dashboard", embedding_function=openai_ef)
    logger.info(f"Querying ChromaDB collection 'dashboard' with filter: {final_filter}")

    content = collection.query(query_texts=[msg], n_results=3, where=final_filter)

    return content


@function_tool(name_override="get_today_date", description_override="get today date")
def get_today_date():
    """
    Fetch today's date from the system clock.
    return: today's date in 'YYYY-MM-DD' format.
    """
    return datetime.today().strftime("%Y-%m-%d")


async def chats(msg: []):
    agent = Agent(
        name="bussiness-analyst agent",
        instructions=AGENT_INSTRUCTIONS,
        tools=[get_report_tool, get_today_date],
        model="gpt-4.1",
    )
    result = await Runner.run(agent, msg)
    return result.final_output
