#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path
from string import Template
from textwrap import dedent

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml")
    print("Install it with: pip install pyyaml")
    sys.exit(1)


ROOT = Path.cwd()


STARTUP_PLAN_SCHEMA = """
topic_id: TOPIC_ID
plan_version: 1
status: planned

source_reading:
  pdf_direct_reading_status: unknown
  extraction_needed: false
  notes: ""

teaching_strategy:
  audience_summary: ""
  explanation_style: ""
  visual_strategy: ""
  code_strategy: ""

proposed_wiki_structure:
  - path: wiki/index.md
    purpose: ""
  - path: wiki/source_map.md
    purpose: ""
  - path: wiki/glossary.md
    purpose: ""
  - path: wiki/open_questions.md
    purpose: ""

proposed_lesson_structure:
  - section_id: section_01
    title: ""
    purpose: ""
    concepts: []
    likely_visuals: []
    likely_code: []

execution_phases:
  - id: phase_01_compile_wiki
    name: "Compile wiki"
    goal: ""
    inputs:
      - topic.yaml
      - raw/
    outputs: []
    instructions: []
    completion_check: []

  - id: phase_02_create_lesson_outline
    name: "Create lesson outline"
    goal: ""
    inputs:
      - wiki/
    outputs: []
    instructions: []
    completion_check: []

  - id: phase_03_expand_sections_with_visuals
    name: "Expand lesson sections with visuals"
    goal: ""
    inputs:
      - wiki/
      - outputs/lesson.md
      - outputs/visual_plan.md
    outputs: []
    instructions: []
    completion_check: []

  - id: phase_04_review
    name: "Review"
    goal: ""
    inputs:
      - prompts/reviewer.md
      - wiki/
      - outputs/
    outputs:
      - reviews/reviewer_report.md
    instructions:
      - Reviewer must not edit source, wiki, lesson, visual, code, or preview files.
    completion_check: []

  - id: phase_05_fix
    name: "Fix validated review findings"
    goal: ""
    inputs:
      - prompts/fixer.md
      - reviews/reviewer_report.md
      - outputs/
    outputs:
      - reviews/fix_log.md
    instructions:
      - Validate reviewer findings before applying fixes.
      - Do not blindly apply reviewer feedback.
    completion_check: []
""".strip()


STARTUP_PROMPT_TEMPLATE = Template(
    """
Use AGENTS.md as global repo guidance.

We are starting a new wheels topic:

topics/$topic/

Read:
- topics/$topic/topic.yaml
- all files under topics/$topic/raw/ that you can access

Task:
Create the topic execution plan.

Create only:

topics/$topic/plan.yaml

The plan should decide the best way to teach this topic to the audience described in topic.yaml.

Important:
- Do not generate the wiki yet.
- Do not generate the lesson yet.
- Do not generate visuals yet.
- Do not modify raw/.
- Follow the explanation quality bar and visual quality bar in AGENTS.md.
- If you cannot reliably read the PDF directly, say so in plan.yaml and recommend the minimum extraction needed.

The plan.yaml MUST use this structure:

$schema

You may add more phases if needed, but keep the schema machine-readable.
"""
)


PHASE_PROMPT_TEMPLATE = Template(
    """
Use AGENTS.md as global repo guidance.

Use the topic configuration and plan:
- topics/$topic/topic.yaml
- topics/$topic/plan.yaml

Run only this phase:

$phase_id — $phase_name

Goal:
$goal

Inputs to use:
$inputs

Expected outputs:
$outputs

Instructions:
$instructions

Completion check:
$completion_check

Rules:
- Do not run later phases.
- Do not modify raw/.
- Stay grounded in the available sources.
- Follow the audience profile in topic.yaml.
- Follow the explanation quality bar and visual quality bar in AGENTS.md.
- If this phase creates or updates visual assets, update preview.html accordingly.
- If this phase is review-only, do not edit source/wiki/output files; only write the review report.
"""
)


def topic_dir(topic: str) -> Path:
    return ROOT / "topics" / topic


def topic_yaml_path(topic: str) -> Path:
    return topic_dir(topic) / "topic.yaml"


def plan_path(topic: str) -> Path:
    return topic_dir(topic) / "plan.yaml"


def state_path(topic: str) -> Path:
    return topic_dir(topic) / ".wheels_state.json"


def load_state(topic: str) -> dict:
    path = state_path(topic)

    if not path.exists():
        return {
            "completed_phases": [],
            "last_prompted_phase": None,
        }

    return json.loads(path.read_text())


def save_state(topic: str, state: dict) -> None:
    state_path(topic).write_text(json.dumps(state, indent=2) + "\n")


def load_plan(topic: str) -> dict:
    path = plan_path(topic)

    if not path.exists():
        return {}

    return yaml.safe_load(path.read_text()) or {}


def yaml_block(value) -> str:
    if value is None:
        return "- none"

    if value == "":
        return "- none"

    rendered = yaml.safe_dump(value, sort_keys=False).strip()

    if not rendered:
        return "- none"

    return rendered


def print_startup_prompt(topic: str) -> None:
    topic_yaml = topic_yaml_path(topic)

    if not topic_yaml.exists():
        print("ERROR: Missing {}".format(topic_yaml))
        sys.exit(1)

    schema = STARTUP_PLAN_SCHEMA.replace("TOPIC_ID", topic)

    prompt = STARTUP_PROMPT_TEMPLATE.substitute(
        topic=topic,
        schema=schema,
    )

    print(dedent(prompt).strip())


def print_phase_prompt(topic: str, phase: dict) -> None:
    phase_id = phase.get("id", "<missing id>")
    phase_name = phase.get("name", "<missing name>")
    goal = phase.get("goal", "")
    inputs = yaml_block(phase.get("inputs", []))
    outputs = yaml_block(phase.get("outputs", []))
    instructions = yaml_block(phase.get("instructions", []))
    completion_check = yaml_block(phase.get("completion_check", []))

    prompt = PHASE_PROMPT_TEMPLATE.substitute(
        topic=topic,
        phase_id=phase_id,
        phase_name=phase_name,
        goal=goal,
        inputs=inputs,
        outputs=outputs,
        instructions=instructions,
        completion_check=completion_check,
    )

    print(dedent(prompt).strip())


def print_next_prompt(topic: str) -> None:
    plan = load_plan(topic)

    if not plan:
        print("No plan.yaml found for topic '{}'.".format(topic))
        print()
        print("Generate the startup prompt first:")
        print()
        print("python scripts/wheels_prompt.py --topic {} --startup".format(topic))
        return

    phases = plan.get("execution_phases", [])

    if not phases:
        print("ERROR: {} has no execution_phases.".format(plan_path(topic)))
        sys.exit(1)

    state = load_state(topic)
    completed = set(state.get("completed_phases", []))

    for phase in phases:
        phase_id = phase.get("id")

        if phase_id not in completed:
            state["last_prompted_phase"] = phase_id
            save_state(topic, state)
            print_phase_prompt(topic, phase)
            return

    print("All phases are marked complete.")


def mark_done(topic: str) -> None:
    state = load_state(topic)
    phase_id = state.get("last_prompted_phase")

    if not phase_id:
        print("No last prompted phase found. Run --next first.")
        return

    completed = state.setdefault("completed_phases", [])

    if phase_id not in completed:
        completed.append(phase_id)

    save_state(topic, state)
    print("Marked complete: {}".format(phase_id))


def print_status(topic: str) -> None:
    state = load_state(topic)
    plan = load_plan(topic)
    phases = plan.get("execution_phases", [])

    completed = set(state.get("completed_phases", []))

    print("Topic: {}".format(topic))
    print("Plan exists: {}".format(plan_path(topic).exists()))
    print("Last prompted phase: {}".format(state.get("last_prompted_phase")))
    print()
    print("Phases:")

    if not phases:
        print("No phases found yet.")
        return

    for phase in phases:
        phase_id = phase.get("id")
        mark = "✓" if phase_id in completed else " "
        print("[{}] {} — {}".format(mark, phase_id, phase.get("name")))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Codex prompts for Wheels topics."
    )

    parser.add_argument(
        "--topic",
        required=True,
        help="Topic id, for example: word2vec",
    )

    parser.add_argument(
        "--startup",
        action="store_true",
        help="Print startup prompt to create plan.yaml",
    )

    parser.add_argument(
        "--next",
        action="store_true",
        help="Print next phase prompt from plan.yaml",
    )

    parser.add_argument(
        "--mark-done",
        action="store_true",
        help="Mark last prompted phase as done",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show topic phase status",
    )

    args = parser.parse_args()

    if args.startup:
        print_startup_prompt(args.topic)
    elif args.next:
        print_next_prompt(args.topic)
    elif args.mark_done:
        mark_done(args.topic)
    elif args.status:
        print_status(args.topic)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
