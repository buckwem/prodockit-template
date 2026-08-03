<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

# Contributing

Thanks for your interest in improving prodockit-template. This guide covers contributing to the template itself - fixing bugs, adding features, or improving the documentation-as-code tooling. If you're a student using the template to write your own assignment, you don't need any of this: just fork the repo and follow the [prodockit User Guide](https://buckwem.github.io/prodockit-userguide/).

## Before you start

For anything beyond a small fix (typos, broken links), please open an issue first to discuss the change. This avoids duplicated effort and lets us agree on the approach before you spend time on an implementation.

## Getting set up

1. Fork the repository and clone your fork.
2. Install the Python prerequisites: `pip install -r requirements.txt`.
3. Install [Pandoc](https://pandoc.org/installing.html) (e.g. `brew install pandoc`) - required even to preview the site locally, not just to build the PDF: `prodockit.bibliography`'s citations/references (see `docs/references.md`) are formatted via `pandoc --citeproc` on every build.
4. Preview the site locally: `zensical serve`.
5. If your change touches PDF generation, Mermaid diagrams, or MathJax equations, also install the Node tooling (`npm ci` in `tools/mermaid/` and `tools/mathjax/`) and build the PDF with `prodockit pdf`. See [Install tooling](https://buckwem.github.io/prodockit-userguide/installtooling/) in the User Guide for the full setup.

## Making a change

1. Create a branch off `main` for your change.
2. Make your change and verify it locally:
   - Website changes: `zensical serve` and check the page in a browser.
   - PDF-affecting changes (`zensical.toml`, `macros.py`, `docs/stylesheets/print.css`): run `prodockit pdf` and check `docs/site_documentation.pdf`.
   - Prose changes: optionally run `vale docs/` if you have [Vale](https://vale.sh/) installed (see [Additional tooling](https://buckwem.github.io/prodockit-userguide/additionaltooling/#install-vale-to-check-for-grammar-spelling-and-style-issues) in the User Guide); it's not enforced in CI.
   - Run the test suite (see below) - it checks the built website and PDF for regressions in this template's own prodockit-specific features (numbering, word count, links, and so on), and runs in CI on every push.
3. Open a pull request against `main`. `main` is protected, so all changes - including from maintainers - go through a PR.
4. Reference the issue your PR addresses (e.g. `Fixes #123`) where applicable.

## Running the test suite

The test suite in `test/` checks the *built output*, not the build process itself - build the website and PDF first, then run the tests against them:

```bash
pip install -r requirements.txt -r testrequirements.txt
prodockit pdf
zensical build
cp source_bundle.pdf public/source_bundle.pdf
python test/run_tests.py
```

Tests are grouped into batches (`build`, `captions`, `content`, `fences`, `links`, `numbering`, `pdf_structure`, `word_count`), each reporting its own pass/fail. Run `python test/run_tests.py --list` to see them, and `python test/run_tests.py --batch <name>` to run just one - useful when you're actively working on a specific capability and don't want to wait on the rest of the suite. Extra arguments after the batch options are passed straight through to `pytest`. See [Testing](https://buckwem.github.io/prodockit-userguide/testing/) in the User Guide for the full guide.

## Version pinning

`.github/workflows/docs.yml` and `.gitlab-ci.yml` both pin `zensical`, `weasyprint` and `prodockit` to exact versions, on top of the floors (`zensical>=...`, `weasyprint>=...`, `prodockit>=...`) in `requirements.txt` - the published site and PDF are artifacts that should change when someone decides they should, not whenever any of the three next releases. `weasyprint` decides pagination, and those page numbers are resolved into the table of contents; `prodockit` renders this project's own PDF and generates its index (issue #149).

The same version ends up written in several places at once, so move them together rather than by hand:

```bash
prodockit pins -p zensical -p weasyprint -p prodockit
```

`-p` is needed for all three here: `prodockit pins`'s own default (`zensical` and `weasyprint`) predates this project pinning itself, so a bare `prodockit pins` or `prodockit pins --check` silently skips the `prodockit` pin.

Press ++enter++ at each prompt to take the newest release, or type a version - each file keeps its own form (a floor stays a floor, an exact pin stays exact). Add `--check` to report drift without writing anything (used by the workflow below); see `prodockit pins --help` for the rest of the options.

To check whether taking the newest release would actually change the published output, run the **Dependency drift** workflow: `.github/workflows/drift.yml` (Actions → Dependency drift → Run workflow) or the `drift` job in `.gitlab-ci.yml` (Run pipeline from the GitLab UI). Both build the docs twice - pinned versus newest - diff byte for byte, and open an issue saying what moved. Neither runs on a schedule; both are on-demand only.

## Reporting bugs and requesting features

Please use the issue templates when opening an issue - they help make sure we get the information needed to act on it.

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
