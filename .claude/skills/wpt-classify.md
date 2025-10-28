---
name: wpt-classify
description: Classify web features in the WPT repository by creating WEB_FEATURES.yml files
---

You are helping classify web platform tests (WPT) to map them to web-platform-dx/web-features.

# Workflow

Follow these 7 steps for each feature classification:

## Step 1: Initial Setup

1. Fetch the feature definition from web-features repository:
   `https://raw.githubusercontent.com/web-platform-dx/web-features/main/features/{feature-name}.yml`
2. Read and understand the feature scope, compat_features, and any notes
3. Use TodoWrite to create todos for all 7 steps

## Step 2: Search & Discovery

1. Identify appropriate search terms based on feature definition:
   - Property definitions: `propdef-{property}`, `the-{property}-property`
   - Feature-specific spec anchors from the feature YAML
2. Use `./wpt-classification-tools/wpt-search {feature-name} {search-term}` for each search term
   - All results will be saved in `wpt-classification-tools/search-results/{feature-name}/` subdirectory
   - Keep individual search result files (no need to combine)
   - **IMPORTANT**: NEVER modify or strip content from the raw search result files from wpt-search
   - Raw search results have format: `filepath:\t\tline_content` and must remain intact
3. **PAUSE** and inform user you're ready for Step 3 deep thinking

## Step 3: Analysis & Filtering (Deep Thinking Mode)

Conservative filtering principles:

- Only map tests where the feature is the PRIMARY focus
- Exclude tests that use the feature incidentally to test something else
- Check test titles, assertions, and primary help links
- If a test is primarily about feature X but uses feature Y, it belongs to X

Common exclusions:

- Reference files (_-ref.html, _-ref.xht)
- Index/metadata files (e.g., section-index.xht)
- Tests already mapped to other features
- Tests primarily about other features (check existing WEB_FEATURES.yml files)

Examples of exclusion reasoning:

- Float tests in `floats-clear/`: Usually about float behavior, not the width/height properties used
- Tests in `css/css-{other-feature}/`: Check existing WEB_FEATURES.yml - likely already mapped
- Anonymous boxes tests: Primary focus is box generation, not the properties used
- Flexbox/Grid tests: Primary focus is layout algorithm, not individual properties

## Step 4: Create Mapped and Excluded Lists

1. Extract all unique file paths from all search results (just the filepath, not the line content)
2. Apply conservative filtering to create mapped files list
   - Save as `wpt-classification-tools/search-results/{feature-name}/{feature-name}-mapped.txt`
   - Format: one filepath per line (no tabs or line content - just paths)
3. Manually create excluded list by subtracting mapped files from all unique files
   - Format: one filepath per line (same as mapped list)

**Note**: The mapped and excluded lists contain ONLY file paths (derived from raw search results). The raw search result files from Step 2 remain unchanged with their full `filepath:\t\tline_content` format.

## Step 5: Create WEB_FEATURES.yml Files

For each directory with mapped tests:

1. Check if WEB_FEATURES.yml already exists - **NEVER delete existing files**
2. Group mapped files by directory
3. For each directory, create or update WEB_FEATURES.yml with format:
   ```yaml
   features:
     - name: { feature-name }
       files:
         - "pattern-*"
         - "specific-file.html"
   ```

**IMPORTANT: Subdirectory Pattern Rules**

- **DO NOT use subdirectory paths in patterns** like `subdirectory/file-*` or `subdirectory/file.html`
- **INSTEAD: Create separate WEB_FEATURES.yml files in each subdirectory**
- Example:
  - ❌ WRONG: In `css/selectors/WEB_FEATURES.yml` add `- invalidation/where.html`
  - ✅ CORRECT: Create/update `css/selectors/invalidation/WEB_FEATURES.yml` with `- where.html`

**Pattern Guidelines**

- Use `*` wildcard for files in the CURRENT directory only (e.g., `file-*`, `*-test.html`)
- When mapping all root-level files in a directory, just use `*` instead of listing out many specific patterns!
- Use `**` recursive wildcard only for mapping ALL files in current + subdirectories
- Use specific filenames for individual files (e.g., `specific-test.html`)
- Don't create WEB_FEATURES.yml in directories you want to exclude

YAML format rules:

- Single-line list entries: `- 'pattern'` (NOT `files: 'pattern'`) except for the recursive wildcard pattern (`files: '**'`)
- Each pattern on its own line with `- ` prefix (EXCEPT `**`)
- Patterns in single quotes
- Exclusion patterns (`- '!pattern'`) will not work against a recursive wildcard pattern `**`. Check with user if you think you need to use an exclusion pattern.

## Step 6: Run Linter

1. Run `./wpt lint` from the repository root
2. Check for any errors related to WEB_FEATURES.yml files
3. Fix any formatting issues found
4. Ask user for help if encountering unfamiliar lint errors
5. Re-run linter until clean

## Step 7: Generate Commit Message

Format (match the style of recent commits):

```
maps {feature-name}

Feature: {feature-name}
Reference: https://github.com/web-platform-dx/web-features/blob/main/features/{feature-name}.yml

Note: {brief description of what the feature does}

Search strategy: {describe search terms and approach}

Results:
- Total matches found: {number}
- Filtered: {number} files

WEB_FEATURES.yml files created:
✅ path/to/dir/WEB_FEATURES.yml - Description ({count} files)
[... for each directory ...]

Excluded ({count} files):
- Category (X files): Reason for exclusion
[... for each exclusion category ...]
```

# Important Rules

1. **NEVER delete existing WEB_FEATURES.yml files** - only create new ones or update with new features
2. Use wpt-search and wpt-filter scripts instead of manual commands
3. Search results format: `filepath:\t\tline_content` (tabs after colon)
4. Always pause after Step 2 for user to enable deep thinking
5. Be conservative: when in doubt, exclude rather than include
6. Mark todos as completed immediately after finishing each step (don't batch)
7. Store all search results in `wpt-classification-tools/search-results/{feature-name}/` subdirectories
8. Run linter before generating commit message
9. All files for a feature (searches, mapped list, filtered, excluded) go in the same subdirectory

# Scripts Available

- `./wpt-classification-tools/wpt-search <feature-name> <search-term>` - Search with auto-exclusions
  - Results saved to `wpt-classification-tools/search-results/{feature-name}/{timestamp}-{search-term}.txt`
- `./wpt-classification-tools/wpt-filter <search-file> <mapped-file>` - Generate filtered/excluded lists
  - Outputs saved to same directory as search file
- `./wpt lint` - Run WPT linter to validate WEB_FEATURES.yml files

# User Interaction

- Ask clarifying questions about ambiguous cases
- Show your reasoning for exclusion decisions
- Let user review before creating WEB_FEATURES.yml files for questionable directories
- Ask for help with unfamiliar lint errors
- Pause after Step 2 for deep thinking mode as requested

# Directory Structure Patterns

- `css/css-{feature}/` - Check if already has WEB_FEATURES.yml for another feature
- Subdirectories - Use `**` pattern or specific filenames
- Root directories - Use `*` pattern
