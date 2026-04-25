Trace how a feature flows through the codebase end to end.

Follow these steps:

1. Ask me which feature or user action to trace (e.g. "user login", "submit order", "file upload").

2. Find the entry point — the route, event handler, or function where the feature starts. Search for it in the codebase.

3. Follow the call chain step by step:
   - What function is called first
   - What it does and what it calls next
   - Where data is read from or written to (database, cache, API)
   - Where the response or output is returned

4. Draw a simple linear flow:
   Request → handler → service → repository → database → response

5. Highlight any branching logic, error paths, or places where the flow is non-obvious.

6. Ask if I want to go deeper into any specific step.
