from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from .tools import arxiv_search_tool, google_search_tool

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-flash",
    api_key=api_key,
)

google_search_agent = AssistantAgent(
    name="Google_Search_Agent",
    tools=[google_search_tool],
    model_client=model_client,
    description="An agent that can search Google for information, returns results with a snippet and body content",
    system_message="You are a helpful AI assistant. Solve tasks using your tools.",
)

arxiv_search_agent = AssistantAgent(
    name="Arxiv_Search_Agent",
    tools=[arxiv_search_tool],
    model_client=model_client,
    description="An agent that can search Arxiv for papers related to a given topic, including abstracts",
    system_message="You are a helpful AI assistant. Solve tasks using your tools. Specifically, you can take into consideration the user's request and craft a search query that is most likely to return relevant academi papers.",
)


report_agent = AssistantAgent(
    name="Report_Agent",
    model_client=model_client,
    description="Generate a report based on a given topic",
    system_message="You are a helpful assistant. Your task is to synthesize data extracted into a high quality literature review including CORRECT references. You MUST write a final report that is formatted as a literature review with CORRECT references.  Your response should end with the word 'TERMINATE'",
)
