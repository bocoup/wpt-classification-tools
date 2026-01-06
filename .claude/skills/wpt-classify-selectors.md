# WPT Classification: CSS Pseudo-Selectors

## CSS Pseudo-Selector PRs Status Report

### Summary Table

| Feature | Selector | PR | Status |
|---------|----------|-----|--------|
| backdrop | `::backdrop` | #55481 | **Merged** (Nov 12) |
| before-after | `::before`, `::after` | #55697 | **Merged** (Nov 21) |
| column-pseudo | `::column` | #56533 | Unknown |
| empty | `:empty` | #56412 | **Merged** (Dec 4) |
| focus-within | `:focus-within` | #56564 | **Open** |
| heading-selectors | `:heading` | #56730 | **Open** |
| link-selectors | `:link`, `:visited`, `:any-link` | #56504 | **Open** |
| placeholder | `::placeholder` | #56691 | **Open** |
| placeholder-shown | `:placeholder-shown` | #56691 | **Open** |
| scope-pseudo | `:scope` | #56311 | **Open** (1 approval) |
| scroll-buttons | `::scroll-button` | #56469 | **Merged** (Dec 4) |
| target | `:target` | #56400 | **Merged** (Dec 2) |
| time-relative-selectors | `:current`, `:past`, `:future` | #55150 | **Merged** (Oct 15) |
| user-action-pseudos | `:focus`, `:hover`, `:active` | #56443 | **Merged** (Dec 4) |

---

## Key Learnings

### 1. Exclude tests for "newer" features when mapping "older" features
From #55481 (backdrop): foolip noted that "features that came much later and use `::backdrop` are more akin to a new feature" — so popover tests were excluded from the backdrop mapping even though they use `::backdrop`.

### 2. Deliberately exclude tests that primarily test other selectors
- **#56412 (empty)**: Excluded `empty-pseudo-in-has.html` because "testing `:has()` is the priority here"
- **#56691 (placeholder)**: Excluded tests primarily testing `:has()` or `shadow-parts`
- **#56504 (link-selectors)**: Excluded tests involving `:has()` and `:not()` interactions

### 3. Remapping tests to more appropriate features is OK
From #56504 (link-selectors): `caret-color-visited-inheritance.html` was **remapped** from `caret-color` to `link-selectors` because it more directly tests `:visited` behavior.

### 4. Distinguish between at-rules and pseudo-classes
From #56311 (scope-pseudo): The contributor applied `scope-pseudo` specifically to "selector-based" tests, not to tests already classified under `scope` (the `@scope` at-rule feature).

### 5. Mixed tests may need exclusion
From #56443 (user-action-pseudos): Tests containing mixed `:focus`, `:focus-within`, and `:focus-visible` subtests were excluded to maintain "feature-specific clarity."

### 6. Exclude tests for related but separate features
From #56400 (target): Excluded tests for:
- `::target-text` pseudo-element (separate feature)
- `:target-current`, `:target-before`, `:target-after` (scroll marker pseudo-classes)

### 7. When uncertain about edge cases, lean toward exclusion
From #56691 (placeholder): Author noted uncertainty about tests for `line-height` and text alignment on placeholders, "ultimately deciding to exclude them to maintain feature focus."

---

## Patterns for Granular Exclusions
From #55150: When multiple features apply to the same tests, using `"**"` wildcards won't work — you need more granular patterns to enable specific exclusions.

---

## Directory Patterns for CSS Pseudo-Selector Tests

### Primary Directories

| Directory | Features Found There |
|-----------|---------------------|
| `css/selectors/` | empty, target, user-action-pseudos, heading-selectors |
| `css/selectors/parsing/` | heading-selectors |
| `css/selectors/old-tests/` | target |
| `css/CSS2/selectors/` | user-action-pseudos |
| `css/css-pseudo/` | backdrop |
| `css/css-animations/` | backdrop, empty |
| `css/css-overflow/` | scroll-buttons |
| `css/css-overflow/parsing/` | scroll-buttons |
| `css/css-position/` | backdrop |

### Secondary Directories (Feature-Specific)

| Directory | Features |
|-----------|----------|
| `html/semantics/interactive-elements/the-dialog-element/` | backdrop |
| `html/browsers/browsing-the-web/scroll-to-fragid/` | target |
| `fullscreen/rendering/` | backdrop |
| `fullscreen/crashtests/` | backdrop |
| `svg/struct/reftests/` | target |
| `webvtt/rendering/.../selectors/cue_function/` | time-relative-selectors |

### Key Takeaways

1. **`css/selectors/`** is the primary hub — most pseudo-selector features will have tests here
2. **`css/selectors/parsing/`** often has `parse-*.html` tests for selector syntax validation
3. **`css/CSS2/selectors/`** has older CSS2-era selector tests (like `:hover`, `:active`, `:focus`)
4. **`css/selectors/old-tests/`** contains legacy tests with `css3-modsel-*` naming
5. **Feature-specific CSS modules** (`css-overflow`, `css-pseudo`, `css-position`, `css-animations`) may contain tests when the selector is used in that context
6. **HTML/SVG/WebVTT directories** may have tests when the selector interacts with specific elements
