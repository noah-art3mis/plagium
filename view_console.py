import difflib


def print_console_diff(original: str, rewritten: str):
    """Print a colored diff in the console"""
    differ = difflib.unified_diff(
        original.splitlines(keepends=True),
        rewritten.splitlines(keepends=True),
        fromfile="Original Text",
        tofile="Rewritten Text",
        lineterm="",
    )

    print("=" * 80)
    print("CONSOLE DIFF VIEW")
    print("=" * 80)
    print("Legend: - = removed, + = added")
    print("-" * 80)

    for line in differ:
        if line.startswith("---") or line.startswith("+++"):
            print(f"\033[1m{line.rstrip()}\033[0m")  # Bold for headers
        elif line.startswith("-"):
            print(f"\033[91m{line.rstrip()}\033[0m")  # Red for deletions
        elif line.startswith("+"):
            print(f"\033[92m{line.rstrip()}\033[0m")  # Green for additions
        elif line.startswith("@@"):
            print(f"\033[94m{line.rstrip()}\033[0m")  # Blue for hunk headers
        else:
            print(line.rstrip())  # Context lines

    print("-" * 80)


def print_side_by_side_console(original: str, rewritten: str):
    """Print a side-by-side diff in the console"""
    from difflib import SequenceMatcher

    print("=" * 100)
    print("SIDE-BY-SIDE CONSOLE DIFF")
    print("=" * 100)
    print(f"{'ORIGINAL':<50} | {'REWRITTEN':<50}")
    print("-" * 100)

    matcher = SequenceMatcher(None, original.splitlines(), rewritten.splitlines())
    orig_lines = original.splitlines()
    rewrit_lines = rewritten.splitlines()

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for k in range(i1, i2):
                orig_line = (
                    orig_lines[k][:48] + ".."
                    if len(orig_lines[k]) > 50
                    else orig_lines[k]
                )
                rewrit_line = (
                    rewrit_lines[j1 + k - i1][:48] + ".."
                    if len(rewrit_lines[j1 + k - i1]) > 50
                    else rewrit_lines[j1 + k - i1]
                )
                print(f"{orig_line:<50} | {rewrit_line:<50}")

        elif tag == "delete":
            for k in range(i1, i2):
                orig_line = (
                    orig_lines[k][:48] + ".."
                    if len(orig_lines[k]) > 50
                    else orig_lines[k]
                )
                print(f"\033[91m{orig_line:<50}\033[0m | {'':<50}")  # Red for deletions

        elif tag == "insert":
            for k in range(j1, j2):
                rewrit_line = (
                    rewrit_lines[k][:48] + ".."
                    if len(rewrit_lines[k]) > 50
                    else rewrit_lines[k]
                )
                print(
                    f"{'':<50} | \033[92m{rewrit_line:<50}\033[0m"
                )  # Green for additions

        elif tag == "replace":
            for k in range(i1, i2):
                orig_line = (
                    orig_lines[k][:48] + ".."
                    if len(orig_lines[k]) > 50
                    else orig_lines[k]
                )
                print(f"\033[91m{orig_line:<50}\033[0m | {'':<50}")  # Red for deletions
            for k in range(j1, j2):
                rewrit_line = (
                    rewrit_lines[k][:48] + ".."
                    if len(rewrit_lines[k]) > 50
                    else rewrit_lines[k]
                )
                print(
                    f"{'':<50} | \033[92m{rewrit_line:<50}\033[0m"
                )  # Green for additions

    print("-" * 100)


def print_word_level_diff(original: str, rewritten: str):
    """Print a word-level diff showing specific changes"""
    from difflib import SequenceMatcher

    print("=" * 80)
    print("WORD-LEVEL DIFF")
    print("=" * 80)

    orig_words = original.split()
    rewrit_words = rewritten.split()
    matcher = SequenceMatcher(None, orig_words, rewrit_words)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            words = orig_words[i1:i2]
            if len(words) > 10:
                words = words[:5] + ["..."] + words[-5:]
            print(" ".join(words), end=" ")

        elif tag == "delete":
            words = orig_words[i1:i2]
            print(f"\033[91m[DELETED: {' '.join(words)}]\033[0m", end=" ")

        elif tag == "insert":
            words = rewrit_words[j1:j2]
            print(f"\033[92m[ADDED: {' '.join(words)}]\033[0m", end=" ")

        elif tag == "replace":
            orig_words_section = orig_words[i1:i2]
            rewrit_words_section = rewrit_words[j1:j2]
            print(f"\033[91m[DELETED: {' '.join(orig_words_section)}]\033[0m", end=" ")
            print(f"\033[92m[ADDED: {' '.join(rewrit_words_section)}]\033[0m", end=" ")

    print("\n" + "=" * 80)


def print_character_diff(original: str, rewritten: str):
    """Print character-level differences"""
    from difflib import SequenceMatcher

    matcher = SequenceMatcher(None, original, rewritten)

    print("=" * 80)
    print("CHARACTER-LEVEL DIFF")
    print("=" * 80)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            print(original[i1:i2], end="")
        elif tag == "delete":
            print(f"\033[91m{original[i1:i2]}\033[0m", end="")  # Red for deletions
        elif tag == "insert":
            print(f"\033[92m{rewritten[j1:j2]}\033[0m", end="")  # Green for additions
        elif tag == "replace":
            print(f"\033[91m{original[i1:i2]}\033[0m", end="")  # Red for deletions
            print(f"\033[92m{rewritten[j1:j2]}\033[0m", end="")  # Green for additions

    print("\n" + "=" * 80)
