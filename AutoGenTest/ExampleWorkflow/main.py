import asyncio

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from .agents import arxiv_search_agent, google_search_agent, model_client, report_agent


async def main() -> None:
    """
    Run the round-robin group chat to draft a literature review on no-code tools
    for building multi-agent AI systems. The run terminates when a message
    contains the token "TERMINATE".
    """
    termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat(
        participants=[google_search_agent, arxiv_search_agent, report_agent],
        termination_condition=termination,
    )

    await Console(
        team.run_stream(
            task="Write a literature review on no code tools for building multi agent ai systems",
        )
    )

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
    
# python -m ExampleWorkflow.main