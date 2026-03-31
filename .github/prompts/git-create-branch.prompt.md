---
name: git-create-branch
description: Create a new branch from master with a custom name. Keywords: create branch, feature branch. Use when starting a new feature or branch.
parameters:
- name: branchName
  type: string
  description: The full branch name (e.g., "feature/PROJ-123").
---

# Create Branch

This prompt creates and switches to a new branch named `{{branchName}}` from the master branch. Ensure you're in a Git repository with a 'master' branch.

To execute automatically:

- Use `run_in_terminal` with command `git checkout -b {{branchName}} master`, explanation "Create and switch to the branch from master", goal "Set up the branch", isBackground false, timeout 10000.