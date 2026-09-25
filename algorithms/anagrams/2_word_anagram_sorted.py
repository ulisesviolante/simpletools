#!/usr/bin/env python3

"""
Compares 2 str to match an Anangram.

Using sorted() compares the characters after putting them into
alphabetical order, rather than counting the frequency of each
character directly.

This runs in O(n log n) time because both normalized words must be
sorted, and it uses O(n) extra space for the sorted character
sequences, where n is the length of the words.

Author: Ulises Violante
Created: 2026-09-24
Version: 0.0.1
"""


def are_anagrams_sorted(word1: str, word2: str) -> bool:

    clean1 = "".join(ch.lower() for ch in word1 if ch.isalpha())
    clean2 = "".join(ch.lower() for ch in word2 if ch.isalpha())

    return sorted(clean1) == sorted(clean2)



print(
    f"'Dormitory' vs 'Dirty room' -> {are_anagrams_sorted('Dormitory', 'Dirty room')}"
)  # True
print(f"'python' vs 'typhon' -> {are_anagrams_sorted('python', 'typhon')}")  # True
print(f"'python' vs 'java' -> {are_anagrams_sorted('python', 'java')}")  # False
