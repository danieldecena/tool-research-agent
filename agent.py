import asyncio
import urllib.request
import urllib.parse
import re

from google.antigravity import LocalAgentConfig, CapabilitiesConfig
from google.antigravity.utils.interactive import run_interactive_loop

def search_web(query: str) -> str:
    """Searches the web for information about tools, documentation, and best practices.
    Returns snippets from the top search results.
    """
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Extract basic snippet text from DuckDuckGo results
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
            clean_snippets = [re.sub(r'<[^>]+>', '', s).strip() for s in snippets]
            if not clean_snippets:
                return "No results found."
            return "\n\n".join(f"Result {i+1}:\n{snippet}" for i, snippet in enumerate(clean_snippets[:5]))
    except Exception as e:
        return f"Search failed: {str(e)}"

SYSTEM_PROMPT = """
You are a Staff Solutions Architect and Codebase Researcher. 
Your goal is to help developers find the best tools, libraries, and architectural solutions for their projects.

When the user asks for a solution or tool recommendation:
1. Use your built-in capabilities to explore their codebase (e.g. read files, list directories, check package.json or requirements.txt) to understand their current stack and constraints.
2. Use the `search_web` tool to find modern best practices, alternatives, and community consensus on tools.
3. Synthesize your findings and provide a concrete recommendation with pros, cons, and a brief setup plan.
"""

async def main():
    config = LocalAgentConfig(
        system_instructions=SYSTEM_PROMPT.strip(),
        # Enable built-in tools (view_file, run_command, etc.) so it can read the codebase
        capabilities=CapabilitiesConfig(),
        # Add our custom web search tool
        tools=[search_web],
    )
    
    print("🤖 Codebase & Web Tool Research Agent initialized.")
    print("You can ask me to evaluate tools or recommend solutions based on your project.")
    print("Type your questions below. (Press Ctrl+C to exit)\n")
    
    await run_interactive_loop(config)

if __name__ == "__main__":
    asyncio.run(main())
