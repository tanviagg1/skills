# Project: skills

Spring Boot REST API for customer lookup by card number.

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

## Mock customers
Edit `src/main/resources/mock-customers.json` to add or change records.

| Card Number | Name | Status |
|---|---|---|
| 4111111111111111 | Alice Johnson | ACTIVE |
| 5500005555555559 | Bob Martinez | ACTIVE |
| 3714496353984311 | Carol Smith | SUSPENDED |

## Run
```bash
gradle bootRun
# App runs on http://localhost:8080
```

## Claude Code Skills
15 slash command skills in `.claude/commands/`:
`/bitbucket-pr`, `/changelog`, `/code-review`, `/debug`, `/document-function`,
`/explain-file`, `/incident`, `/lint-fix`, `/pr-description`, `/pre-deploy-checklist`,
`/readme-update`, `/standup`, `/ticket`, `/trace-feature`, `/write-tests`
