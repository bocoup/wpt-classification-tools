# WPT Classification: HTML Elements

## Directory Structure for HTML Element Tests

HTML element tests are spread across multiple directory trees. When classifying an element, search all of these locations:

| Directory Pattern | Content |
|-------------------|---------|
| `html/semantics/.../the-{element}-element/` | Primary element definition tests |
| `html/rendering/non-replaced-elements/{element}-0/` | Rendering tests for non-replaced elements |
| `html/rendering/replaced-elements/...` | Rendering tests for replaced elements (img, audio, video) |
| `html/rendering/widgets/` | Form control rendering tests |
| `html/dom/...` | DOM API tests |
| `html/webappapis/...` | Event handlers and scripting tests |

## Examples

### Simple Element (Single Directory)
Most elements like `br`, `div`, `p`, `time`, `wbr` have tests in one directory:
- `html/semantics/text-level-semantics/the-br-element/`

### Multi-Directory Elements

**`hr`** - 2 directories:
- `html/semantics/grouping-content/the-hr-element/`
- `html/rendering/non-replaced-elements/the-hr-element-0/`

**`audio`** - 4 directories:
- `html/semantics/embedded-content/the-audio-element/`
- `html/semantics/embedded-content/media-elements/` (shared with video)
- `html/rendering/replaced-elements/embedded-content-rendering-rules/`
- `html/rendering/replaced-elements/embedded-content/`

**`textarea`** - 3 directories:
- `html/semantics/forms/the-textarea-element/`
- `html/rendering/widgets/`
- `html/rendering/bindings/the-textarea-element-0/`

**`body`** - Tests in DOM and events directories:
- `html/dom/documents/dom-tree-accessors/` → `Document.body.html`
- `html/webappapis/scripting/events/` → `body-onload.html`, `event-handler-*`

## Shared Test Files (Dual Mapping)

When a test genuinely tests multiple elements, map it to both features:

```yaml
features:
- name: b
  files:
  - b-strong-styles.html
- name: strong
  files:
  - b-strong-styles.html
```

## Common Exclusions for Form Elements

Form elements often have tests that belong to `constraint-validation` rather than the element itself:

```yaml
features:
- name: textarea
  files:
  - "*"
  - "!textarea-setcustomvalidity.html"
  - "!textarea-validity-clone.html"
  - "!textarea-validity-valueMissing-inside-datalist.html"
- name: constraint-validation
  files:
  - textarea-setcustomvalidity.html
  - textarea-validity-clone.html
  - textarea-validity-valueMissing-inside-datalist.html
```

Look for these patterns to identify constraint-validation tests:
- `*-setcustomvalidity.html`
- `*-validity*.html`
- Tests referencing `ValidityState`, `checkValidity()`, `reportValidity()`

## Filename Prefix Patterns in Shared Directories

When multiple elements share a directory (like `media-elements/`), use prefix patterns:

```yaml
# In html/semantics/embedded-content/media-elements/
features:
- name: audio
  files:
  - audio_*
- name: video
  files:
  - video_*
```

```yaml
# In html/rendering/widgets/
features:
- name: textarea
  files:
  - textarea-*
- name: input
  files:
  - input-*
```

## Reference PRs

| PR | Feature(s) | Pattern Used | Notable |
|----|-----------|--------------|---------|
| #56728 | `br` | `files: "**"` | Simple, single directory |
| #56607 | `output`, `constraint-validation` | Exclusion patterns | Multi-feature directory |
| #56606 | `label` | `files: "*"` | Single level only |
| #56578 | `div`, `p`, `pre` | `files: "**"` | Batch of simple elements |
| #56577 | `hr` | `files: "**"` | Two directories |
| #56575 | `del`, `ins` | `files: "**"` | Two related elements |
| #55481 | `audio` | Mixed patterns | Four directories, prefix patterns |
| #56466 | `textarea` | Exclusions + prefixes | Complex, validation overlap |
| #56306 | `strong`, `b` | Dual mapping | Shared test file |
| #56460 | `time` | `files: "**"` | Simple |
| #56243 | `wbr` | `files: "**"` | Simple |
| 5f0dd61 | `body` | Specific files | Scattered across DOM/events |
