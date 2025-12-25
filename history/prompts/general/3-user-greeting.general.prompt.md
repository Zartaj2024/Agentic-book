---
id: 3
title: User greeting
stage: general
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: hi
labels: ["greeting"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- history/prompts/general/3-user-greeting.general.prompt.md
tests:

---

## Prompt

hi

## Response snapshot

Hello! How can I assist you today?

## Outcome

- ✅ Impact: minimal
- 🧪 Tests: N/A
- 📁 Files: N/A
- 🔁 Next prompts: user's next request
- 🧠 Reflection: User initiated a conversation with a greeting.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Respond with a friendly greeting and ask how I can help.
