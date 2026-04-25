Review my staged or recently changed code before I commit.

Follow these steps:

1. Run `git diff --staged` to see staged changes. If nothing is staged, run `git diff` for unstaged changes.

2. Review the diff and flag any of the following:
   - Bugs or logic errors
   - Security issues (hardcoded secrets, SQL injection, XSS, etc.)
   - Missing error handling
   - Dead code or unused variables
   - Functions that are too long or doing too much
   - Naming that is unclear

3. Rate overall quality: Good / Needs Minor Changes / Needs Major Changes

4. List issues as a numbered checklist with file name and line number where possible.

5. Ask if I want you to fix any of the flagged issues.
