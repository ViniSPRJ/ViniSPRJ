#!/usr/bin/env python3
"""web_agent.py
A command-line tool that spins up a LangChain agent capable of:
1. Searching the web (DuckDuckGo)
2. Scraping webpage content (requests + BeautifulSoup)
3. Executing Python code when helpful (Python REPL Tool)

The agent can answer arbitrary questions that may require live web data.

Prerequisites (see requirements.txt):
  pip install -r requirements.txt
  playwright install  # if you want to enable JS-rendered page scraping

Environment variables:
  OPENAI_API_KEY – required for ChatOpenAI

Run:
  python web_agent.py
"""
from __future__ import annotations

import sys

import requests
from bs4 import BeautifulSoup

from langchain.agents import AgentType, initialize_agent  # type: ignore
from langchain.chat_models import ChatOpenAI  # type: ignore
from langchain.tools import Tool  # type: ignore
from langchain.utilities import PythonREPL  # type: ignore

try:
    # DuckDuckGo search wrapper lives in the community package
    from langchain_community.tools import DuckDuckGoSearchRun  # type: ignore
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "DuckDuckGoSearchRun not available. Did you install langchain_community?\n"
        "pip install langchain langchain_community"
    ) from e


def scrape_website(url: str, max_chars: int = 4000) -> str:  # noqa: D401
    """Scrape *visible* text from the given URL and return at most ``max_chars`` characters.

    The function performs a simple GET request (no JS execution). For JS-heavy
    sites consider using Playwright for a full browser render.
    """
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as exc:  # pylint: disable=broad-except
        return f"Error fetching {url}: {exc}"

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove script/style tags
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = " ".join(soup.stripped_strings)
    # Truncate to avoid excessively long outputs (agents have context limits)
    return text[:max_chars]


def build_tools() -> list[Tool]:
    """Create and return the list of tools available to the agent."""
    # 1) Web Search
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="Web Search",
        func=search.run,
        description=(
            "Useful for answering questions about current events or topics "
            "on the internet. Input should be a search query."
        ),
    )

    # 2) Web Scraper
    scrape_tool = Tool(
        name="Scrape Website",
        func=scrape_website,
        description=(
            "Use this to scrape the visible text from a webpage. "
            "Input must be a valid URL, and the output will be raw text."
        ),
    )

    # 3) Python REPL – allows the agent to run code for computation or parsing
    python_tool = PythonREPL().to_tool()

    return [search_tool, scrape_tool, python_tool]


def create_agent(model_name: str = "gpt-3.5-turbo", temperature: float = 0.0):
    """Instantiate and return a LangChain agent executor."""
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    tools = build_tools()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent


def run_cli():  # noqa: D401
    """Simple REPL so a user can interact with the agent via the terminal."""
    agent = create_agent()
    print("\n🤖 Web Agent ready! Ask anything (type 'exit' to quit).\n")

    for line in sys.stdin:
        query = line.strip()
        if not query:
            continue
        if query.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        try:
            response = agent.run(query)
            print(f"\n📝 Answer: {response}\n")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error: {exc}")
            continue
        print("Ask another question or 'exit' ➜ ", end="", flush=True)


if __name__ == "__main__":
    run_cli()