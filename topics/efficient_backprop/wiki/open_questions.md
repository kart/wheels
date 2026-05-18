# Open Questions And Bootstrap Caveats

## Source Extraction Caveats

- PDF text extraction is readable but contains encoding artifacts.
- Formula transcription should be visually checked against rendered pages before final prose.
- Figure captions are mostly available, but axes/labels need rendered-page inspection.
- No OCR was run.

## Paper Interpretation Caveats

- The source is a 1998 paper/chapter. Modern relevance notes in `historical_vs_current.md` are bootstrap interpretation, not source claims.
- If the final article makes concrete claims about current best practices, additional current sources should be added or the claims should be clearly marked as interpretation.
- The paper's recommendation of a specific scaled tanh activation should be framed in sigmoid-era context.
- The paper's target-scaling advice is tied to sigmoid outputs and should not be generalized blindly to modern architectures/losses.

## Items Later Section Authors Must Verify

- Exact formulas in sections 3, 5, 6, 7, and 9.
- Captions and visual meaning for Figures 6-8, 15-18, and 19-26.
- Whether section planning should include RBF material as a dedicated aside or fold it into the second-derivative discussion.
- How much modern interpretation the user wants in the final article.

## Foundation Gaps

- The source assumes comfort with derivatives, Jacobians, matrix multiplication, eigenvalues, and Taylor expansion.
- `foundation_stack.md` supplies the prerequisite scaffold, but later section planning must decide which background concepts deserve full sections and which can be introduced inline.

## Stop-Boundary Reminder

Bootstrap must stop before creating:

- `topics/efficient_backprop/sections/**`
- `topics/efficient_backprop/outputs/**`
- `topics/efficient_backprop/reviews/**`
- section prose
- section visuals
- section code
- publish artifacts
