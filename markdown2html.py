#!/usr/bin/python3
"""
Converts Markdown to HTML
"""
import sys
import re
from hashlib import md5
from os.path import exists

def parse_arguments():
    """Check the script arguments for correctness."""
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)
    if not exists(sys.argv[1]):
        sys.stderr.write(f"Missing {sys.argv[1]}\n")
        sys.exit(1)

def parse_markdown_to_html(markdown):
    """Convert markdown text to HTML format."""
    html_content = []
    in_list = None  # Tracks the type of list we are in ('ul' or 'ol')

    for line in markdown:
        line = line.rstrip()
        if not line:
            continue

        # Headings
        if line.startswith('#'):
            level = line.count('#') - line.find(' ')
            content = line.split(' ', 1)[1]
            html_content.append(f"<h{level}>{content}</h{level}>")
        
        # Unordered List
        elif line.startswith('-'):
            if in_list != 'ul':
                if in_list:
                    html_content.append(f"</{in_list}>")
                html_content.append("<ul>")
                in_list = 'ul'
            html_content.append(f"<li>{line[2:]}</li>")
        
        # Ordered List
        elif line.startswith('*'):
            if in_list != 'ol':
                if in_list:
                    html_content.append(f"</{in_list}>")
                html_content.append("<ol>")
                in_list = 'ol'
            html_content.append(f"<li>{line[2:]}</li>")

        # Paragraphs and line breaks
        else:
            if in_list:
                html_content.append(f"</{in_list}>")
                in_list = None
            # Replace markdown with HTML tags
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'__([^_]*)__', r'<em>\1</em>', line)
            line = re.sub(r'\[\[(.*?)\]\]', lambda m: md5(m.group(1).encode()).hexdigest(), line)
            line = re.sub(r'\(\((.*?)\)\)', lambda m: re.sub('[cC]', '', m.group(1)), line)
            html_content.append(f"<p>{line}</p>")

    if in_list:
        html_content.append(f"</{in_list}>")

    return '\n'.join(html_content) + '\n'

def main():
    parse_arguments()
    with open(sys.argv[1], 'r') as markdown_file:
        markdown = markdown_file.readlines()
    html_content = parse_markdown_to_html(markdown)
    with open(sys.argv[2], 'w') as html_file:
        html_file.write(html_content)

if __name__ == "__main__":
    main()

