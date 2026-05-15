"""Experimental Manim scenes for the Word2Vec lesson.

These scenes are intentionally simple: they use text, dots, boxes, arrows, and
short animations to support the beginner-friendly lesson. They are educational
redraws, not copies of figures from the Word2Vec paper.
"""

from __future__ import annotations

from manim import *


config.background_color = "#fbfaf7"

INK = "#1f2933"
MUTED = "#52606d"
BLUE = "#2563eb"
GREEN = "#15803d"
ORANGE = "#c2410c"
PURPLE = "#7c3aed"
RED = "#b91c1c"
BOX = "#e5e7eb"


def label(text: str, size: int = 28, color: str = INK) -> Text:
    """Small wrapper to keep typography consistent."""
    return Text(text, font_size=size, color=color, font="Arial")


def boxed_word(text: str, color: str = BLUE) -> VGroup:
    """A word label inside a stable rounded rectangle."""
    word = label(text, 28)
    rect = RoundedRectangle(
        corner_radius=0.08,
        width=max(1.1, word.width + 0.45),
        height=0.62,
        stroke_color=color,
        fill_color=WHITE,
        fill_opacity=1,
    )
    return VGroup(rect, word)


class OneHotVsDenseScene(Scene):
    """Contrast identity-only one-hot vectors with learned dense positions."""

    def construct(self) -> None:
        title = label("One-hot IDs identify words. Dense vectors can carry similarity.", 32)
        title.to_edge(UP)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        left_title = label("One-hot: separate slots", 26, BLUE)
        left_title.move_to(LEFT * 3.6 + UP * 2.0)

        right_title = label("Dense: learned map", 26, GREEN)
        right_title.move_to(RIGHT * 3.25 + UP * 2.0)

        words = ["cat", "dog", "car", "engine"]
        one_hot_rows = VGroup()
        for i, word in enumerate(words):
            word_text = label(word, 24)
            word_cell = VGroup(
                Rectangle(
                    width=1.25,
                    height=0.38,
                    stroke_opacity=0,
                    fill_opacity=0,
                ),
                word_text,
            )
            bits = VGroup()
            for j in range(4):
                square = Square(0.38, stroke_color=BOX, fill_color=WHITE, fill_opacity=1)
                if i == j:
                    square.set_fill(BLUE, opacity=0.85)
                bits.add(square)
            bits.arrange(RIGHT, buff=0.08)
            row = VGroup(word_cell, bits).arrange(RIGHT, buff=0.35)
            one_hot_rows.add(row)
        one_hot_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        one_hot_rows.move_to(LEFT * 3.45 + DOWN * 0.05)

        # The coordinates are illustrative, not paper data.
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 4, 1],
            x_length=3.6,
            y_length=2.8,
            tips=False,
            axis_config={"color": "#cbd5e1", "stroke_width": 2},
        )
        axes.move_to(RIGHT * 3.25 + DOWN * 0.05)
        dense_points = {
            "cat": (1.0, 2.7, BLUE),
            "dog": (1.5, 2.35, BLUE),
            "car": (3.45, 1.2, ORANGE),
            "engine": (4.1, 1.55, ORANGE),
        }
        dots = VGroup()
        for word, (x, y, color) in dense_points.items():
            dot = Dot(axes.c2p(x, y), color=color, radius=0.08)
            text = label(word, 22).next_to(dot, UP, buff=0.08)
            dots.add(VGroup(dot, text))

        note = label("Interpretation: nearby positions can encode useful similarity.", 22, MUTED)
        note.to_edge(DOWN)

        self.play(FadeIn(left_title), FadeIn(right_title))
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.15) for row in one_hot_rows], lag_ratio=0.12))
        self.play(Create(axes), LaggedStart(*[FadeIn(group, scale=0.8) for group in dots], lag_ratio=0.18))
        self.play(FadeIn(note, shift=UP * 0.15))
        self.wait(1.2)


class CBOWVsSkipgramScene(Scene):
    """Show the prediction directions without reversing CBOW and Skip-gram."""

    def construct(self) -> None:
        title = label("CBOW and Skip-gram use opposite prediction directions.", 34)
        title.to_edge(UP)

        sentence_words = ["the", "quick", "brown", "fox", "jumps"]
        sentence = VGroup(*[boxed_word(word, BLUE if word == "brown" else MUTED) for word in sentence_words])
        sentence.arrange(RIGHT, buff=0.12)
        sentence.move_to(UP * 1.55)
        center_box = sentence[2]

        window_brace = Brace(VGroup(sentence[1], sentence[2], sentence[3]), DOWN, color=MUTED)
        window_label = label("context window", 20, MUTED).next_to(window_brace, DOWN, buff=0.08)

        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(word, shift=UP * 0.1) for word in sentence], lag_ratio=0.08))
        self.play(GrowFromCenter(window_brace), FadeIn(window_label))

        cbow_title = label("CBOW", 30, BLUE).move_to(LEFT * 3.2 + DOWN * 0.1)
        cbow_caption = label("context -> current word", 23, MUTED).next_to(cbow_title, DOWN, buff=0.18)
        cbow_context = VGroup(boxed_word("quick", MUTED), boxed_word("fox", MUTED)).arrange(DOWN, buff=0.22)
        cbow_context.move_to(LEFT * 4.35 + DOWN * 1.75)
        cbow_target = boxed_word("brown", BLUE).move_to(LEFT * 2.35 + DOWN * 1.75)
        cbow_arrows = VGroup(
            Arrow(cbow_context[0].get_right(), cbow_target.get_left(), buff=0.12, color=BLUE),
            Arrow(cbow_context[1].get_right(), cbow_target.get_left(), buff=0.12, color=BLUE),
        )

        skip_title = label("Skip-gram", 30, GREEN).move_to(RIGHT * 3.05 + DOWN * 0.1)
        skip_caption = label("current word -> context", 23, MUTED).next_to(skip_title, DOWN, buff=0.18)
        skip_center = boxed_word("brown", GREEN).move_to(RIGHT * 2.1 + DOWN * 1.75)
        skip_targets = VGroup(boxed_word("quick", MUTED), boxed_word("fox", MUTED)).arrange(DOWN, buff=0.22)
        skip_targets.move_to(RIGHT * 4.1 + DOWN * 1.75)
        skip_arrows = VGroup(
            Arrow(skip_center.get_right(), skip_targets[0].get_left(), buff=0.12, color=GREEN),
            Arrow(skip_center.get_right(), skip_targets[1].get_left(), buff=0.12, color=GREEN),
        )

        divider = Line(UP * 0.15, DOWN * 2.7, color="#d1d5db")

        self.play(Create(divider))
        self.play(FadeIn(cbow_title), FadeIn(cbow_caption))
        self.play(FadeIn(cbow_context), FadeIn(cbow_target))
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in cbow_arrows], lag_ratio=0.15))
        self.play(FadeIn(skip_title), FadeIn(skip_caption))
        self.play(FadeIn(skip_center), FadeIn(skip_targets))
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in skip_arrows], lag_ratio=0.15))

        caution = label("Paper-grounded rule: do not swap these directions.", 22, RED)
        caution.to_edge(DOWN)
        self.play(FadeIn(caution, shift=UP * 0.15))
        self.wait(1.2)


class AnalogyVectorScene(Scene):
    """Animate analogy offsets as an empirical vector-space pattern."""

    def construct(self) -> None:
        title = label("Analogy evaluation looks for a similar vector offset.", 34)
        title.to_edge(UP)
        self.play(FadeIn(title))

        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 5, 1],
            x_length=6.6,
            y_length=4.3,
            tips=False,
            axis_config={"color": "#d1d5db", "stroke_width": 2},
        )
        axes.move_to(DOWN * 0.2)
        self.play(Create(axes))

        # Coordinates are illustrative teaching geometry, not paper vectors.
        positions = {
            "France": (1.2, 1.3),
            "Paris": (2.55, 3.25),
            "Italy": (4.15, 1.15),
            "Rome": (5.5, 3.05),
        }

        point_groups = {}
        for word, (x, y) in positions.items():
            dot = Dot(axes.c2p(x, y), radius=0.08, color=PURPLE if word in {"Paris", "Rome"} else BLUE)
            text = label(word, 23).next_to(dot, UP, buff=0.08)
            point_groups[word] = VGroup(dot, text)

        self.play(LaggedStart(*[FadeIn(group, scale=0.8) for group in point_groups.values()], lag_ratio=0.12))

        france_to_paris = Arrow(
            point_groups["France"][0].get_center(),
            point_groups["Paris"][0].get_center(),
            buff=0.12,
            color=ORANGE,
            stroke_width=5,
        )
        italy_to_rome = Arrow(
            point_groups["Italy"][0].get_center(),
            point_groups["Rome"][0].get_center(),
            buff=0.12,
            color=ORANGE,
            stroke_width=5,
        )
        relation_label = label("country -> capital offset", 24, ORANGE).move_to(UP * 2.1)

        self.play(GrowArrow(france_to_paris), FadeIn(relation_label))
        self.play(TransformFromCopy(france_to_paris, italy_to_rome))

        expression = label("Paris - France + Italy -> nearest vector: Rome", 26, INK)
        expression.to_edge(DOWN).shift(UP * 0.3)
        caveat = label("Caution: illustrative geometry, not guaranteed reasoning.", 21, RED)
        caveat.next_to(expression, DOWN, buff=0.16)

        self.play(FadeIn(expression, shift=UP * 0.12))
        self.play(FadeIn(caveat, shift=UP * 0.12))
        self.wait(1.3)
