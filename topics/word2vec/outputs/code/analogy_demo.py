#!/usr/bin/env python3
"""
Demonstrate cosine similarity and analogy-style vector arithmetic.

This script uses tiny hand-made vectors so the arithmetic is easy to inspect.
It does not use vectors from the Word2Vec paper and does not reproduce the
paper's large-scale results.

The point is only to separate the evaluation mechanics from model training:
1. form a vector expression,
2. compare candidates with cosine similarity,
3. choose the nearest vector.
"""

from __future__ import annotations

import math


Vector = tuple[float, float]


def add(left: Vector, right: Vector) -> Vector:
    return (left[0] + right[0], left[1] + right[1])


def subtract(left: Vector, right: Vector) -> Vector:
    return (left[0] - right[0], left[1] - right[1])


def cosine_similarity(left: Vector, right: Vector) -> float:
    """Return cosine similarity for two small vectors."""
    dot = left[0] * right[0] + left[1] * right[1]
    left_length = math.sqrt(left[0] ** 2 + left[1] ** 2)
    right_length = math.sqrt(right[0] ** 2 + right[1] ** 2)

    if left_length == 0 or right_length == 0:
        return 0.0

    return dot / (left_length * right_length)


def nearest_word(
    query: Vector,
    vectors: dict[str, Vector],
    excluded_words: set[str],
) -> tuple[str, float]:
    """Find the nearest candidate by cosine similarity."""
    best_word = ""
    best_score = -2.0

    for word, vector in vectors.items():
        if word in excluded_words:
            continue

        score = cosine_similarity(query, vector)
        if score > best_score:
            best_word = word
            best_score = score

    return best_word, best_score


def main() -> None:
    # Hand-made 2D vectors with two loose directions:
    # x-axis: country-like location
    # y-axis: capital-city-like location
    #
    # These numbers are illustrative. Real word vectors are learned from data
    # and have many more dimensions.
    vectors: dict[str, Vector] = {
        "france": (1.0, 0.0),
        "paris": (1.0, 1.0),
        "italy": (2.0, 0.0),
        "rome": (2.0, 1.0),
        "germany": (3.0, 0.0),
        "berlin": (3.0, 1.0),
        "dog": (0.2, -1.0),
    }

    # Paper-style analogy expression:
    # Paris - France + Italy should land near Rome in this toy space.
    query = add(subtract(vectors["paris"], vectors["france"]), vectors["italy"])
    excluded = {"paris", "france", "italy"}
    word, score = nearest_word(query, vectors, excluded)

    print("Analogy-style query:")
    print("  paris - france + italy")
    print()
    print(f"Query vector: ({query[0]:.1f}, {query[1]:.1f})")
    print(f"Nearest word by cosine similarity: {word} (score {score:.3f})")
    print()
    print("Candidate scores:")
    for candidate, vector in vectors.items():
        if candidate in excluded:
            continue
        print(f"  {candidate:7s} {cosine_similarity(query, vector):.3f}")

    print(
        "\nNote: this is a hand-made teaching example. It shows the evaluation "
        "mechanic, not evidence that tiny vectors understand geography."
    )


if __name__ == "__main__":
    main()
