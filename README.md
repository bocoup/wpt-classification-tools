# WPT Classification Tools

Tools to assist in the classification of test material in [the Web Platform
Tests project](https://web-platform-tests.org/) according to [the "web
features"](https://github.com/web-platform-dx/web-features)
published by [the WebDX Community Group](https://www.w3.org/community/webdx/).

## `progress.csv`

This file tracks the progress of this effort and includes three columns to
describe each web feature to be classified in WPT:

- `id` - the identifier of the feature as assigned by the web-features project
- `name` - the name of the feature as assigned by the web-features project
- `status` - the status of the feature in Bocoup's classification effort; the
  values in this column take one of four forms:
  - empty - the feature has not been reviewed
  - prefixed by `@` - the feature has been claimed by the owner of the
    GitHub handle which follows the `@` character; it is expected to be
    classified soon
  - prefixed with `#` - the feature has been classified and that classification
    submitted for review; the number following the `#` character is the
    identifier of the corresponding GitHub pull request filed against the WPT
    project
  - prefixed with `X` - the feature has been reviewed and judged unsuitable for
    classification; a short note about the judgement follows the `X` character

## License

Copyright (c) 2025 Bocoup
Licensed under the MIT license.
