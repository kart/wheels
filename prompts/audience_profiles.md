# Audience Profiles

## beginner_technical

The reader has undergraduate-level technical maturity.

Assume:
- math may be weak
- coding skill is novice to beginner
- the reader is capable but needs careful buildup
- examples, intuition, and visuals are essential

Explanation rules:
- Motivation before mechanics
- Intuition before equations
- Examples before abstraction
- Visuals wherever they reduce cognitive load
- Short sections instead of long walls of text
- Code only after explaining what the code is trying to do
- Code must be well-commented and educational
- Avoid unexplained formulas
- Avoid shallow summaries
- Avoid assuming ML/system-design/algorithm expertise

Tone:
- Clear
- Patient
- Concrete
- Not condescending
- Not hype-driven

## system_design_interview_l5_plus

The reader is preparing for system design interviews at L5/L6/L7-like levels.

Default path:
- Aim the main article at a strong L5 candidate.
- Keep the core flow coherent: requirements, APIs, data model, core architecture, bottlenecks, scaling, tradeoffs, and failure modes.
- Explain every major design decision with the reason behind it, not just the selected component or pattern.
- Avoid shallow interview-prep answers.
- Avoid verbosity caused by repeating the entire answer separately for each level.

L6+ forks:
- Include L6+ forks where useful, but do not make every paragraph have separate L5/L6/L7 versions.
- Use L6+ forks only when they add meaningful design depth.
- Deepen the design with topics such as multi-region architecture, consistency boundaries, operational maturity, cost controls, capacity modeling, data evolution, incident handling, platform abstractions, and organizational/ownership tradeoffs.
- Use callouts such as:
  - "L6+ extension:"
  - "Senior-level tradeoff:"
  - "Where a stronger answer goes deeper:"

Design guidance:
- Database choices should include SQL vs NoSQL tradeoffs when relevant.
- APIs should be concrete when relevant.
- Workflows should be step-by-step.
- Diagrams should be architecture, sequence, or data-flow oriented.
- Failure modes and observability should be included.
- Source-grounded public facts must be separated from inferred design choices.

Tone:
- Interview-practical
- Precise
- Tradeoff-aware
- Senior where it matters
- Not padded
