# Experimental Manim Animations: Word2Vec

These files contain experimental Manim Community Edition scenes for the reviewed Word2Vec lesson. They are intended for later review before embedding in a blog post or using in a YouTube explanation.

## Scenes

- `OneHotVsDenseScene`
  - Contrasts one-hot word identity with an illustrative dense-vector map.
  - Teaching purpose: motivate why dense learned vectors can carry similarity information.

- `CBOWVsSkipgramScene`
  - Shows the two Word2Vec prediction directions side by side.
  - Teaching purpose: preserve the paper-grounded distinction that CBOW predicts the current word from context, while Skip-gram predicts surrounding context from the current word.

- `AnalogyVectorScene`
  - Shows analogy evaluation as a reusable vector offset.
  - Teaching purpose: explain `Paris - France + Italy -> Rome` as nearest-neighbor search over an empirical vector-space pattern, not symbolic reasoning.

## Render Commands

Use the repo virtual environment explicitly:

```bash
.venv/bin/manim -ql topics/word2vec/outputs/manim/word2vec_scenes.py OneHotVsDenseScene
.venv/bin/manim -ql topics/word2vec/outputs/manim/word2vec_scenes.py CBOWVsSkipgramScene
.venv/bin/manim -ql topics/word2vec/outputs/manim/word2vec_scenes.py AnalogyVectorScene
```

To render directly into the topic media folder, add `--media_dir`:

```bash
.venv/bin/manim -ql --media_dir topics/word2vec/outputs/manim_media topics/word2vec/outputs/manim/word2vec_scenes.py OneHotVsDenseScene
.venv/bin/manim -ql --media_dir topics/word2vec/outputs/manim_media topics/word2vec/outputs/manim/word2vec_scenes.py CBOWVsSkipgramScene
.venv/bin/manim -ql --media_dir topics/word2vec/outputs/manim_media topics/word2vec/outputs/manim/word2vec_scenes.py AnalogyVectorScene
```

## Output Location

Low-quality preview renders should appear under:

```text
topics/word2vec/outputs/manim_media/videos/word2vec_scenes/480p15/
```

The expected MP4 filenames are:

- `OneHotVsDenseScene.mp4`
- `CBOWVsSkipgramScene.mp4`
- `AnalogyVectorScene.mp4`

For convenience, the latest successful low-quality renders were also copied to:

```text
topics/word2vec/outputs/manim_media/OneHotVsDenseScene.mp4
topics/word2vec/outputs/manim_media/CBOWVsSkipgramScene.mp4
topics/word2vec/outputs/manim_media/AnalogyVectorScene.mp4
```

## Render Status

Rendered successfully with:

```text
Manim Community v0.19.1
```

Commands used:

```bash
.venv/bin/manim -ql --media_dir topics/word2vec/outputs/manim_media topics/word2vec/outputs/manim/word2vec_scenes.py OneHotVsDenseScene
.venv/bin/manim -ql --media_dir topics/word2vec/outputs/manim_media topics/word2vec/outputs/manim/word2vec_scenes.py CBOWVsSkipgramScene
.venv/bin/manim -ql --media_dir topics/word2vec/outputs/manim_media topics/word2vec/outputs/manim/word2vec_scenes.py AnalogyVectorScene
```

## Experimental Review Notes

- The scenes use simple Manim objects: `Text`, `Dot`, `Square`, `RoundedRectangle`, `Arrow`, `Line`, `Axes`, and `Brace`.
- They avoid LaTeX-heavy rendering.
- Dense-vector coordinates and analogy geometry are illustrative teaching geometry, not paper data.
- The scenes are not copied from the paper's diagrams.
- Before publishing, review text fit, pacing, colors, and mobile/video readability.
- If rendering fails because of system dependencies, check `ffmpeg`, Cairo, and Pango availability. On macOS these may need Homebrew installation outside the Python environment.
