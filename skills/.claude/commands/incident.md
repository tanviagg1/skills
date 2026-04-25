Help me respond to a production incident in a structured way.

Follow these steps:

1. Ask me: What is broken? When did it start? Who reported it?

2. Help me gather information:
   - What errors are showing in logs (ask me to paste them)
   - What changed recently: run `git log --oneline -10`
   - Is this affecting all users or a subset?

3. Identify the most likely cause based on the information gathered.

4. Suggest an immediate mitigation (rollback, feature flag off, restart, etc.).

5. Once resolved, draft a postmortem with:

   **Incident Summary**
   - What broke, when, and how long it lasted

   **Timeline**
   - Key events from detection to resolution

   **Root Cause**
   - What actually caused the issue

   **Fix Applied**
   - What was done to resolve it

   **Prevention**
   - What to do so this doesn't happen again (checklist items, monitoring, tests)
