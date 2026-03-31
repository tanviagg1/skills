---
name: git-feature-branch
description: Create a feature branch from master, connect to GitHub repo (https://github.com/tanviagg1/test.git), add/commit files with formatted message, rebase master (resolving conflicts), and push. Keywords: add, commit, push, rebase, feature branch. Use for feature development workflows.
parameters:
- name: ticketNumber
  type: string
  description: The ticket number (e.g., "PROJ-123") for the branch name and commit message.
- name: releaseNumber
  type: string
  description: The release number (e.g., "v1.2.3") for the commit message format.
---

# Git Feature Branch Workflow

This prompt automates connecting to the GitHub repo (https://github.com/tanviagg1/test.git), creating a feature branch, staging/committing changes with a standardized message, rebasing master, and pushing. Ensure you're in a Git repository with a 'master' branch.

## Steps:
1. **Set remote origin**: Connect to the GitHub repo if not already set.
2. **Create feature branch**: Switch to a new branch named `feature/{{ticketNumber}}` from master.
3. **Add all files**: Stage all changes.
4. **Commit with formatted message**: Commit using the format `{{releaseNumber}}/{{ticketNumber}}`.
5. **Rebase master**: Pull latest master changes and rebase onto your branch. Resolve any conflicts manually if they occur.
6. **Push branch**: Push the rebased branch to remote.

To execute automatically, use the following tool calls in sequence:

- Set remote: Use `run_in_terminal` with command `git remote get-url origin >/dev/null 2>&1 || git remote add origin https://github.com/tanviagg1/test.git`, explanation "Check if remote origin is set; if not, add it to connect to the GitHub repo", goal "Connect to GitHub repo", isBackground false, timeout 5000.
- Create branch: Use `run_in_terminal` with command `git checkout -b feature/{{ticketNumber}} master`, explanation "Create and switch to the feature branch from master", goal "Set up the feature branch", isBackground false, timeout 10000.
- Add files: Use `run_in_terminal` with command `git add .`, explanation "Stage all files for commit", goal "Add all changes", isBackground false, timeout 5000.
- Commit: Use `run_in_terminal` with command `git commit -m "{{releaseNumber}}/{{ticketNumber}}"`, explanation "Commit the staged files with the formatted message", goal "Commit changes", isBackground false, timeout 10000.
- Rebase: Use `run_in_terminal` with command `git rebase master`, explanation "Rebase the current branch onto master", goal "Merge latest master changes", isBackground false, timeout 30000. (Note: If conflicts occur, resolve manually and continue rebase.)
- Push: Use `run_in_terminal` with command `git push origin feature/{{ticketNumber}}`, explanation "Push the branch to the remote repository", goal "Push changes", isBackground false, timeout 15000.

If rebase fails due to conflicts, abort with `git rebase --abort`, resolve manually, then restart rebase or commit again.