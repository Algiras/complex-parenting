import glob


def check_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    errors = []
    for i, line in enumerate(content.splitlines()):
        for char in line:
            # Check for the specific replacement character reported
            if char == "\ufffd" or char == "\x00":
                errors.append(f"Line {i + 1}: Invalid char {repr(char)}")
            # Check for other potentially problematic control chars (excluding tab)
            elif ord(char) < 32 and char not in ("\t", "\n", "\r"):
                errors.append(f"Line {i + 1}: Control char {repr(char)}")

    return errors


def main():
    files = glob.glob("books/*.qmd")
    all_errors = {}

    print(f"Scanning {len(files)} files for invalid characters...")

    for file in files:
        errors = check_file(file)
        if errors:
            all_errors[file] = errors

    if all_errors:
        print("\nFound invalid characters:")
        for file, errs in all_errors.items():
            print(f"\n{file}:")
            for err in errs:
                print(f"  - {err}")
    else:
        print("\nNo invalid characters found.")


if __name__ == "__main__":
    main()
