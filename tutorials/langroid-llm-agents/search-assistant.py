"""
2-Agent system where:
- Assistant takes user's (complex) question, breaks it down into smaller pieces
    if needed
- WebSearcher takes Assistant's question, uses the Search tool to search the web
    (using DuckDuckGo), and returns a coherent answer to the Assistant.

Once the Assistant thinks it has enough info to answer the user's question, it
says DONE and presents the answer to the user.

Run like this:

python3 search-assistant.py

To run with a different Groq-hosted LLM, you can pass in the LLM via the MODEL env var:

MODEL=groq/<another_model> python3 search-assistant.py
"""

from dotenv import load_dotenv
from rich import print
from rich.prompt import Prompt
from fire import Fire
import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.duckduckgo_search_tool import DuckduckgoSearchTool

# can pass in this env var at the command line
MODEL = "groq/llama3-70b-8192"

def main() -> None:
    print(
        """
        [blue]Welcome to the Web Search Assistant chatbot!
        I will try to answer your complex questions. 
        
        Enter x or q to quit at any point.
        """
    )
    load_dotenv()

    llm_config = lm.OpenAIGPTConfig(
        chat_model=MODEL,  # or lr.OpenAIChatModel.GPT4_TURBO
        chat_context_length=8192,
        temperature=0,
        max_output_tokens=200,
        timeout=45,
    )

    assistant_config = lr.ChatAgentConfig(
        system_message="""
        You are a resourceful assistant, able to think step by step to answer
        complex questions from the user. You must break down complex questions into
        simpler questions that can be answered by a web search. You must ask me 
        (the user) each question ONE BY ONE, and I will do a web search and send you
        a brief answer. Once you have enough information to answer my original
        (complex) question, you MUST say DONE and present the answer to me.
        """,
        llm=llm_config,
        vecdb=None,
    )
    assistant_agent = lr.ChatAgent(assistant_config)
    search_tool_handler_method = DuckduckgoSearchTool.default_value("request")

    search_agent_config = lr.ChatAgentConfig(
        llm=llm_config,
        vecdb=None,
        system_message=f"""
        You are a web-searcher. For any question you get, you must use the
        `{search_tool_handler_method}` tool/function-call to get up to 5 results.
        I WILL SEND YOU THE RESULTS; DO NOT MAKE UP THE RESULTS!!
        Once you receive the results, you must compose a CONCISE answer 
        based on the search results and say DONE and show the answer to me,
        in this format:
        DONE [... your CONCISE answer here ...]
        IMPORTANT: YOU MUST WAIT FOR ME TO SEND YOU THE 
        SEARCH RESULTS BEFORE saying you're DONE.
        """,
    )
    search_agent = lr.ChatAgent(search_agent_config)
    search_agent.enable_message(DuckduckgoSearchTool)

    assistant_task = lr.Task(
        assistant_agent,
        name="Assistant",
        llm_delegate=True,
        single_round=False,
        interactive=False,
    )
    search_task = lr.Task(
        search_agent,
        name="Searcher",
        llm_delegate=True,
        single_round=False,
        interactive=False,
    )
    assistant_task.add_sub_task(search_task)
    question = Prompt.ask("What do you want to know?")
    assistant_task.run(question)


if __name__ == "__main__":
    Fire(main)
