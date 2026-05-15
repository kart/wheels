# Fix Log: Word2Vec

Fix phase: `phase_08_fixer_loop`

Inputs reviewed:

- `topic.yaml`
- `plan.yaml`
- `wiki/`
- `outputs/`
- `reviews/reviewer_report.md`

Rule compliance:

- `raw/` was not modified.
- No publish draft was created.
- Fixes were limited to validated reviewer findings.

## Reviewer Findings and Decisions

### Finding 1: Preview exposes draft-only visual and code production notes

Decision: accepted.

Validation:

- The reviewer was correct. `outputs/preview.html` displayed learner-facing figures and code demos, but also retained authoring text such as `Caption draft`, `Placement note`, `Visual Placeholder Checklist`, `Code Demo Placement Notes`, and `Expansion Notes for the Final Lesson`.
- That text is useful in `outputs/lesson.md` as a draft artifact, but it weakens the preview as a polished reading experience.

Fix applied:

- Regenerated `outputs/preview.html` so draft-only scaffolding is omitted from the local reading page.
- Kept the real figure captions, local SVGs, code demos, and sample outputs.
- Left `outputs/lesson.md` unchanged because it is intentionally a modular draft.

Verification:

- Static check confirms no preview text remains for `Caption draft`, `Placement note`, `Visual Placeholder Checklist`, `Code Demo Placement Notes`, `Expansion Notes for the Final Lesson`, or `Planned purpose`.

### Finding 2: First code demo appears before CBOW and Skip-gram are fully taught

Decision: accepted.

Validation:

- The reviewer was correct. The `toy_context_pairs.py` source appeared immediately after the context-window introduction, before the dedicated CBOW and Skip-gram sections.
- The lesson explains the broad prediction idea there, but a novice benefits from seeing both prediction directions before reading the script.

Fix applied:

- Regenerated `outputs/preview.html` so the `toy_context_pairs.py` demo appears after the CBOW and Skip-gram sections and before the speed/scaling section.
- Added a learner-facing lead-in in the preview: "Now that both prediction directions are clear, this script prints the toy training examples created from one sentence."
- The code source is collapsed by default while sample output remains open, reducing the wall-of-code effect on first read.

Verification:

- Preview check confirms `Code demo: CBOW and Skip-gram examples` now appears immediately before section `5. Why the Paper Cares So Much About Speed`.
- Code demo output remains present in the preview.

### Finding 3: `outputs/visual_plan.md` contains stale preview status

Decision: accepted.

Validation:

- The reviewer was correct. `outputs/visual_plan.md` still said `outputs/preview.html` did not exist, which was true during visual production but stale after phase 06.

Fix applied:

- Updated `outputs/visual_plan.md` to say phase 06 integrated the visual assets into `outputs/preview.html`, and that the preview should be rechecked after future visual, lesson, or code changes.

Verification:

- The stale "does not exist yet" statement no longer appears in `outputs/visual_plan.md`.

### Finding 4: Toy context-pair output can confuse beginners because `the` appears twice

Decision: accepted with implementation choice.

Validation:

- The reviewer was correct. The sentence is pedagogically useful and matches the lesson, but repeated `the` tokens can make output harder to inspect.

Fix applied:

- Kept the same toy sentence for alignment with the lesson and context-window visual.
- Updated `outputs/code/toy_context_pairs.py` to label every token as `word@index`, for example `the@0` and `the@6`.
- Regenerated `outputs/preview.html` so embedded source and sample output reflect the updated code.

Verification:

- Running `python outputs/code/toy_context_pairs.py` succeeds.
- Output now includes distinct labels such as `the@0` and `the@6`.
- CBOW remains `context words -> current word`.
- Skip-gram remains `current word -> surrounding word`.

## Verification Summary

Commands/checks run:

- `python outputs/code/toy_context_pairs.py`
- `python outputs/code/analogy_demo.py`
- Static preview integrity check:
  - 8 image references
  - 0 missing images
  - 0 missing alt attributes
  - 35 internal links
  - 0 missing anchor targets
  - no draft scaffolding strings left in `outputs/preview.html`
  - token-position labels present in `outputs/preview.html`
- `git diff -- raw topic.yaml plan.yaml wiki outputs/lesson.md outputs/visuals reviews/reviewer_report.md`

Result:

- Relevant artifacts were rechecked after fixes.
- No raw/source/wiki/lesson/visual/reviewer-report files were modified.

## Deep-dive publish repair

Date: 2026-05-14

Reason:

- The previous publish blog was reader-friendly but too shallow for the selected `paper_deep_dive` article shape.
- It skipped the first-principles bridge from raw words to numeric inputs, one-hot vectors, embedding lookup, and trainable word-vector parameters.
- It summarized the paper instead of walking through the paper's architecture and evaluation logic in enough depth for a beginner technical reader.

Files changed:

- `outputs/publish/blog.md`
- `outputs/preview.html`
- `reviews/fix_log.md`

Changes applied:

- Rewrote `outputs/publish/blog.md` as a true paper walkthrough while preserving Jekyll front matter.
- Added the missing first-principles bridge:
  - neural networks operate on numbers, not raw words
  - vocabularies map words to IDs
  - one-hot vectors have dimension `V`
  - one-hot vectors solve identity and fixed dimensionality but not similarity
  - dense word vectors are lower-dimensional trainable representations
  - the embedding matrix is a trainable `V x N` table
  - a one-hot vector selects a row from that table
- Clarified what is trained:
  - input/projection word-vector rows
  - output prediction parameters
  - hierarchical-softmax tree-decision parameters where relevant
  - updates come from prediction error without dumping backpropagation math
- Restored paper-deep-dive structure:
  - problem and numeric representation bridge
  - prior work and older neural language models
  - feedforward NNLM and RNNLM cost stories
  - CBOW and Skip-gram architectures
  - computational complexity
  - hierarchical softmax and Huffman tree intuition
  - analogy evaluation mechanics
  - experimental results and caveats
  - limitations, misconceptions, recap, and what came next
- Defined terms before formulas:
  - `V`, `N`, `D`, `H`, `C`, `T`, `E`, and `Q`
  - NNLM, RNNLM, hierarchical softmax, and Huffman tree
- Deepened analogy evaluation:
  - analogy question format
  - query-vector construction
  - cosine nearest-neighbor search
  - input-word exclusion
  - strict exact-match scoring
  - worked `big:biggest :: small:?` and `Paris - France + Italy -> Rome` examples
- Removed mechanical repeated "Paper claim" prose from the reader-facing article.
- Converted blog visuals to explicit `<figure>` blocks with exactly one visible `<figcaption>` each.
- Regenerated `outputs/preview.html` from the repaired blog content so it reads like the final post, with internal build notes collapsed at the bottom.

Remaining limitations:

- The local preview is a static HTML rendering, not a full Jekyll render with the site's production CSS.
- The SVGs are unchanged educational redraws; they still need a final human visual pass inside the target `karthik.dev` theme.
- The post uses selected table values from the source-grounded wiki rather than reproducing every paper table.

### Caption duplication follow-up

Decision: accepted.

Issue:

- The SVG assets already contain visible caption text inside their own bordered drawing area.
- The repaired blog and preview also added external `<figcaption>` text, causing each visual caption to appear twice.

Fix applied:

- Removed external `<figcaption>` elements from `outputs/publish/blog.md`.
- Regenerated `outputs/preview.html` from the blog so the preview no longer shows duplicate captions.
- Kept `alt` text on each image for accessibility.

Remaining limitation:

- The visible captions still live inside the SVG files. A future visual cleanup could remove those internal SVG captions and restore external HTML captions instead, but this pass used the smaller change.
