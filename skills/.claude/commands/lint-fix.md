Run the linter, explain each error, and fix them.

Follow these steps:

1. Detect the linter from package.json or config files (ESLint, Prettier, Flake8, Ruff, etc.).

2. Run the linter on changed files: `git diff --name-only HEAD` to find them.

3. For each error or warning:
   - Show the file and line number
   - Explain what the rule means in plain English
   - Fix it

4. After all fixes, run the linter again to confirm zero errors.

5. Summarize what was fixed.
