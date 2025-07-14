import os
import sys

def tree(dir_path: str, prefix: str = "", max_depth: int = -1, level: int = 0):
    if max_depth != -1 and level > max_depth:
        return
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        print(prefix + "└─ [Permission Denied]")
        return

    for i, name in enumerate(entries):
        path = os.path.join(dir_path, name)
        connector = "└─" if i == len(entries) - 1 else "├─"
        print(prefix + connector + " " + name)

        if os.path.isdir(path):
            extension = "    " if i == len(entries) - 1 else "│   "
            tree(path, prefix + extension, max_depth, level + 1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python treegen.py <directory> [max_depth]")
        sys.exit(1)
    root = sys.argv[1]
    depth = int(sys.argv[2]) if len(sys.argv) >= 3 else -1

    print(root)
    tree(root, "", depth)

if __name__ == "__main__":
    main()
