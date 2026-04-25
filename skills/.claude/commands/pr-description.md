Generate a pull request title and description from my current branch changes.

Follow these steps:

1. Run `git log main..HEAD --oneline` to see commits on this branch.
2. Run `git diff main..HEAD --stat` to see files changed.
3. Read the most important changed files to understand the context.

4. Generate:

**Title:** Short, imperative, under 70 characters.

**Description:**
## What changed
- Bullet points of what was added, changed, or removed.

## Why
- The reason or problem this solves.

## How to test
- Step-by-step instructions to verify the change works.

## Notes for reviewer
- Anything tricky, decisions made, or areas to pay attention to.

5. Ask if I want to adjust the tone or add anything.
