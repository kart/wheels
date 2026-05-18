# Fix Log: section_01_problem_and_prerequisites

## Inputs

- Reviewer report: `topics/adam/sections/section_01_problem_and_prerequisites/review.md`
- User comments: revise the central visual so it is not clipped, text stays inside the canvas, arrows are less oversized, labels are clearer, the right panel does not imply magical knowledge of the optimum, the memory callout does not occlude the plot, Adam-friendly notation is used where appropriate, and the caption remains clear that the visual is conceptual.

## Decisions

| Item | Decision | Reason | Files changed |
|---|---|---|---|
| Reviewer blocking finding: right side of SVG and preview are clipped. | accepted | Verified in the SVG source and prior rendered preview; long right-panel text exceeded the canvas. | `visuals/noisy_gradient_trace.svg`, `preview.html` |
| User comment: keep all labels and subtitles fully visible. | accepted | This is required for a reader-facing teaching visual. | `visuals/noisy_gradient_trace.svg` |
| User comment: reduce oversized arrows and visual clutter. | accepted | The original arrow markers competed with the plot and made the diagram harder to parse. | `visuals/noisy_gradient_trace.svg` |
| User comment: clarify that left panel shows SGD reacting to noisy/latest gradients. | accepted | This matches the section learning goal and paper motivation around stochastic gradients. | `visuals/noisy_gradient_trace.svg`, `draft.md`, `blog_fragment.md`, `preview.html`, `media_plan.md` |
| User comment: clarify that right panel shows Adam-style running estimates of direction and squared-gradient scale. | accepted | This is source-supported by the Adam paper notes and glossary definitions for `m_t` and `v_t`. | `visuals/noisy_gradient_trace.svg`, `draft.md`, `blog_fragment.md`, `preview.html`, `media_plan.md`, `source_notes.md` |
| User comment: avoid implying optimizer state knows the direct path to the optimum. | accepted | The redesigned right panel labels the step as estimate-shaped and explicitly says it is not a perfect map to the minimum. | `visuals/noisy_gradient_trace.svg` |
| User comment: move/redesign memory callout so it does not occlude the plot. | accepted | The callout now sits below the right plot area rather than inside the plotted trajectory. | `visuals/noisy_gradient_trace.svg` |
| User comment: keep caption clear that this is conceptual, not measured. | accepted | Caption now says "conceptual sketch" and "not a measured result from the paper" in draft, blog fragment, and preview. | `draft.md`, `blog_fragment.md`, `preview.html`, `media_plan.md` |
| Reviewer optional improvement: blog fragment caption omitted the measured-result caveat. | accepted | The blog fragment should carry the same source-fidelity caveat as the draft and preview. | `blog_fragment.md` |
| Reviewer optional improvement: soften "billions of parameters." | deferred | User comments focused on the visual. The wording is non-blocking and can be addressed in a later prose pass if desired. | none |
| Reviewer optional improvement: add responsive table wrappers. | deferred | The current fix scope is the central visual; existing tables are short and were not the approval blocker. | none |
| User follow-up: change left label, remove `g_2`/`g_4`, rename noisy-gradient label, reduce arrowheads, remove floating dashed arrows, add a below-plot recent-gradient callout, relabel green arrow, and clarify that `m_t`/`v_t` are introduced later. | accepted | These changes improve visual precision and avoid implying unexplained gradient-to-step notation before the prose has introduced it. | `visuals/noisy_gradient_trace.svg`, `draft.md`, `blog_fragment.md`, `preview.html`, `media_plan.md`, `fix_log.md`, `state.yaml` |
| User request: replace the hand-authored SVG with a code-generated technical visual following the Wheels code-generated visual policy. | accepted | This matches the updated visual policy and makes the Python generator the inspectable source of truth while preserving the same conceptual teaching goal. | `visuals/noisy_gradient_trace_spec.md`, `visuals/noisy_gradient_trace.py`, `visuals/noisy_gradient_trace.svg`, `visuals/noisy_gradient_trace.png`, `media_plan.md`, `source_notes.md`, `fix_log.md`, `state.yaml` |
| User request: improve the opening prerequisite/intuition ramp. | accepted | The original opening introduced optimizer/objective/gradient/notation too quickly for a first section. The revised opening starts from parameters as knobs, loss as a wrongness score, training as repeated knob changes, gradients as local hints, mini-batches as cheaper noisy hints, SGD as following the latest hint, and Adam as stateful memory. | `draft.md`, `blog_fragment.md`, `preview.html`, `authoring_notes.md`, `source_notes.md`, `fix_log.md`, `state.yaml` |

## Verification

- Re-rendered `visuals/noisy_gradient_trace.svg` with headless Chrome and inspected the generated PNG.
- Re-rendered `preview.html` with headless Chrome and inspected the generated PNG.
- Re-rendered `preview.html` with local `.venv` Playwright/Chromium at desktop width and inspected the generated PNG.
- Captured the preview figure with local `.venv` Playwright/Chromium at mobile width and inspected the generated PNG.
- Confirmed the redesigned SVG text is within the canvas in rendered output and the preview embeds the revised visual without right-edge clipping.
- Follow-up visual refinements were re-rendered with local `.venv` Playwright/Chromium for the standalone SVG, desktop preview, and mobile figure capture. The revised labels and callout render without right-edge clipping.
- Code-generated replacement was created with `visuals/noisy_gradient_trace.py` as source of truth and rendered to SVG/PNG with `.venv/bin/python`.
- The generator fixes SVG hash salt and omits timestamp metadata to reduce artifact churn across reruns.
- Re-rendered the standalone SVG and `preview.html` with local `.venv` Playwright/Chromium after the final prose changes.
- Captured the preview figure at mobile width with local `.venv` Playwright/Chromium.
- Confirmed the rendered visual has no obvious clipped text, text outside the canvas, oversized arrows, overlapping labels, or misleading direct-path implication.

## Remaining Open Issues

- A reviewer should re-check the revised visual and preview before user approval.
- No known section-local blocker remains from the accepted visual findings. A reviewer should still perform the normal approval-gate review.
