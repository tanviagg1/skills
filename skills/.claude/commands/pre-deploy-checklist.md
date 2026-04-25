Run through a pre-deployment checklist before I push to production.

Follow these steps:

1. Run `git status` and `git log main..HEAD --oneline` to understand what is being deployed.

2. Check each item and report PASS, FAIL, or SKIP with a reason:

   **Code**
   - [ ] No console.log / print / debug statements left in changed files
   - [ ] No hardcoded secrets, API keys, or passwords
   - [ ] Linter passes on changed files
   - [ ] Tests pass (ask me to run them if unsure)

   **Dependencies**
   - [ ] No new dependencies with known vulnerabilities
   - [ ] Lock file (package-lock.json / yarn.lock / poetry.lock) is committed

   **Database**
   - [ ] Any new migrations are included and tested
   - [ ] No destructive migrations (DROP, DELETE) without a rollback plan

   **Configuration**
   - [ ] All new environment variables are documented
   - [ ] Feature flags are set correctly for production

   **Docs**
   - [ ] README or docs updated if behaviour changed

3. Give a go / no-go recommendation with a list of any blockers.
