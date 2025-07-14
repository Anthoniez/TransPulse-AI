# generate_tree.py

import os

def print_tree(directory, prefix=""):
    items = sorted(os.listdir(directory))
    ignore = {'__pycache__', '.git', 'transpulse', '.DS_Store'}
    for index, item in enumerate(items):
        if item in ignore or item.endswith(('.csv', '.pkl', '.json')):
            continue
        path = os.path.join(directory, item)
        is_last = index == len(items) - 1
        connector = '└── ' if is_last else '├── '
        print(prefix + connector + item)
        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            print_tree(path, prefix + extension)

# Run from project root
print_tree(".")
