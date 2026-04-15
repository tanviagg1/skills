from .client import GitHubClient

ENTRY_POINTS = [
    "main.py", "app.py", "server.py", "index.ts", "index.js",
    "src/index.ts", "src/index.js", "src/main.ts", "src/main.js",
    "cmd/main.go", "main.go",
]

IMPORTANT_PATTERNS = [
    "router", "route", "controller", "service", "handler",
    "model", "schema", "middleware", "api", "views",
]

MAX_FILE_CHARS = 3000


class RepoAnalyzer:
    def __init__(self):
        self.client = GitHubClient()

    def analyze(self, repo_url: str) -> dict:
        """Analyze a repo and return structured context for diagram generation."""
        info = self.client.get_repo_info(repo_url)
        tree = self.client.get_repo_tree(repo_url)

        all_paths = [f["path"] for f in tree]

        # Pick key files to read
        key_files = self._pick_key_files(all_paths)

        file_contents = {}
        for path in key_files[:10]:  # limit to 10 files
            content = self.client.get_file_content(repo_url, path)
            if content:
                file_contents[path] = content[:MAX_FILE_CHARS]

        return {
            "repo_info": info,
            "file_tree": all_paths[:100],  # first 100 paths
            "key_files": file_contents,
        }

    def _pick_key_files(self, paths: list[str]) -> list[str]:
        """Score and rank files by architectural importance."""
        scored = []
        for path in paths:
            score = 0
            name = path.lower()

            # Entry points get highest score
            if any(path.endswith(ep) or path == ep for ep in ENTRY_POINTS):
                score += 10

            # Important pattern matches
            for pattern in IMPORTANT_PATTERNS:
                if pattern in name:
                    score += 3

            # Prefer files closer to root
            depth = path.count("/")
            score -= depth

            # Skip test files, lock files, configs
            if any(x in name for x in ["test", "spec", "lock", ".min.", "vendor"]):
                score -= 5

            scored.append((score, path))

        scored.sort(reverse=True)
        return [path for _, path in scored]
