---
name: skills-project
description: Context about the skills Spring Boot project — structure, stack, endpoints, and conventions
type: project
---

## Project: skills

**Local path:** /Users/tanviagarwal/Documents/Projects/skills
**Remote:** https://github.com/tanviagg1/test.git
**Active branch:** basic-claude-skills

## Stack
- Java 21
- Spring Boot 4.0.2
- Gradle build system
- No database — mock data loaded from JSON file

## Structure
```
src/main/java/com/skills/
  SkillsApplication.java          — entry point
  controller/CustomerController   — REST endpoints
  service/CustomerService         — business logic
  backend/CustomerBackendClient   — data access (mock)
  model/Customer.java             — record with 8 fields

src/main/resources/
  mock-customers.json             — mock customer data (edit to add/change records)

.claude/commands/                 — 15 Claude Code slash command skills
```

## API
- `GET /customers/{cardNumber}` — returns a Customer JSON or 404

## Mock customers (in mock-customers.json)
| Card Number | Name | Status |
|---|---|---|
| 4111111111111111 | Alice Johnson | ACTIVE |
| 5500005555555559 | Bob Martinez | ACTIVE |
| 3714496353984311 | Carol Smith | SUSPENDED |

## Run
```bash
cd /Users/tanviagarwal/Documents/Projects/skills
gradle bootRun
# App runs on http://localhost:8080
```

## Claude Code Skills
15 slash command skills stored in .claude/commands/:
bitbucket-pr, changelog, code-review, debug, document-function,
explain-file, incident, lint-fix, pr-description, pre-deploy-checklist,
readme-update, standup, ticket, trace-feature, write-tests

**Why:** Project was originally named "skill", renamed to "skills" locally. Mock data was moved from hardcoded Java Map to mock-customers.json for easier editing.
**How to apply:** When user asks to add customers or change data, edit mock-customers.json. When user asks to run the app, use `gradle bootRun` from the skills directory.
