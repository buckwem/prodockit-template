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
4. Fetch the citation style `prodockit.bibliography` formats references with - not vendored in the repo, so every build (including `zensical serve`) needs it present locally:

   ```bash
   curl -fsSL -o harvard-cite-them-right.csl "https://www.zotero.org/styles/harvard-cite-them-right"
   ```
5. Preview the site locally: `zensical serve`.
6. Make a clean website build with `zensical build --clean`. If your change touches PDF generation, Mermaid diagrams, or MathJax equations, also install the Node tooling (`npm ci` in `tools/mermaid/` and `tools/mathjax/`) and run `prodockit pdf` afterwards. The PDF command reads the completed site rather than building it itself. See [Install tooling](https://buckwem.github.io/prodockit-userguide/installtooling/) in the User Guide for the full setup.

## Making a change

1. Create a branch off `main` for your change.
2. Make your change and verify it locally:
   - Website changes: `zensical serve` and check the page in a browser.
   - PDF-affecting changes (`zensical.toml`, `macros.py`, `docs/stylesheets/print.css`): run `zensical build --clean`, then `prodockit pdf`, and check `docs/site_documentation.pdf`.
   - Prose changes: optionally run `vale docs/` if you have [Vale](https://vale.sh/) installed (see [Additional tooling](https://buckwem.github.io/prodockit-userguide/additionaltooling/#install-vale-to-check-for-grammar-spelling-and-style-issues) in the User Guide); it's not enforced in CI.
   - Run the project diagnostics (see below). They validate the active environment, dependencies, configuration, source inputs and rendering tools without depending on the report's wording or examples.
3. Open a pull request against `main`. `main` is protected, so all changes - including from maintainers - go through a PR.
4. Reference the issue your PR addresses (e.g. `Fixes #123`) where applicable.

## Running the project diagnostics

Run the read-only, offline diagnostic before building. Its checks remain valid as authors replace the template's sample content with their own report.

```bash
pip install -r requirements.txt
pdk diag
zensical build --clean --strict
prodockit pdf
```

`pdk diag` checks the running Python and selected commands, package metadata and dependency conflicts, resolved project configuration and source inputs, version pins and shared files, configured renderers, Git and template metadata. It changes nothing and exits non-zero only for an actionable failure. Use `pdk diag --verbose` for evidence behind passing checks, `pdk diag --online` to include package and template updates, or `pdk diag --json` when attaching a report to a support issue. See [Diagnose an environment and project](https://prodockit.org/command-line/#diagnose-an-environment-and-project) for the command guide.

Run `prodockit template-sync` when the online diagnostic reports that the upstream template has changed and you want to preview the actual file updates.

## Version pinning

`.github/workflows/docs.yml` and `.gitlab-ci.yml` pin `zensical` and `weasyprint` exactly, on top of their floors in `requirements.txt`. Those renderers decide the published appearance and pagination, so they move only after review. `prodockit` is a floor (`prodockit>=...`) everywhere: a project receives compatible fixes without waiting for a template update and sync.

The same version ends up written in several places at once, so move them together rather than by hand:

```bash
prodockit pins
```

Prodockit is managed by default alongside Zensical, WeasyPrint and the other build inputs.

Press ++enter++ at each prompt to take the newest release, or type a version - each file keeps its own form (a floor stays a floor, an exact pin stays exact). Add `--check` to compare the declared versions with current releases without writing anything; see `prodockit pins --help` for the rest of the options.

The template also declares files supplied by the installed release in `.prodockit-shared-files.toml`. Check versions and those files together without contacting package indexes:

```bash
pdk diag
```

The diagnostic includes offline version and shared-file consistency, resolved
configuration, missing navigation pages, images, citation styles, optional
renderers and disabled extensions before a build.

If the shared stylesheets differ, restore the installed release's copies and review them before committing:

```bash
prodockit shared-files --apply
git diff -- docs/stylesheets/pdk.css docs/stylesheets/pdk-pdf.css
```

Before accepting an upgrade, build the website and PDF, take the upgrade with `prodockit pins`, build both outputs again, and review the differences before committing. This manual comparison is available when needed; routine Prodockit release checks are handled by `prodockit template-sync`.

## Reporting bugs and requesting features

Please use the issue templates when opening an issue - they help make sure we get the information needed to act on it.

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE.md).
