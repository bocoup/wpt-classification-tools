#!/usr/bin/env python3
"""
Generate a markdown report from git grep search results.
Shows context around matches with clickable links.
"""

import os
import sys
import re
from collections import defaultdict
from pathlib import Path


def extract_title(filepath):
    """Extract title or description from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(2000)  # Read first 2000 chars

            # Try to extract HTML title
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                return title_match.group(1).strip()

            # Try to find comment at top of file
            comment_match = re.search(r'^(?://|#|/\*)\s*(.+?)(?:\*/|$)', content, re.MULTILINE)
            if comment_match:
                return comment_match.group(1).strip()

            # For test files, look for test() or describe() calls
            test_match = re.search(r'(?:test|describe)\(["\'](.+?)["\']', content)
            if test_match:
                return test_match.group(1).strip()

    except Exception:
        pass

    return None


def get_file_context(filepath, line_num, context_lines=1):
    """Get lines of context around a specific line number."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        start = max(0, line_num - context_lines - 1)
        end = min(len(lines), line_num + context_lines)

        context = []
        for i in range(start, end):
            line_content = lines[i].rstrip()
            context.append((i + 1, line_content))

        return context
    except Exception:
        return []


def find_line_number(filepath, search_content):
    """Find the line number for a specific content in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if search_content.strip() in line:
                    return line_num
    except Exception:
        pass
    return None


def parse_grep_output(grep_file):
    """Parse git grep output file."""
    results = defaultdict(list)

    with open(grep_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Try format with line number: filepath:line_number:content
            match_with_num = re.match(r'^([^:]+):(\d+):(.*)$', line)
            if match_with_num:
                filepath = match_with_num.group(1)
                line_num = int(match_with_num.group(2))
                content = match_with_num.group(3)

                results[filepath].append({
                    'line_num': line_num,
                    'content': content
                })
            else:
                # Try format without line number: filepath:content
                match_without_num = re.match(r'^([^:]+):(.*)$', line)
                if match_without_num:
                    filepath = match_without_num.group(1)
                    content = match_without_num.group(2)

                    # Find the line number in the file
                    line_num = find_line_number(filepath, content)
                    if line_num:
                        results[filepath].append({
                            'line_num': line_num,
                            'content': content
                        })

    return results


def generate_markdown_report(grep_file, feature_name):
    """Generate markdown report from grep results."""
    results = parse_grep_output(grep_file)

    # GitHub base URL
    GITHUB_BASE = "https://github.com/web-platform-tests/wpt/blob/master"

    # Group by directory
    by_directory = defaultdict(list)
    for filepath in sorted(results.keys()):
        directory = os.path.dirname(filepath) or '.'
        by_directory[directory].append(filepath)

    # Generate markdown
    output = [f"# {feature_name} Search Results\n"]
    output.append(f"*Generated from {os.path.basename(grep_file)}*\n")
    output.append(f"**Total files found:** {len(results)}\n")

    for directory in sorted(by_directory.keys()):
        output.append(f"\n## Directory: `{directory}`\n")

        for filepath in sorted(by_directory[directory]):
            # Use full filepath in heading with GitHub URL
            github_url = f"{GITHUB_BASE}/{filepath}"
            output.append(f"\n### [{filepath}]({github_url})\n")

            # Try to extract title/description
            title = extract_title(filepath)
            if title:
                output.append(f"**Description:** {title}\n")

            # Show matches with context
            matches = results[filepath]
            for match in matches:
                line_num = match['line_num']
                context = get_file_context(filepath, line_num, context_lines=1)

                if context:
                    output.append("\n```")
                    for ctx_line_num, ctx_content in context:
                        prefix = "→" if ctx_line_num == line_num else " "
                        output.append(f"{prefix} {ctx_line_num:4d} | {ctx_content}")
                    output.append("```")
                    # Use GitHub URL with line number
                    output.append(f"[View in file]({github_url}#L{line_num})\n")

    return '\n'.join(output)


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_search_report.py <grep_file> <feature_name>")
        sys.exit(1)

    grep_file = sys.argv[1]
    feature_name = sys.argv[2]

    if not os.path.exists(grep_file):
        print(f"Error: File {grep_file} not found")
        sys.exit(1)

    markdown = generate_markdown_report(grep_file, feature_name)

    # Write to file
    output_file = grep_file.replace('.txt', '-report.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"Report generated: {output_file}")


if __name__ == '__main__':
    main()
