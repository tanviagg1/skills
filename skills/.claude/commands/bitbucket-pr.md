Guide me through committing my changes and raising a pull request on Bitbucket.

Follow these steps in order:

1. Run `git status` to show me what files have changed.

2. Ask me which files I want to include in this commit.

3. Stage the selected files with `git add`.

4. Ask me to describe what this change does in plain English, then generate a commit message in this format:
   <type>(<scope>): <short summary>

   Types: feat, fix, docs, refactor, test, chore
   Keep the first line under 72 characters.
   Add a short body if the change needs context.

5. Commit with the generated message.

6. Ask me which branch I want to merge into (default: main).

7. Push the branch to origin.

8. Show me the Bitbucket pull request URL to open in my browser:
   https://bitbucket.org/<workspace>/<repo>/pull-requests/new?source=<branch>&dest=<target>

   If you don't know the workspace or repo name, read it from `git remote get-url origin`.

9. Suggest a clear PR title and description I can paste into Bitbucket, including:
   - What changed and why
   - How to test it
   - Any notes for the reviewer
