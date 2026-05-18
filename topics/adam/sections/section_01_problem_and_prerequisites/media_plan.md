# Media Plan

## Generated Section Visual

- Spec: `topics/adam/sections/section_01_problem_and_prerequisites/visuals/noisy_gradient_trace_spec.md`
- Source: `topics/adam/sections/section_01_problem_and_prerequisites/visuals/noisy_gradient_trace.py`
- Rendered outputs:
  - `topics/adam/sections/section_01_problem_and_prerequisites/visuals/noisy_gradient_trace.svg`
  - `topics/adam/sections/section_01_problem_and_prerequisites/visuals/noisy_gradient_trace.png`
- Purpose: Contrast SGD reacting to noisy/latest stochastic gradients with Adam-style running estimates of recent direction and squared-gradient scale.
- Type: Code-generated simplified qualitative teaching diagram.
- Source relationship: Inspired by the paper's motivation around stochastic, noisy, sparse, and high-dimensional optimization. It is not copied from the paper.
- Caption: "A conceptual sketch of the motivation: a single mini-batch gradient can be useful and still wobble, while Adam-style optimizers keep running estimates of recent direction and squared-gradient scale. The symbols `m_t` and `v_t` are introduced later; this is not a measured result from the paper."

## Source Evidence Not Embedded

- `topics/adam/wiki/source_assets/pages/paper_01_page_01.png`
- `topics/adam/wiki/source_assets/pages/paper_01_page_05.png`

These page screenshots remain source evidence only and are not reader-facing visuals for this section.

## Code

The visual generator is section-local educational infrastructure, not reader-facing lesson code. It should be treated as the source of truth for the rendered SVG and PNG.
