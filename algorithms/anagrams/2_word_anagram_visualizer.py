#!/usr/bin/env python3

"""
Below is a small Python two-word anagram visualizer. 
It normalizes case or spaces, then animates letter frequency counts 
so you can see why two inputs are or are not anagrams.

Author: Ulises Violante
Created: 2026-09-24
Version: 0.0.1
"""



import os
import time
from collections import Counter


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def normalize(text: str) -> str:
    # Keep letters only with lowercase; ignore spaces, punctuation, and capitalization.
    return "".join(char.lower() for char in text if char.isalpha())

def visualize_anagram(word1: str, word2: str, delay: float = 0.6):
    a = normalize(word1)
    b = normalize(word2)

    clear()

    print(f"Original inputs: {word1!r}  vs  {word2!r}")
    print(f"Normalized:      {a!r}  vs  {b!r}\n")

    if len(a) != len(b):
        print(f"❌ Not anagrams: lengths differ ({len(a)} vs {len(b)}).")
        return

    counts = Counter()

    for i, (left, right) in enumerate(zip(a, b), start=1):
        counts[left] += 1
        counts[right] -= 1

        # clear() ## Uncomment to clear the output before each step.
        print("TWO-WORD ANAGRAM VISUALIZER")
        print("=" * 35)
        print(f"Word 1: {a}")
        print(f"Word 2: {b}")
        print(f"\nStep {i}/{len(a)}")
        print(f"Add from word 1:    {left!r}  (+1)")
        print(f"Remove from word 2: {right!r}  (-1)\n")

        active = {letter: count for letter, count in sorted(counts.items()) if count != 0}
        print("Running letter balance:")
        print(active if active else "✅ Balanced so far")

        input("\nPress Enter to continue...")

    clear()
    print("FINAL RESULT")
    print("=" * 35)
    print(f"{word1!r}  vs  {word2!r}")
    print()

    if all(count == 0 for count in counts.values()):
        print("✅ They are anagrams.")
        print("Every letter appears the same number of times in both words.")
    else:
        print("❌ They are not anagrams.")
        print("Unmatched letter counts:")
        print({letter: count for letter, count in sorted(counts.items()) if count != 0})


visualize_anagram("listen", "silent")

