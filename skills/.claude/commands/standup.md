Summarize my recent commits into a standup update.

Follow these steps:

1. Run `git log --since="yesterday" --author="$(git config user.name)" --oneline` to get my commits from the last day.

2. If it is Monday, use `git log --since="3 days ago"` to cover the weekend.

3. Group the commits into plain-English bullet points. Do not use raw commit messages — translate them into what was actually accomplished.

4. Format the standup as:

   **Yesterday**
   - What I worked on and completed

   **Today**
   - Ask me what I plan to work on today

   **Blockers**
   - Ask me if I have any blockers

5. Keep it concise — each bullet should be one sentence.
