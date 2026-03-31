---
name: git-commit
description: Commit staged files with a formatted message. Keywords: commit, commit message. Use after staging files.
parameters:
- name: releaseNumber
  type: string
  description: The release number (e.g., "v1.2.3") for the commit message.
- name: ticketNumber
  type: string
  description: The ticket number (e.g., "PROJ-123") for the commit message.
---

# Commit Files

This prompt commits the staged files with a message in the format `{{releaseNumber}}/{{ticketNumber}}`.

To execute automatically:

- Use `run_in_terminal` with command `git commit -m "{{releaseNumber}}/{{ticketNumber}}"`, explanation "Commit the staged files with the formatted message", goal "Commit changes", isBackground false, timeout 10000.