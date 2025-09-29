from difflib import SequenceMatcher
import Levenshtein


# -------------------------------
# 1. N-gram Jaccard similarity
# -------------------------------
def ngram_similarity(s1, s2, n=3):
    def ngrams(text, n):
        tokens = text.lower().split()
        return set(tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1))

    ngrams1 = ngrams(s1, n)
    ngrams2 = ngrams(s2, n)

    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)

    return intersection / union if union > 0 else 0.0


# -------------------------------
# 2. Levenshtein similarity
# -------------------------------
def levenshtein_similarity(s1, s2):
    distance = Levenshtein.distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1 - distance / max_len if max_len > 0 else 1.0


# -------------------------------
# 3. Longest Common Subsequence (LCS)
# -------------------------------
def lcs_similarity(s1, s2):
    # Using difflib SequenceMatcher (approx LCS)
    matcher = SequenceMatcher(None, s1, s2)
    # Fixed: get_matching_blocks() returns tuples (i, j, n), not objects with .size
    lcs_len = sum(n for i, j, n in matcher.get_matching_blocks())
    max_len = max(len(s1), len(s2))
    return lcs_len / max_len if max_len > 0 else 1.0


# Alternative simpler approach using ratio():
# def lcs_similarity(s1, s2):
#     matcher = SequenceMatcher(None, s1, s2)
#     return matcher.ratio()
