from github import Github
from app.config import settings


class GitHubClient:
    def __init__(self):
        self.client = Github(settings.github_token)

    def parse_repo_url(self, url: str) -> str:
        """Extract owner/repo from a GitHub URL."""
        url = url.rstrip("/")
        if "github.com/" in url:
            parts = url.split("github.com/")[-1].split("/")
            return f"{parts[0]}/{parts[1]}"
        return url

    def get_repo_tree(self, repo_url: str, max_depth: int = 3) -> list[dict]:
        """Get the file tree of a repository."""
        repo_path = self.parse_repo_url(repo_url)
        repo = self.client.get_repo(repo_path)
        tree = repo.get_git_tree(sha="HEAD", recursive=True).tree

        IGNORE = {
            "node_modules", ".git", "dist", "build", "__pycache__",
            ".next", "coverage", ".venv", "venv", "env"
        }

        files = []
        for item in tree:
            parts = item.path.split("/")
            if any(p in IGNORE for p in parts):
                continue
            if item.type == "blob":
                files.append({"path": item.path, "size": item.size})

        return files

    def get_file_content(self, repo_url: str, path: str) -> str:
        """Get the content of a specific file."""
        repo_path = self.parse_repo_url(repo_url)
        repo = self.client.get_repo(repo_path)
        try:
            content = repo.get_contents(path)
            return content.decoded_content.decode("utf-8", errors="ignore")
        except Exception:
            return ""

    def get_repo_info(self, repo_url: str) -> dict:
        """Get basic repo metadata."""
        repo_path = self.parse_repo_url(repo_url)
        repo = self.client.get_repo(repo_path)
        return {
            "name": repo.name,
            "description": repo.description,
            "language": repo.language,
            "stars": repo.stargazers_count,
        }
