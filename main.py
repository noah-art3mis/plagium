import argparse
from similarity import ngram_similarity, levenshtein_similarity, lcs_similarity


def main(file1_path, file2_path):
    try:
        with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
            s1 = f1.read()
            s2 = f2.read()
            
        print("N-gram similarity:", ngram_similarity(s1, s2, n=3))
        print("Levenshtein similarity:", levenshtein_similarity(s1, s2))
        print("LCS similarity:", lcs_similarity(s1, s2))
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare similarity between two text files')
    parser.add_argument('file1', help='Path to first file')
    parser.add_argument('file2', help='Path to second file')
    
    args = parser.parse_args()
    main(args.file1, args.file2)
