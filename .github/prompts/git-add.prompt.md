---
name: git-add
description: Stage all files for commit. Keywords: add, stage files. Use when preparing changes for commit.
parameters: []
---

# Add Files

This prompt stages all files in the working directory for the next commit.

To execute automatically:

- Use `run_in_terminal` with command `git add .`, explanation "Stage all files for commit", goal "Add all changes", isBackground false, timeout 5000.