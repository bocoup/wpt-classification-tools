---
name: wpt-classify
description: Classify web features in the WPT repository by creating WEB_FEATURES.yml files
---

You are helping classify web platform tests (WPT) to map them to web-platform-dx/web-features.

# Workflow

Follow these 5 steps for each feature classification:

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
3. **🛑 STOP HERE - DO NOT PROCEED TO STEP 3 🛑**
   - Output: "Step 2 complete. Ready to proceed to Step 3 (Analysis & Filtering). Please enable deep thinking mode if desired."
   - **WAIT for user confirmation before continuing to Step 3**

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
3. Create excluded list containing ALL files from search results that were NOT mapped
   - Save as `wpt-classification-tools/search-results/{feature-name}/{feature-name}-excluded.txt`
   - Format: one filepath per line (same as mapped list)
   - IMPORTANT: The excluded list should contain every unique file from the search results that didn't make it into the mapped list
   - This ensures complete accounting of all search results
4. If there are no mapped files, notify the user and **🛑 STOP HERE - DO NOT PROCEED TO STEP 4 🛑**

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

**Handling Overlapping Features with Exclusion Patterns**

When a directory contains tests for multiple related features (e.g., a base feature and a more specific sub-feature):

1. Map the more specific feature first with its specific pattern
2. Map the base feature with `*` and use exclusion patterns to avoid double-mapping
3. Example structure:

   ```yaml
   features:
     - name: base-feature
       files:
         - "*"
         - "!specific-feature-*" # Exclude tests for specific sub-feature
     - name: specific-feature
       files:
         - specific-feature-* # Map the specific tests
   ```

4. Real example from webrtc:
   ```yaml
   features:
     - name: webrtc
       files:
         - "*"
         - "!RTCSctpTransport-*" # Exclude SCTP tests
     - name: webrtc-sctp
       files:
         - RTCSctpTransport-* # SCTP-specific tests
   ```

YAML format rules:

- Single-line list entries: `- 'pattern'` (NOT `files: 'pattern'`) except for the recursive wildcard pattern (`files: '**'`)
- Each pattern on its own line with `- ` prefix (EXCEPT `**`)
- Patterns in single quotes
- Exclusion patterns (`- '!pattern'`) work with `*` wildcards but will not work against a recursive wildcard pattern `**`
- Exclusion patterns can include wildcards (e.g., `'!specific-*'`, `'!*-excluded.html'`)


# Important Rules

1. **NEVER delete existing WEB_FEATURES.yml files** - only create new ones or update with new features
2. Use wpt-search and wpt-filter scripts instead of manual commands
3. Search results format: `filepath:\t\tline_content` (tabs after colon)
4. **🛑 MANDATORY: STOP after Step 2 and WAIT for user confirmation before Step 3 🛑**
   - This allows the user to enable deep thinking mode for the analysis phase
   - DO NOT proceed to Step 3 without explicit user instruction
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
