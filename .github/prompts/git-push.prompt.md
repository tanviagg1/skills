---
name: git-push
description: Push the current branch to the remote repository. Keywords: push, push branch. Use after committing changes.
parameters:
- name: ticketNumber
  type: string
  description: The ticket number (e.g., "PROJ-123") for the branch name to push.
---

# Push Branch

This prompt pushes the feature branch `feature/{{ticketNumber}}` to the remote repository.

To execute automatically:

- Use `run_in_terminal` with command `git push origin feature/{{ticketNumber}}`, explanation "Push the branch to the remote repository", goal "Push changes", isBackground false, timeout 15000.

## Verification Tests (manual run by ChatGPT)

Add tests for prompt validation and workflow correctness:

- Use `run_in_terminal` with command `git branch --show-current`, explanation "Check current branch", goal "Verify branch", isBackground false, timeout 5000.
- Use `run_in_terminal` with command `git status --porcelain`, explanation "Check working tree cleanliness", goal "Verify status", isBackground false, timeout 5000.
- Use `run_in_terminal` with command `git log -1 --oneline`, explanation "Show last commit", goal "Verify commit", isBackground false, timeout 5000.
- Use `run_in_terminal` with command `git ls-remote --heads origin "$(git branch --show-current)"`, explanation "Verify remote branch exists", goal "Verify remote push", isBackground false, timeout 15000.