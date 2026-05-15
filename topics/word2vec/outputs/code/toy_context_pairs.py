#!/usr/bin/env python3
"""
Generate tiny CBOW and Skip-gram training examples.

This script is intentionally small and educational. It does not train a model.
It only shows how an ordinary sentence can be turned into the prediction tasks
used to teach word vectors.

Paper-grounded directions:
- CBOW: surrounding context words -> current/middle word
- Skip-gram: current/middle word -> surrounding context words
"""

from __future__ import annotations


def labeled_token(tokens: list[str], index: int) -> str:
    """Show token position so repeated words stay easy to distinguish."""
    return f"{tokens[index]}@{index}"


def context_window(tokens: list[str], center_index: int, radius: int) -> list[str]:
    """Return nearby words around one center token, excluding the center token."""
    start = max(0, center_index - radius)
    end = min(len(tokens), center_index + radius + 1)

    return [
        labeled_token(tokens, index)
        for index, token in enumerate(tokens[start:end], start=start)
        if index != center_index
    ]


def cbow_examples(tokens: list[str], radius: int) -> list[tuple[tuple[str, ...], str]]:
    """
    Create CBOW examples.

    Each example is:
        (context words, target current word)

    Example:
        (("quick", "brown", "jumps", "over"), "fox")
    """
    examples = []

    for center_index, center_word in enumerate(tokens):
        context = context_window(tokens, center_index, radius)

        # Boundary words have smaller contexts. We keep them so beginners can
        # see what happens at the start and end of a sentence.
        if context:
            examples.append((tuple(context), labeled_token(tokens, center_index)))

    return examples


def skipgram_examples(tokens: list[str], radius: int) -> list[tuple[str, str]]:
    """
    Create Skip-gram examples.

    Each example is:
        (current word, one surrounding context word)

    Example:
        ("fox", "brown")
        ("fox", "jumps")
    """
    examples = []

    for center_index, center_word in enumerate(tokens):
        for context_word in context_window(tokens, center_index, radius):
            examples.append((labeled_token(tokens, center_index), context_word))

    return examples


def print_cbow(examples: list[tuple[tuple[str, ...], str]]) -> None:
    print("CBOW examples: context words -> current word")
    for context, target in examples:
        context_text = ", ".join(context)
        print(f"  [{context_text}] -> {target}")


def print_skipgram(examples: list[tuple[str, str]]) -> None:
    print("\nSkip-gram examples: current word -> surrounding word")
    for center, context in examples:
        print(f"  {center} -> {context}")


def main() -> None:
    sentence = "the quick brown fox jumps over the lazy dog"
    tokens = sentence.split()
    radius = 2

    print(f"Sentence: {sentence}")
    print(f"Window radius: {radius}")
    print("Token labels use word@index so repeated words stay distinct.")
    print()

    print_cbow(cbow_examples(tokens, radius))
    print_skipgram(skipgram_examples(tokens, radius))

    print(
        "\nNote: these are toy training examples only. The paper trains on very "
        "large corpora; this script is only meant to clarify prediction direction."
    )


if __name__ == "__main__":
    main()
