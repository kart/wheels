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
  - id: phase_01_source_extraction_and_source_map
    name: "Source extraction and source map"
    goal: ""
    inputs:
      - topic.yaml
      - raw/
    outputs: []
    instructions: []
    completion_check: []

  - id: phase_02_compile_wiki
    name: "Compile wiki"
    goal: ""
    inputs:
      - topic.yaml
      - raw/
    outputs: []
    instructions: []
    completion_check: []

  - id: phase_03_refine_plan_after_wiki
    name: "Refine plan after wiki"
    goal: "Refine plan.yaml into appropriately sized lesson/content chunks after the wiki exists."
    inputs:
      - topic.yaml
      - plan.yaml
      - wiki/
      - wiki_preview/
    outputs:
      - plan.yaml
    instructions:
      - Preserve completed phases.
      - Replace overly broad future phases with chunked phases when useful.
      - Each chunk phase should generate content, visuals, preview updates, review report, validated fixes, and a fix log.
      - Do not generate lesson content during this phase.
    completion_check:
      - plan.yaml has execution_phases.
      - future lesson/content work is split into appropriate chunks for the topic size.

  - id: phase_04_create_lesson_outline
    name: "Create lesson outline"
    goal: ""
    inputs:
      - wiki/
      - topic.yaml
      - plan.yaml
    outputs: []
    instructions: []
    completion_check: []

  - id: phase_05_expand_content_chunk
    name: "Expand content chunk"
    goal: ""
    inputs:
      - wiki/
      - outputs/lesson.md
      - outputs/visual_plan.md
    outputs: []
    instructions: []
    completion_check: []

  - id: phase_90_final_reviewer_audit
    name: "Final reviewer audit"
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

  - id: phase_91_final_fixer_loop
    name: "Final fixer loop"
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

  - id: phase_99_publish_pack
    name: "Publish pack"
    goal: ""
    inputs:
      - prompts/publish_pack.md
      - outputs/
      - reviews/
    outputs:
      - outputs/publish/
    instructions: []
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
- prompts/audience_profiles.md if it exists
- templates/article_shapes.md if it exists

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
- Follow the selected audience_profile and article_shape from topic.yaml if present.
- If you cannot reliably read a source directly, say so in plan.yaml and recommend the minimum extraction needed.
- Include a post-wiki replanning phase unless the topic is obviously tiny.
- For large papers/resources, plan should eventually split content generation into multiple chunk phases.
- Each later chunk phase should include generation, visuals, preview update, review, validated fixes, and fix log.

The plan.yaml MUST use this structure:

$schema

You may add more phases if needed, but keep the schema machine-readable.

Every execution phase must contain:
- id
- name
- goal
- inputs
- outputs
- instructions
- completion_check
"""
)


REPLAN_PROMPT_TEMPLATE = Template(
    """
Use AGENTS.md as global repo guidance.

We are refining the execution plan for:

topics/$topic/

Read:
- topics/$topic/topic.yaml
- topics/$topic/plan.yaml
- topics/$topic/wiki/
- topics/$topic/wiki_preview/index.html if it exists
- prompts/audience_profiles.md if it exists
- templates/article_shapes.md if it exists

Completed phases so far:
$completed_phases

Task:
Refine topics/$topic/plan.yaml now that the compiled wiki exists.

Goal:
Make the plan suitable for the actual topic size and source complexity.

For larger papers/resources, split lesson/content generation into multiple manageable content chunks.

Required behavior:
1. Preserve useful strategy sections already in plan.yaml.
2. Preserve completed phases and their ids.
3. Do not delete or rename completed phase ids.
4. Replace overly broad future lesson-generation phases with:
   - one outline phase
   - multiple chunk phases
   - final review/fix phases
   - publish-pack phase later
5. Each chunk phase should represent a coherent part of the topic.
6. Each chunk phase should include the full local loop:
   - update outputs/lesson.md only for that chunk
   - update outputs/visual_plan.md
   - generate visual/code assets for that chunk if useful
   - update outputs/preview.html as a reader-facing blog preview
   - run a reviewer pass for that chunk
   - write reviews/<phase_id>_review.md
   - validate reviewer findings
   - apply accepted fixes
   - write reviews/<phase_id>_fix_log.md
   - stop and wait for the user before the next phase
7. For paper_deep_dive topics, preserve deep source coverage.
   - Do not collapse the paper into a high-level overview.
   - Include section-by-section source coverage or an explicitly justified adapted structure.
8. For system_design_deep_dive and algorithm_walkthrough topics, chunk according to the selected article shape.

Important:
- Do not generate lesson content now.
- Do not generate visuals now.
- Do not modify raw/.
- Only modify topics/$topic/plan.yaml.
- Keep paths relative to topics/$topic/.
- Preserve compatibility with scripts/wheels_prompt.py.

Every execution phase must contain:
- id
- name
- goal
- inputs
- outputs
- instructions
- completion_check
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

General rules:
- Do not run later phases.
- Do not modify raw/.
- Stay grounded in the available sources.
- Follow the audience profile in topic.yaml.
- Follow the selected article_shape in topic.yaml if present.
- Follow the explanation quality bar and visual quality bar in AGENTS.md.
- Use project venv commands when running Python tools:
  - .venv/bin/python
  - .venv/bin/pip
  - .venv/bin/manim
- Do not use system Python, system pip, or bare manim unless explicitly asked.
- If this phase creates or updates visual assets, update preview.html accordingly.
- If this phase is review-only, do not edit source/wiki/output files; only write the review report.

Phase-specific guardrails:
$phase_guardrails
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


def classify_phase(phase: dict) -> str:
    text = "{} {}".format(
        phase.get("id", ""),
        phase.get("name", ""),
    ).lower()

    if "review" in text or "audit" in text:
        return "review"

    if "fix" in text:
        return "fix"

    if "publish" in text:
        return "publish"

    if "preview" in text or "html" in text:
        return "preview"

    if "manim" in text or "animation" in text:
        return "manim"

    if "code" in text:
        return "code"

    if "visual" in text or "asset" in text or "diagram" in text:
        return "visual"

    if "replan" in text or "refine_plan" in text or "refine plan" in text:
        return "replan"

    if "outline" in text:
        return "outline"

    if "chunk" in text or "section" in text:
        return "content_chunk"

    if "lesson" in text or "draft" in text:
        return "lesson"

    if "wiki" in text or "source" in text or "extraction" in text:
        return "wiki"

    return "general"


def guardrails_for_phase(topic: str, phase: dict) -> str:
    kind = classify_phase(phase)
    phase_id = phase.get("id", "phase")

    common = """
- Keep outputs beginner-friendly.
- Use examples and intuition before equations.
- Avoid unsupported claims.
- Prefer clear, readable output over cleverness.
""".strip()

    if kind == "wiki":
        return common + """

Wiki/source guardrails:
- Compile source-grounded understanding, not a polished article.
- Separate source claims from interpretation.
- Track uncertainty and missing extraction needs.
- Do not invent context not present in the sources.
- If figures/tables are important and PDF text extraction is insufficient, flag them explicitly.
"""

    if kind == "replan":
        return common + """

Replan guardrails:
- Only update plan.yaml.
- Preserve completed phases and completed phase ids.
- For large topics, split future content work into coherent chunk phases.
- Each chunk phase should include content generation, visual/code asset generation if useful, preview update, reviewer report, validated fixes, and fix log.
- Do not generate lesson prose during replanning.
"""

    if kind == "outline":
        return common + """

Outline guardrails:
- Create a strong article/lesson outline, not the full prose-heavy lesson.
- Use the selected article_shape from topic.yaml.
- Include where visuals should appear.
- Include where code or pseudocode should appear if useful.
- For paper_deep_dive topics, include section-by-section source coverage or an explicitly justified adapted structure.
- Keep this modular so later phases can expand chunks one at a time.
"""

    if kind in {"content_chunk", "lesson"}:
        return common + """

Content chunk guardrails:
- Work only on the intended chunk/section for this phase.
- Do not rewrite unrelated sections.
- Build up concepts gradually.
- Motivation before mechanics.
- Intuition before equations.
- Examples before abstraction.
- Visuals should be placed near the text they support.
- Code should appear only after the concept is explained.
- For paper_deep_dive topics, preserve deep source coverage; do not collapse into a high-level overview.
- Update outputs/lesson.md.
- Update outputs/visual_plan.md.
- Generate or update visual/code assets for this chunk if useful.
- Update outputs/preview.html as a reader-facing blog preview.
- Write a chunk-level reviewer report at reviews/{phase_id}_review.md.
- Validate reviewer findings and apply accepted fixes.
- Write a chunk-level fix log at reviews/{phase_id}_fix_log.md.
- Stop after this chunk; do not continue to the next chunk.
""".replace("{phase_id}", phase_id)

    if kind == "visual":
        return common + """

Visual guardrails:
- Prioritize correctness and educational clarity over beauty.
- Create deterministic, source-consistent visuals.
- Avoid decorative visuals that do not teach.
- Do not invent exact numeric charts unless the numbers are explicitly sourced.
- If a chart is qualitative, label it clearly as qualitative.
- Verify arrows, labels, directions, axes, and captions.
- Ensure visual file paths match lesson.md, visual_plan.md, and preview.html.
- If a visual is too risky or under-specified, leave a placeholder and explain why in outputs/review.md.
"""

    if kind == "code":
        return common + """

Code guardrails:
- Only create code that genuinely improves understanding.
- Keep code beginner-friendly and well-commented.
- Explain intuition before code.
- Prefer Python standard library or minimal dependencies.
- Do not pretend toy demos reproduce paper-scale or production-scale results.
- Run generated scripts if possible using .venv/bin/python.
- Capture expected output when useful for the lesson or preview.
"""

    if kind == "preview":
        return common + """

Preview guardrails:
- outputs/preview.html should look like a reader-facing blog preview, not an internal artifact dashboard.
- Include table of contents.
- Place visuals near the relevant explanations.
- Include captions and alt text.
- Render code blocks cleanly.
- Do not depend on external CDNs.
- If an asset is missing, show a clear placeholder instead of breaking the page.
- Move internal/debug details to a collapsed Build Notes section or omit them.
"""

    if kind == "review":
        return common + """

Review guardrails:
- Read prompts/reviewer.md.
- Do not modify lesson.md, preview.html, visual_plan.md, visuals, code, wiki, topic.yaml, plan.yaml, or raw files.
- Only write the reviewer report.
- Be strict about source fidelity, technical correctness, visual correctness, and beginner suitability.
- Ignore minor grammar/style unless it affects understanding.
- Check that visuals match captions and nearby text.
- Check that code demos match lesson claims.
- For paper topics, check that the output does not overstate what the source proves.
"""

    if kind == "fix":
        return common + """

Fixer guardrails:
- Read prompts/fixer.md.
- Read the reviewer report carefully.
- For each reviewer finding, decide whether it is valid.
- If valid, apply the smallest correct fix.
- If invalid, explain why it was rejected.
- Do not blindly apply reviewer comments.
- Do not rewrite unrelated sections.
- Preserve the intended audience level.
- Update preview.html after accepted content, visual, or code changes.
- Update the relevant fix log with accepted, rejected, and partially accepted findings.
"""

    if kind == "publish":
        return common + """

Publish guardrails:
- Read prompts/publish_pack.md if it exists.
- Create a clean publish-ready package from reviewed and fixed outputs.
- outputs/publish/blog.md should be Jekyll-ready if topic.yaml publish_target.format is jekyll_markdown.
- Use Jekyll front matter from topic.yaml publish_target.
- Use image paths based on publish_target.asset_base_path.
- Do not include internal reviewer/debug notes in the final blog.
- Do not create unsupported new claims.
- Do not actually publish anything.
- At the end of your response, print copy commands only if topic.yaml or the user has provided a publish destination.
"""

    if kind == "manim":
        return common + """

Manim guardrails:
- Treat Manim output as experimental unless the plan says otherwise.
- Use .venv/bin/manim.
- Keep scenes simple and robust.
- Avoid LaTeX-heavy rendering unless necessary.
- Do not copy copyrighted paper figures directly.
- Clearly document render commands and output paths.
"""

    return common


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


def print_replan_prompt(topic: str) -> None:
    topic_yaml = topic_yaml_path(topic)
    plan = plan_path(topic)

    if not topic_yaml.exists():
        print("ERROR: Missing {}".format(topic_yaml))
        sys.exit(1)

    if not plan.exists():
        print("ERROR: Missing {}".format(plan))
        print("Run startup first:")
        print("python scripts/wheels_prompt.py --topic {} --startup".format(topic))
        sys.exit(1)

    state = load_state(topic)
    completed = state.get("completed_phases", [])

    prompt = REPLAN_PROMPT_TEMPLATE.substitute(
        topic=topic,
        completed_phases=yaml_block(completed),
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
    guardrails = guardrails_for_phase(topic, phase)

    prompt = PHASE_PROMPT_TEMPLATE.substitute(
        topic=topic,
        phase_id=phase_id,
        phase_name=phase_name,
        goal=goal,
        inputs=inputs,
        outputs=outputs,
        instructions=instructions,
        completion_check=completion_check,
        phase_guardrails=guardrails,
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
        "--replan",
        action="store_true",
        help="Print prompt to refine plan.yaml after wiki exists",
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
    elif args.replan:
        print_replan_prompt(args.topic)
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
