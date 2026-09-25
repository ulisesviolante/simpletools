#!/usr/bin/env python3

"""
Using Counter compares the frequency of each character directly, rather than relying on letter order.
This runs in O(n) time for the two normalized words and uses O(k) extra space,
where k is the number of distinct characters.

Author: Ulises Violante
Created: 2026-09-24
Version: 0.0.1
"""

from collections import Counter


def are_anagrams(word1: str, word2: str) -> bool:
    normalize = lambda s: "".join(ch.lower() for ch in s if ch.isalpha())
    return Counter(normalize(word1)) == Counter(normalize(word2))


print(
    f"'Dormitory' vs 'Dirty room' -> {are_anagrams('Dormitory', 'Dirty room')}"
)  # True
print(f"'python' vs 'typhon' -> {are_anagrams('python', 'typhon')}")  # True
print(f"'python' vs 'java' -> {are_anagrams('python', 'java')}")  # False
