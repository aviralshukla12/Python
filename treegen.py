# treegen.py
import os
import sys

def print_tree(start_path, prefix='', max_depth=None, current_depth=0):
    if max_depth is not None and current_depth > max_depth:
        return
    entries = sorted(os.listdir(start_path))
    for i, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        connector = '└── ' if i == len(entries) - 1 else '├── '
        print(prefix + connector + entry)
        if os.path.isdir(path):
            extension = '    ' if i == len(entries) - 1 else '│   '
            print_tree(path, prefix + extension, max_depth, current_depth + 1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python treegen.py <directory> [max_depth]")
        sys.exit(1)

    directory = sys.argv[1]
    max_depth = int(sys.argv[2]) if len(sys.argv) >= 3 else None

    if not os.path.exists(directory):
        print(f"Error: {directory} does not exist.")
        sys.exit(1)

    print_tree(directory, max_depth=max_depth)
