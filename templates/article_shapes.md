# Article Shapes

Article shapes define the reader-facing structure of the final blog/lesson.

A topic should choose one article shape in topic.yaml:

- paper_deep_dive
- system_design_deep_dive
- algorithm_walkthrough

The final outputs/preview.html and outputs/publish/blog.md should follow the selected shape.

---

## paper_deep_dive

Use for papers, research notes, technical reports, or foundational ideas from written sources.

Reader journey:

1. Why this matters
2. The problem before the paper
3. A tiny example
4. The core intuition
5. Prerequisite intuition
6. The paper's mechanism
7. Visual walkthrough
8. Minimal code/demo if useful
9. Experiments and results
10. What the paper does not prove
11. Common misconceptions
12. Recap
13. What came next

Style notes:

- Start with motivation, not citation trivia.
- Make the paper feel necessary.
- Use examples before formulas.
- Keep paper claims separate from later interpretation.
- Include visuals near the concepts they explain.
- Mention limitations and caveats explicitly.

For paper_deep_dive, the final blog must include either:

1. A section-by-section walkthrough of the source paper, or
2. An explicitly justified adapted structure that still covers every major paper section.

A paper_deep_dive must not collapse the paper into a high-level overview.

---

## system_design_deep_dive

Use for systems like Uber, YouTube, Twitter, Kafka, RocksDB, or distributed infra topics.

Reader journey:

1. What are we building?
2. One concrete user journey
3. Requirements and constraints
4. Back-of-the-envelope scale
5. Core APIs and entities
6. High-level architecture
7. Deep dives into hard parts
8. Data model
9. Failure modes and tradeoffs
10. Observability and operations
11. Final architecture
12. Interview-style recap

Style notes:

- Start with a concrete user action.
- Make requirements explicit.
- Explain tradeoffs instead of pretending there is one perfect design.
- Use architecture diagrams heavily.
- Include operational concerns, bottlenecks, and failure modes.

---

## algorithm_walkthrough

Use for LeetCode, DSA, algorithm patterns, or coding-interview problems.

Reader journey:

1. Problem in plain English
2. Tiny example
3. Brute force intuition
4. Why brute force is wasteful
5. Key insight
6. Visual dry run
7. Code
8. Complexity
9. Edge cases
10. Pattern behind the problem
11. Similar problems

Style notes:

- Do not jump to code.
- Explain the brute force first.
- Explain the waste.
- Explain the key insight.
- Dry-run visually before final code.
- Code should be beginner-friendly and well-commented.
