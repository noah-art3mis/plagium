import argparse

from dotenv import load_dotenv

from ai_rewriter import rewrite
from similarity import lcs_similarity, levenshtein_similarity, ngram_similarity
from utils.io import get_data
from view_console import print_character_diff, print_word_level_diff

models = [
    "anthropic:claude-opus-4-1-20250805",
    "anthropic:claude-sonnet-4-5-20250929",
    "anthropic:claude-3-5-haiku-20241022",
    "google_genai:gemini-2.5-pro",
    "google_genai:gemini-2.5-flash",
    "google_genai:gemini-2.5-flash-lite",
    "openai:gpt-5",
    "openai:gpt-5-mini",
    "openai:gpt-5-nano",
    "openai:gpt-4.1",
    "openai:gpt-4-mini",
    "openai:gpt-4-nano",
    "openai:gpt-4o",
    "openai:gpt-4o-mini",
    "openai:o1",
    "openai:o1-mini",
    "openai:o3",
    "openai:o3-mini",
    "openai:o4",
]


def compare(file1_path: str):

    s1 = get_data(file1_path)

    s2 = rewrite(
        prompt_template=r"Rewrite: {text}",
        snippet=s1,
        model="openai:gpt-5",
        temperature=0.0,
    )

    ngram = ngram_similarity(s1, s2, n=3)
    levenshtein = levenshtein_similarity(s1, s2)
    lcs = lcs_similarity(s1, s2)

    print_word_level_diff(s1, s2)
    # print_character_diff(s1, s2)

    print(
        "(N-gram similarity measures the overlap of character sequences, where higher values indicate more similar texts)"
    )
    print(f"N-gram similarity: {ngram:.3f}")
    print(
        "(Levenshtein similarity measures the minimum number of single-character edits needed to transform one string into the other, where lower values indicate more similar texts)"
    )
    print(f"Levenshtein similarity: {levenshtein:.3f}")
    print(
        "(LCS similarity measures the longest common subsequence between two strings, where higher values indicate more similar texts)"
    )
    print(f"LCS similarity: {lcs:.3f}")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Compare similarity between original and AI-rewritten text"
    )
    parser.add_argument("file", help="Path to file")

    args = parser.parse_args()
    compare(args.file)


if __name__ == "__main__":
    main()
