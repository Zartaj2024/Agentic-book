---
id: 1
title: course-content-specification
stage: spec
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-course-content-specification
branch: 1-course-content-specification
user: Claude User
command: /sp.specify
labels: [specification,education,course-content]
links:
  spec: specs/1-course-content-specification/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-course-content-specification/spec.md
 - specs/1-course-content-specification/checklists/requirements.md
 - spec/chapters/kinematics-01.yaml
tests:
 - null
---

## Prompt

Learning Outcomes (by module)

Provide measurable learning outcomes for each chapter. Example (Chapter 1 — Kinematics):

LO1: Derive forward kinematics for a serial manipulator.

LO2: Implement forward kinematics in Python and validate with simulation.

Content Format Requirements

Each chapter: Overview, Theory, Worked Examples, Lab Exercises, Code Examples, Project, Quiz (MCQs), Further Reading, Instructor Notes.

Code examples: runnable, containerized (Docker), ROS2-native where applicable, with unit tests.

Diagrams: high-quality SVGs; include both source (e.g., draw.io/Diagrams.net or Figma export) and optimized web assets.

Metadata & Specification Schema (SpecifyPlus)

Create machine-readable spec for each chapter including:

chapter_id: string
title: string
prereqs: [chapter_id]
estimated_hours: number
learning_outcomes: [string]
assessments: {type: ["lab","quiz","project"], weight: number}
resources: {code_repo: url, datasets: [url]}

Store specs in spec/chapters/*.yaml and render a syllabus page o

## Response snapshot

Created a comprehensive feature specification for course content creation that includes:

1. Defined measurable learning outcomes format (LO1, LO2, etc.)
2. Specified required chapter sections (Overview, Theory, Worked Examples, Lab Exercises, Code Examples, Project, Quiz, Further Reading, Instructor Notes)
3. Required machine-readable YAML specifications for chapters
4. Specified containerized code examples with unit tests
5. Required high-quality SVG diagrams with source files
6. Created sample YAML specification file
7. Created quality checklist for the specification

## Outcome

- ✅ Impact: Created complete specification for educational content creation system
- 🧪 Tests: No tests needed for specification
- 📁 Files: Created spec.md, requirements checklist, and sample YAML
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Specification addresses all requirements from user input

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Plan the implementation