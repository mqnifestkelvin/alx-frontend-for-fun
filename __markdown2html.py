#!/usr/bin/python3
"""
Module for converting markdown to HTML.
"""

import re
import sys
from os.path import exists
from hashlib import md5

def parse_heading(line):
    """Converts markdown headings to HTML headings."""
    level = line.count('#', 0, line.find(' '))
    content = line.strip().split(' ', 1)[1].strip()
    return f"<h{level}>{content}</h{level}>\n"

def parse_list_item(line):
    """Converts markdown list items to HTML list items."""
    content = line.strip()[1:].strip()
    return f"<li>{content}</li>\n"

def style_content(line):
    """Applies HTML styles to markdown content."""
    # Bold and Italic
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__([^_]*)__', r'<em>\1</em>', line)

    # Custom transformations
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: md5(m.group(1).encode()).hexdigest(), line)
    line = re.sub(r'\(\((.*?)\)\)', lambda m: re.sub('[cC]', '', m.group(1)), line)

    return line

def parse_markdown(markdown, flags):
    """Parses markdown lines and converts them to HTML."""
    html = []
    i = 0
    while i < len(markdown):
        line = markdown[i].rstrip()

        if line.startswith('#'):
            html.append(parse_heading(line))
        elif line.startswith('-'):
            list_items = []
            while i < len(markdown) and markdown[i].startswith('-'):
                list_items.append(parse_list_item(markdown[i].rstrip()))
                i += 1
            i -= 1  # adjust because of the outer loop increment
            html.append(f"<ul>\n{''.join(list_items)}</ul>\n")
        elif line.strip():
            paragraph = "<p>\n"
            while i < len(markdown) and markdown[i].strip() and not markdown[i].startswith(('#', '-', '*')):
                paragraph += style_content(markdown[i].rstrip()) + "\n"
                i += 1
                if i < len(markdown) and markdown[i].strip() and not markdown[i].startswith(('#', '-', '*', '\n')):
                    paragraph += "<br/>\n"
            i -= 1  # adjust because of the outer loop increment
            paragraph += "</p>\n"
            html.append(paragraph)

        i += 1

    return ''.join(html)

def markdown_to_html(input_file, output_file, flags):
    """Main function to convert markdown file to HTML file."""
    with open(input_file, 'r') as f:
        markdown = f.readlines()

    html_content = parse_markdown(markdown, flags)

    with open(output_file, 'w') as f:
        f.write(html_content)

def main():
    """Entry point of the script."""
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    if not exists(sys.argv[1]):
        sys.stderr.write(f"Missing {sys.argv[1]}\n")
        sys.exit(1)

    markdown_to_html(sys.argv[1], sys.argv[2], sys.argv[3:])

if __name__ == "__main__":
    main()

