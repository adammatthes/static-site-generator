from textnode import TextNode, TextType
import subprocess
import os
import shutil
from markdownblocks import markdown_to_html_alt, extract_title
import sys

try:
    basepath = sys.argv[1]
except IndexError:
    basepath = '/'



def copy_static_to_public():
    files_to_delete = []
    for p, d, f in os.walk('docs'):
        for f1 in f:
            files_to_delete.append(f'{p}/{f1}')

    for f in files_to_delete:
        subprocess.run(['rm', f])

    files_to_copy = []
    new_file_paths = []
    new_dirs = []
    for p, d, f in os.walk('static'):
        for d1 in d:
            new_dirs.append(f'{p.replace("static", "docs")}/{d1}')
        for f1 in f:
            files_to_copy.append(f'{p}/{f1}')
            new_file_paths.append(f'{p.replace("static", "docs")}/{f1}')

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}")

    with open(from_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    html_result = markdown_to_html_alt(markdown_content)

    page_title = extract_title(markdown_content)

    template_content = template_content.replace('{{ Title }}', page_title)\
                        .replace('{{ Content }}', html_result)

    global basepath
    html_result = html_result.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')


    with open(dest_path, 'w') as html_file:
        html_file.write(html_result)


def main():

    try:
        subprocess.run(['rm', '-rf', 'docs/*'])
    except Exception as e:
        print(e)

        copy_static_to_public()

    for p, d, f in os.walk('content'):
        try:
            subprocess.run(['mkdir', p.replace('content', 'docs')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(e)
        
        for f1 in f:
            generate_page(f'{p}/{f1}', 'template.html', f'{p.replace("content", "docs")}/{f1.replace("md", "html")}')

if __name__ == "__main__":
    main()
