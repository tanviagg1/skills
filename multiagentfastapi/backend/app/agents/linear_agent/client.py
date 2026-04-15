import httpx
from app.config import settings

LINEAR_API_URL = "https://api.linear.app/graphql"


class LinearClient:
    def __init__(self):
        self.headers = {
            "Authorization": settings.linear_api_key,
            "Content-Type": "application/json",
        }

    async def _query(self, query: str, variables: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                LINEAR_API_URL,
                json={"query": query, "variables": variables or {}},
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_teams(self) -> list[dict]:
        query = """
        query {
            teams {
                nodes { id name }
            }
        }
        """
        data = await self._query(query)
        return data["data"]["teams"]["nodes"]

    async def create_project(self, name: str, description: str, team_id: str) -> dict:
        query = """
        mutation CreateProject($name: String!, $description: String, $teamIds: [String!]!) {
            projectCreate(input: {
                name: $name,
                description: $description,
                teamIds: $teamIds
            }) {
                success
                project { id name url }
            }
        }
        """
        data = await self._query(query, {
            "name": name,
            "description": description,
            "teamIds": [team_id],
        })
        return data["data"]["projectCreate"]["project"]

    async def create_issue(
        self,
        title: str,
        description: str,
        team_id: str,
        project_id: str,
        priority: int = 0,
        estimate: int = None,
    ) -> dict:
        query = """
        mutation CreateIssue(
            $title: String!,
            $description: String,
            $teamId: String!,
            $projectId: String,
            $priority: Int,
            $estimate: Int
        ) {
            issueCreate(input: {
                title: $title,
                description: $description,
                teamId: $teamId,
                projectId: $projectId,
                priority: $priority,
                estimate: $estimate
            }) {
                success
                issue { id title url }
            }
        }
        """
        variables = {
            "title": title,
            "description": description,
            "teamId": team_id,
            "projectId": project_id,
            "priority": priority,
        }
        if estimate is not None:
            variables["estimate"] = estimate

        data = await self._query(query, variables)
        return data["data"]["issueCreate"]["issue"]
