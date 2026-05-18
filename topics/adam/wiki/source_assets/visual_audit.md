# Visual Audit

## PDFs Inspected

- `raw/papers/adam.pdf`

## Tools Used

- `pdfinfo` confirmed 15 pages.
- `pdftotext -layout` produced `wiki/source_assets/extracted/adam_pdftotext_layout.txt`.
- `pdftoppm -png -r 160` rendered all 15 pages under `wiki/source_assets/pages/`.

Both `pdftotext` and `pdftoppm` reported a recoverable xref reconstruction warning: `xref num 342 not found but needed, try to reconstruct`. The generated text and images are present, but formulas and plots should be checked against rendered pages.

## Pages Rendered

All pages were rendered because the PDF is short:

- `paper_01_page_01.png`
- `paper_01_page_02.png`
- `paper_01_page_03.png`
- `paper_01_page_04.png`
- `paper_01_page_05.png`
- `paper_01_page_06.png`
- `paper_01_page_07.png`
- `paper_01_page_08.png`
- `paper_01_page_09.png`
- `paper_01_page_10.png`
- `paper_01_page_11.png`
- `paper_01_page_12.png`
- `paper_01_page_13.png`
- `paper_01_page_14.png`
- `paper_01_page_15.png`

## Manual Spot Checks Needed Later

- Algorithm 1 notation on page 2: verify hats, square roots, and epsilon placement.
- Section 2.1 page 3: verify effective step-size bound cases before quoting exact inequalities.
- Section 3 pages 3-4: verify equation numbering and `zeta` explanation.
- Theorem 4.1 page 5 and appendix pages 12-15: verify assumptions before simplifying for beginners.
- Figures 1-4 pages 6-8: use qualitative descriptions unless exact values are manually extracted.
- AdaMax derivation pages 8-9: verify p-norm to infinity-norm limit before presenting formulas.

## OCR

OCR was not used. The PDF text layer is adequate for source-map and wiki compilation. Visual verification is still required for formulas and charts because text extraction does not preserve mathematical layout perfectly.
