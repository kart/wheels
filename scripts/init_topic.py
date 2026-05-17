#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


SUPPORTED_ARTICLE_SHAPES = {
    "paper_deep_dive": "Paper Reading",
    "system_design_deep_dive": "System Design",
    "algorithm_walkthrough": "Algorithms",
    "general_concept_deep_dive": "Concepts",
}

RAW_DIRS = [
    "papers",
    "articles",
    "images",
    "notes",
    "extracted",
    "repos",
]

TOPIC_ID_RE = re.compile(r"^[a-z0-9_-]+$")


def derived_title(topic_id: str) -> str:
    return topic_id.replace("-", " ").replace("_", " ").title()


def render_topic_yaml(topic_id: str, article_shape: str, audience_profile: str) -> str:
    category = SUPPORTED_ARTICLE_SHAPES[article_shape]
    title = derived_title(topic_id)

    return f"""id: {topic_id}
title: "{title}"
audience_profile: {audience_profile}
article_shape: {article_shape}

workflow:
  mode: section_by_section
  require_user_approval_per_section: true
  use_new_wheels_skills: true

publish_target:
  format: jekyll_markdown
  layout: default
  category: "{category}"
  asset_base_path: /assets/images
  asset_filename_prefix: {topic_id}-

raw_resource_policy:
  paper_deep_dive: "Place primary papers under raw/papers/."
  system_design_deep_dive: "Place the design prompt or brief under raw/brief.md; add supporting notes/articles under raw/notes/ or raw/articles/."
  algorithm_walkthrough: "Place the problem statement under raw/problem.md."
  general_concept_deep_dive: "Place the concept brief under raw/brief.md; add supporting resources under raw/."

quality_contract:
  - Mechanism-first, not prose-first.
  - Use code when it naturally clarifies the concept.
  - Do not force code when a worked example, diagram, table, or trace teaches better.
  - Explain motivation before mechanism.
  - Use examples before abstraction.
  - Introduce equations only after intuition.
  - Include toy-to-real bridges where applicable.
  - Keep sections small and reviewable.
  - Require user approval before moving to the next section.

section_planning_preferences:
  - Prefer small, reviewable sections.
  - Each section should answer a concrete learning question.
  - Each section should identify a concrete teaching mechanism.
  - Each section should include expected reader confusions.
  - Each section should include a toy-to-real bridge where applicable.
"""


def validate_args(args: argparse.Namespace) -> None:
    if not TOPIC_ID_RE.match(args.topic_id):
        raise ValueError(
            "--id must contain only lowercase letters, numbers, underscores, and hyphens"
        )

    if args.article_shape not in SUPPORTED_ARTICLE_SHAPES:
        supported = ", ".join(sorted(SUPPORTED_ARTICLE_SHAPES))
        raise ValueError(f"--article-shape must be one of: {supported}")

    if not args.audience_profile.strip():
        raise ValueError("--audience-profile must be non-empty")


def init_topic(args: argparse.Namespace) -> Path:
    validate_args(args)

    topic_dir = Path("topics") / args.topic_id
    topic_yaml = topic_dir / "topic.yaml"

    if topic_dir.exists() and not args.force:
        raise FileExistsError(
            f"{topic_dir} already exists. Refusing to overwrite without --force."
        )

    if not topic_dir.exists():
        topic_dir.mkdir(parents=True)

        raw_dir = topic_dir / "raw"
        raw_dir.mkdir()

        for name in RAW_DIRS:
            (raw_dir / name).mkdir()

    topic_yaml.write_text(
        render_topic_yaml(
            topic_id=args.topic_id,
            article_shape=args.article_shape,
            audience_profile=args.audience_profile,
        ),
        encoding="utf-8",
    )

    return topic_yaml


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a deterministic minimal Wheels topic scaffold."
    )
    parser.add_argument("--id", dest="topic_id", required=True, help="Topic id.")
    parser.add_argument(
        "--article-shape",
        required=True,
        choices=sorted(SUPPORTED_ARTICLE_SHAPES),
        help="Article shape for this topic.",
    )
    parser.add_argument(
        "--audience-profile",
        required=True,
        help="Audience profile id for this topic.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite only topics/<id>/topic.yaml if the topic already exists.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        topic_yaml = init_topic(args)
    except (ValueError, FileExistsError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Created or updated {topic_yaml}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
