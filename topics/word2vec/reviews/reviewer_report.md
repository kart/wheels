# Reviewer Report: Word2Vec

Review phase: `phase_07_reviewer_audit`

Scope reviewed:

- `topic.yaml`
- `plan.yaml`
- `raw/papers/word2vec.pdf` via previously extracted/source-mapped content
- `wiki/`
- `outputs/lesson.md`
- `outputs/visual_plan.md`
- `outputs/visuals/*.svg`
- `outputs/code/*.py`
- `outputs/preview.html`

Reviewer rule followed: this report is the only artifact changed in this phase.

## Findings

### Medium: Preview still exposes draft-only visual and code production notes

Files:

- `outputs/preview.html:133`
- `outputs/preview.html:147`
- `outputs/preview.html:330`
- `outputs/preview.html:356`
- `outputs/preview.html:386`
- `outputs/preview.html:390`
- `outputs/preview.html:410`
- `outputs/preview.html:413`
- `outputs/preview.html:574`
- `outputs/preview.html:577`
- `outputs/preview.html:580`

The preview correctly replaces visual placeholders with real figures, but it also leaves the draft scaffolding text immediately after those figures: `Caption draft`, `Placement note`, `Visual Placeholder Checklist`, `Code Demo Placement Notes`, and `Expansion Notes for the Final Lesson`.

This does not break source fidelity, but it undermines the phase 06 requirement for a polished local reading experience. A learner reading the preview sees production instructions mixed into the lesson, which can distract from the topic and make the page feel like an internal build artifact rather than a teaching preview.

Recommended fix:

- In `outputs/preview.html`, hide or omit draft-only scaffolding sections and placement-note paragraphs.
- Keep the actual figure captions and code demo blocks.
- Keep `outputs/lesson.md` unchanged unless the fixer decides the draft itself should retain those notes for authoring.

### Medium: The first code demo appears before CBOW and Skip-gram are fully taught

Files:

- `outputs/preview.html:150`
- `outputs/preview.html:182`
- `outputs/preview.html:205`
- `outputs/lesson.md:97`
- `outputs/lesson.md:101`
- `outputs/lesson.md:162`

The toy context-pair script is useful and technically correct, but in the preview it appears in full immediately after the context-window introduction and before the dedicated CBOW and Skip-gram sections. The code defines `cbow_examples` and `skipgram_examples` before the reader has seen the full beginner explanation of either architecture.

This partially weakens the topic rule: "If code is included, explain the idea before the code." Section 2 explains the broad prediction-game idea, but not enough to make a novice comfortable with the full script and its output.

Recommended fix:

- Move the `toy_context_pairs.py` demo after both the CBOW and Skip-gram sections, or collapse the source code by default with a short visible sample output.
- Add one short lead-in paragraph before the code: "Now that both prediction directions are clear, this script prints the training examples."

### Low: `outputs/visual_plan.md` contains stale preview status

File:

- `outputs/visual_plan.md:22`

The visual plan still says `outputs/preview.html` does not exist and should be integrated in phase 06. That was true at phase 04, but it is now stale after phase 06 generated `outputs/preview.html`.

This is not a lesson correctness issue, but it can confuse later reviewers or fixers using `visual_plan.md` as current status documentation.

Recommended fix:

- Update the line to say the visuals have been integrated into `outputs/preview.html` in phase 06.
- If preserving phase history is desired, phrase it as "At phase 04 this did not exist; phase 06 later integrated the assets."

### Low: Toy context-pair output can confuse beginners because the word `the` appears twice

Files:

- `outputs/code/toy_context_pairs.py:85`
- `outputs/preview.html:261`
- `outputs/preview.html:297`

The demo sentence is clear and familiar, but because `the` appears twice, the output contains multiple examples where `the` is the center word. Without token positions, a novice may not realize those are different occurrences in the sentence.

This is not technically wrong. It is a clarity issue in an educational demo.

Recommended fix:

- Either print token positions, for example `the@0` and `the@6`, or use a toy sentence without duplicate words.
- If positions are added, keep the main conceptual labels unchanged: CBOW remains `context -> current`, Skip-gram remains `current -> context`.

## Checks Passed

### Source fidelity

Passed with cautions.

- The lesson consistently distinguishes `Paper claim` from `Teaching interpretation`.
- The lesson avoids saying Word2Vec invented continuous/distributed word representations.
- Claims about exact-match scoring, synonym handling, table values, and the Microsoft Sentence Completion result are grounded in the wiki/source summary.
- The lesson correctly frames analogy arithmetic as empirical, not symbolic reasoning.
- The "state of the art" sentence is tied to the Microsoft challenge and says "at the time" in `outputs/lesson.md:374`.

No major overclaim found.

### CBOW vs Skip-gram direction

Passed.

- `outputs/lesson.md:119` states CBOW as `context words -> current/middle word`.
- `outputs/lesson.md:184` states Skip-gram as `current/center word -> surrounding context words`.
- `outputs/visual_plan.md:43` describes CBOW context words flowing to `w(t)`.
- `outputs/visual_plan.md:50` describes Skip-gram `w(t)` flowing outward to context predictions.
- `outputs/code/toy_context_pairs.py:9` through `outputs/code/toy_context_pairs.py:11` preserve the same directions.

No reversal found.

### Visual correctness

Passed with minor review cautions.

- All eight SVG files parse as valid XML.
- Each SVG contains a `<title>` and `<desc>`.
- `cbow_flow.svg` and `skipgram_flow.svg` preserve the Figure 1 prediction directions.
- `complexity_comparison.svg` is explicitly labeled qualitative and does not invent exact numeric measurements.
- `one_hot_vs_dense.svg` and `analogy_vector_offset.svg` mark their geometry as illustrative rather than paper data.
- No decorative-only visual was found; each visual teaches a mechanism, contrast, or evaluation step.

Remaining caution:

- Browser screenshot verification was not available in the previous phase, so visual text fitting and mobile scaling still need manual/browser review.

### Code demos

Passed with the pedagogical placement issue noted above.

- `outputs/code/toy_context_pairs.py` runs successfully.
- `outputs/code/analogy_demo.py` runs successfully.
- Both scripts use only Python standard library.
- Both scripts include explicit toy-data caveats.
- `outputs/review.md` documents why `tiny_skipgram_training.py` was skipped.

No code correctness failure found.

### HTML preview integrity

Passed with the draft-note issue noted above.

Static checks found:

- 8 image references in `outputs/preview.html`.
- 0 missing image files.
- 0 missing `alt` attributes.
- 39 internal TOC links.
- 0 missing anchor targets.
- Code demos and sample outputs are present.
- CSS includes mobile media rules and scroll handling for code/tables.

Browser limitation:

- Automated screenshot/layout testing could not be verified here because Playwright/Chromium tooling was not available in the environment.

### Beginner suitability

Mostly passed.

Strengths:

- The lesson starts with motivation before mechanics.
- Examples precede equations in the CBOW, Skip-gram, and cost sections.
- Equations are accompanied by plain-English variable explanations.
- Visuals are placed near the relevant concepts.
- The result section avoids dumping every paper table.

Main risks:

- The preview still contains authoring scaffolding.
- The first code block is long and appears before both model directions have been fully taught.

## Rule Compliance

Passed.

- No raw files were modified during this review phase.
- No wiki, lesson, output, visual, code, topic, or plan files were edited during this review phase.
- This report is the only phase 07 output.

## Suggested Fix Priority

1. Remove or hide draft-only scaffolding from `outputs/preview.html`.
2. Move or collapse the toy context-pair code demo so it appears after CBOW and Skip-gram are both explained.
3. Update stale preview status in `outputs/visual_plan.md`.
4. Add token positions or use a no-duplicate toy sentence in `toy_context_pairs.py`.
