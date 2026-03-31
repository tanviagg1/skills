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