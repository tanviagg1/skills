import re
from pathlib import Path
from groq import Groq
from .analyzer import RepoAnalyzer
from app.config import settings

PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "github.md"


class GitHubAgent:
    def __init__(self):
        self.analyzer = RepoAnalyzer()
        self.client = Groq(api_key=settings.groq_api_key)
        self.system_prompt = PROMPT_PATH.read_text()

    async def run(self, repo_url: str, send_event) -> str:
        await send_event({"type": "status", "message": "Fetching repository structure..."})

        try:
            context = self.analyzer.analyze(repo_url)
        except Exception as e:
            await send_event({"type": "error", "message": f"Could not access repo: {str(e)}"})
            return ""

        await send_event({"type": "status", "message": f"Analysing {len(context['key_files'])} key files..."})

        prompt = self._build_prompt(context)

        await send_event({"type": "status", "message": "Generating sequence diagram..."})

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        result = response.choices[0].message.content or ""

        diagram = self._extract_mermaid(result)
        summary = self._extract_summary(result)

        if diagram:
            await send_event({"type": "diagram", "content": diagram})

        return summary or result

    def _build_prompt(self, context: dict) -> str:
        repo = context["repo_info"]
        tree_str = "\n".join(context["file_tree"])

        files_str = ""
        for path, content in context["key_files"].items():
            files_str += f"\n\n### {path}\n```\n{content}\n```"

        return f"""
Repository: {repo['name']}
Description: {repo.get('description', 'N/A')}
Primary Language: {repo.get('language', 'N/A')}

File Tree:
{tree_str}

Key File Contents:
{files_str}
"""

    def _extract_mermaid(self, text: str) -> str:
        match = re.search(r"```mermaid\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_summary(self, text: str) -> str:
        match = re.search(r"\*\*Summary:\*\*\s*(.*)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
