#!/usr/bin/env python3
"""
Generate WEB_FEATURES.yml files from a list of test file paths.
Based on wpt-generate from wpt-classification-tools.

This script merges with existing WEB_FEATURES.yml files instead of overwriting them.
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import yaml


def grep_match_line_to_filename(line):
    """Extract filename from a grep-style match line or plain filepath."""
    if ':' in line:
        return line.split(':', 1)[0]
    return line.strip()


def compare_filepaths(path1, path2):
    """Compare file paths for sorting."""
    return (path1 > path2) - (path1 < path2)


def list_files(directory):
    """List files in a given directory."""
    try:
        return sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    except OSError:
        return []


def is_test_file(filename):
    """Determine if a file is a test file (not -ref or support file)."""
    # Reference files
    if '-ref.' in filename or '-notref.' in filename:
        return False
    # Common support file patterns
    if filename.startswith('support-') or '/support/' in filename:
        return False
    # Test file extensions
    return filename.endswith(('.html', '.htm', '.xht', '.xhtml', '.svg', '.xml'))


def main():
    feature_name = sys.argv[1] if len(sys.argv) > 1 else 'unknown'

    # Read file paths from stdin
    file_paths = []
    for line in sys.stdin:
        filepath = grep_match_line_to_filename(line)
        if filepath:
            file_paths.append(filepath)

    if not file_paths:
        print("No file paths provided", file=sys.stderr)
        return 1

    # Group files by directory
    dirs_to_files = defaultdict(list)
    for filepath in file_paths:
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        dirs_to_files[directory].append(filename)

    # Generate WEB_FEATURES.yml for each directory
    generated_files = []
    updated_files = []

    for directory in sorted(dirs_to_files.keys()):
        yaml_path = os.path.join(directory, 'WEB_FEATURES.yml')

        # Get only the classified test files
        classified_files = sorted([f for f in dirs_to_files[directory] if is_test_file(f)])

        # Load existing YAML file if it exists
        existing_data = {'features': []}
        file_exists = os.path.exists(yaml_path)

        if file_exists:
            try:
                with open(yaml_path, 'r') as f:
                    existing_data = yaml.safe_load(f) or {'features': []}
                    if 'features' not in existing_data:
                        existing_data = {'features': []}
            except Exception as e:
                print(f"Warning: Could not read {yaml_path}: {e}", file=sys.stderr)
                existing_data = {'features': []}

        # Find if this feature already exists
        feature_found = False
        for feature in existing_data['features']:
            if feature.get('name') == feature_name:
                # Update existing feature
                feature['files'] = classified_files
                feature_found = True
                break

        # Add new feature if it doesn't exist
        if not feature_found:
            existing_data['features'].append({
                'name': feature_name,
                'files': classified_files
            })

        # Write YAML file
        os.makedirs(directory, exist_ok=True)
        with open(yaml_path, 'w') as f:
            yaml.dump(existing_data, f, default_flow_style=False, sort_keys=False)

        if file_exists:
            updated_files.append(yaml_path)
            print(f"Updated: {yaml_path}")
        else:
            generated_files.append(yaml_path)
            print(f"Generated: {yaml_path}")

    # Summary
    test_count = sum(1 for f in file_paths if is_test_file(f))
    print(f"\nSummary:")
    print(f"  Total files: {len(file_paths)}")
    print(f"  Test files: {test_count}")
    print(f"  Directories: {len(dirs_to_files)}")
    print(f"  YAML files generated: {len(generated_files)}")
    print(f"  YAML files updated: {len(updated_files)}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
