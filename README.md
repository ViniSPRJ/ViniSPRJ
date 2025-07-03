- Learning forever
- 👋 Hi, I'm @ViniSPRJ
- 👀 I'm interested in ... learning
- 🌱 I'm currently learning ...Code, AI
- 💞️ I'm looking to collaborate on ...
- 📫 How to reach me ...never
- 😄 Pronouns: ...
- ⚡ Fun fact: ...

<!---
ViniSPRJ/ViniSPRJ is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

# Web Agent (LangChain)

This repository contains a simple command-line agent that can:

1. Search the web (DuckDuckGo)
2. Scrape website content
3. Execute Python for on-the-fly computation
4. Combine the above using an LLM (OpenAI Chat)

---

## Setup

1. **Clone / download** this repository.
2. **Install dependencies**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   # For full-page JS rendering (optional)
   playwright install
   ```

3. **Environment variables**:

   * `OPENAI_API_KEY` – required for ChatGPT-style completions.
   * (`SERPAPI_API_KEY` is **NOT** needed because we use DuckDuckGo.)

   You can place variables in a `.env` file at the project root:

   ```env
   OPENAI_API_KEY=sk-...
   ```

---

## Running the Agent

```bash
python web_agent.py
```

You will see:

```
🤖 Web Agent ready! Ask anything (type 'exit' to quit).
```

Type your question, for example:

```
Who won the Nobel Prize in Physics in 2023 and why?
```

The agent will:

1. Issue a DuckDuckGo search to gather up-to-date links.
2. Optionally scrape relevant pages for details.
3. Use the LLM to craft a concise answer.

---

## Extending

* **Add new tools** – create a function and wrap it with `langchain.tools.Tool`.
* **Swap the LLM** – change `model_name` in `create_agent()`.
* **Change agent type** – experiment with `AgentType` in `initialize_agent`.

---

## License

MIT
