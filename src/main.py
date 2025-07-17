from textnode import TextNode, TextType
import subprocess
import os
import shutil
from markdownblocks import markdown_to_html_alt


def copy_static_to_public():
    files_to_delete = []
    for p, d, f in os.walk('public'):
        for f1 in f:
            files_to_delete.append(f'{p}/{f1}')

    for f in files_to_delete:
        subprocess.run(['rm', f])

    files_to_copy = []
    new_file_paths = []
    new_dirs = []
    for p, d, f in os.walk('static'):
        for d1 in d:
            new_dirs.append(f'{p.replace("static", "public")}/{d1}')
        for f1 in f:
            files_to_copy.append(f'{p}/{f1}')
            new_file_paths.append(f'{p.replace("static", "public")}/{f1}')

    for nd in new_dirs:
        try:
            subprocess.run(['mkdir', nd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    for old, new in zip(files_to_copy, new_file_paths):
        if old.endswith(('jpg', 'png')):
            shutil.copy(old, new)
        else:
            with open(old, 'r') as old_file:
                content = old_file.read()
                with open(new, 'w') as new_file:
                    new_file.write(content)




def main():

    with open('content/index.md', 'r') as markdown_file:
        print(markdown_to_html_alt(markdown_file.read()))
    #copy_static_to_public()

if __name__ == "__main__":
    main()
