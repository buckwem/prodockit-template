# Changelog

What has changed in this template. A clone does not pull, so this is
what someone who cloned earlier has not got.

At the repository root rather than under `docs/`, because `docs/` is the
report here - anything put there is published into every document built
from the template (issue #184).

Newest first.

## Unreleased

- Cached the pinned Pandoc package and Python downloads used by CI, and allowed
  GitLab runners to reuse their locally held pinned Python image. Routine builds
  no longer depend on fresh Docker Hub, PyPI and Pandoc CDN responses
  ([#174](https://github.com/buckwem/prodockit-template/issues/174)).
- Documented creation, activation and recovery of the Python 3.14 `.venv`, so
  local builds use the same `.python-version` baseline as CI and a Homebrew
  interpreter upgrade has an explicit recovery path
  ([#193](https://github.com/buckwem/prodockit-template/issues/193)).
- Refreshed the committed Mermaid tool scaffold from ProDockit 0.54.0. The
  resolved Mermaid 11.17.2 and DOMPurify 3.4.14 dependency graph passes
  `npm audit`, so local setup, CI and template-synced projects no longer
  install the vulnerable lockfile reported in
  [#242](https://github.com/buckwem/prodockit-template/issues/242).

## 0.0.43 (2026-09-01)

- Restored the automated cover-page word count on both the website and PDF by
  rendering the shared ProDockit `word_count` macro directly instead of hiding
  a PDF-only marker from the website.

## 0.0.42 (2026-09-01)

- Removed the template's pytest suite and testing-only dependencies. ProDockit
  now has a 0.54.0 floor, and project, environment, dependency, configuration,
  renderer and template integrity is checked before each build by the
  read-only, content-neutral `pdk diag` command. The managed website stylesheet
  is also aligned with 0.54.0's top, middle and bottom table-cell controls.
- Declared PyMdown Extensions 11.0.2 as an explicit build-input floor. The
  template configures its Markdown extensions directly, even though ProDockit
  also installs the package transitively
  ([#240](https://github.com/buckwem/prodockit-template/issues/240)).
- Reworked the starter document into a solution-architecture report structure,
  with dedicated executive-summary, requirements, solution-architecture,
  governance and operations sections, plus a separate collection of removable
  authoring examples ([#237](https://github.com/buckwem/prodockit-template/pull/237)).
- Simplified the consent dialog used only by the canonical GitHub website while
  keeping the reusable configuration, forks and GitLab output analytics-free
  ([#236](https://github.com/buckwem/prodockit-template/pull/236)).

## 0.0.35 (2026-08-24)

- Dependency-drift automation has been removed from both GitHub Actions and
  GitLab CI. Routine prodockit release checks now belong to
  `prodockit template-sync`; maintainers can still compare pinned and upgraded
  builds manually when considering a broader dependency update.

## 0.0.34 (2026-08-24)

- The template now uses the same complete website extension stylesheet as
  prodockit itself and the User Guide. Table, tree, numbered-step, heading,
  caption, screenshot and other shared presentation rules therefore stay in
  step when an existing project runs `prodockit template-sync`.
- Template-only cover text and header artwork now live in a separate
  stylesheet, preserving the template's presentation without allowing its
  project-specific rules to drift into the shared stylesheet.

## 0.0.33 (2026-08-23)

- The website's generated MathJax configuration and pinned browser bundle now
  carry explicit cache revisions. Existing readers receive the corrected
  maths renderer without having to clear all data for `template.prodockit.org`.

## 0.0.32 (2026-08-22)

- The reusable template PDF no longer displays the template repository's own
  release version on its cover. A regression test now requires the marker to
  remain absent even after a template release has been published.
- Release-triggered GitHub documentation redeploys and GitLab tag builds have
  been removed because they existed only to refresh that unwanted marker.

## 0.0.31 (2026-08-22)

- PDF subsection headings are left-aligned without an underline again. Table
  captions now attach to their table rather than absorbing the preceding
  heading into a centred figure.
- All capability demonstrations are consolidated in Section 5, including the
  `prodockit.tree` example in Section 5.4.
- PDF typography is aligned with prodockit 0.42.1 at 11pt body text and 10pt
  code, with the template's body line spacing reduced from 1.6 to 1.4.
- Website table styles include the current grid, theme-aware 5% header and
  per-cell shading, and rotated-header rules.
- The prodockit dependency remains a minimum rather than an exact pin and is
  raised to `prodockit>=0.42.1` throughout local and hosted builds.

## 0.0.30 (2026-08-22)

- prodockit raised to a **0.42.0 floor** (from 0.41.0) everywhere, including
  both publishing and drift workflows, bringing forward cross-page references
  and configurable table-cell shading without exact-pinning later fixes out.
- Website tables now use the same complete grid and subtle 5% header shading
  as the PDF. Individual cells can override the percentage or turn shading
  off, including across merged cells.
- The template's own published example uses
  **https://template.prodockit.org/**. The custom-domain configuration is
  applied only when this upstream repository builds, so projects created from
  the template continue to derive and publish to their own Pages URL.

## 0.0.29 (2026-08-20)

- prodockit raised to **0.41.0** (from 0.40.0).

## 0.0.28 (2026-08-19)

- `prodockit.tree` and `prodockit.steps` are enabled, and demonstrated in
  the starter document
  ([#204](https://github.com/buckwem/prodockit-template/issues/204)).

    Both were registered extensions this template had never turned on, so
    a directory listing had to be hand-drawn as box-drawing characters -
    which has to be redrawn whenever a name changes, and carries no
    structure into the PDF - and a sequence of instructions was an
    ordinary numbered list.

    They are in Section 4's capability table too. An extension nobody
    knows about is not much better than one that is switched off.

- `prodockit.citations` is deliberately still **not** enabled, and
  `zensical.toml` now says why.

    It and `prodockit.bibliography` cover the same job two ways, and this
    template has committed to the second: `references.bib` and a CSL style
    are configured, and the starter document cites with `\cite{}`
    throughout. Enabling both would offer two competing ways to cite in a
    document demonstrating one.

- prodockit is now a **floor** in CI, not an exact pin, and moves to
  **0.40.0**.

    A document generated from this template used to sit on whatever
    prodockit release the template happened to name on the day it was
    generated, until somebody updated the template and the project synced
    from it. Its CI now installs `prodockit>=0.40.0`, so a project picks
    up fixes as they are released.

    `zensical` and `weasyprint` stay pinned exactly. Those two decide
    *rendering* - a new weasyprint repaginates, and those page numbers are
    resolved into the table of contents and the index - and the site and
    PDF are artifacts that should change when somebody decides they
    should.

    The drift job keeps an exact prodockit pin on purpose: it compares a
    baseline build against one made with the newest of everything, and a
    floor on both sides would compare the newest with the newest and never
    report anything.

    0.40.0 is the floor because it is the release where `\ref{}` resolves
    figures and tables.

## 0.0.27 (2026-08-19)

- prodockit pinned to **0.39.0** (from 0.38.0), which brings
  `prodockit template-sync`
  ([#498](https://github.com/buckwem/prodockit-extensions/pull/498)).

    This is the release that lets a project generated from this template
    catch up with it afterwards. A clone does not pull, which is what this
    changelog exists to work around; from now on there is a command that
    does the pulling:

    ```bash
    prodockit template-sync          # report; writes no project file
    prodockit template-sync --apply  # branch, write, stage - the commit is yours
    ```

    What it will and will not write is decided by `.prodockit-template.toml`
    in this repository, so the answer travels with the template rather than
    with the tool. The report, its figures and its bibliography are never
    written and never even read.

    Nothing needs to be installed for it: the template is fetched into a
    per-user cache. A project on Surrey's GitLab tracks the Surrey mirror
    and everything else this GitHub copy.

- The editor's own settings are no longer shipped ([#195](https://github.com/buckwem/prodockit-template/pull/195)).

    `.vscode/settings.json` and `.vscode/ltex.dictionary.en-US.txt` came
    from the template, and then fought whatever the extensions and
    Zensical Studio wrote there. They are `.gitignore`d now and set up on
    the machine instead. If you have them committed, they are yours to
    keep - nothing removes them.

- `LICENSE` is now `LICENSE.md`, and the template carries a manifest
  ([#197](https://github.com/buckwem/prodockit-template/pull/197), [#198](https://github.com/buckwem/prodockit-template/pull/198), [#199](https://github.com/buckwem/prodockit-template/pull/199), [#200](https://github.com/buckwem/prodockit-template/pull/200)).

    The rename follows Zensical, which declares `License-File: LICENSE.md`.

    `.prodockit-template.toml` is new, and is what `prodockit
    template-sync` reads to decide which files belong to the template and
    which are yours. Every file the template ships is classified in it, so
    nothing is guessed at. Your `zensical.toml` `pdf_copyright` and your
    `.vale.ini` are explicitly yours: a sync will not put this template's
    author on your report, nor replace your prose rules.

- Sized tables look like ordinary ones again, and dense tables have
  `{: .compact }` ([#186](https://github.com/buckwem/prodockit-template/pull/186), [#187](https://github.com/buckwem/prodockit-template/pull/187), [#191](https://github.com/buckwem/prodockit-template/pull/191)).

    Giving a table a column width used to restyle it - the theme scopes
    its own table rules to `table:not([class])`, and a width attribute put
    a class on it. Sized tables lost their row rules with it. Both are
    restored, and a table of many short columns can now ask for tighter
    padding rather than being left with the default.

- CI fails a hung job in minutes rather than hours, and the built-output
  checks report instead of gating ([#190](https://github.com/buckwem/prodockit-template/pull/190), [#196](https://github.com/buckwem/prodockit-template/pull/196)).

    A job that hung used to run until the platform's own six-hour limit.
    The checks on the built site and PDF now tell you what they found
    without failing the run: they are advice about a document, and a
    document that is merely unusual should still publish.

- Zensical pinned to **0.0.55** (from 0.0.53) and prodockit to
  **0.36.1** (from 0.35.0) ([#183](https://github.com/buckwem/prodockit-template/pull/183)).

    Zensical was compared before moving, not just bumped: this template's
    own site and PDF built under both versions and diffed byte for byte.
    The PDF is **identical**. Thirteen site files differ, each by exactly
    two lines - the `generator` meta tag and the JavaScript bundle's
    hashed filename - and the stylesheets, workers and licences are
    byte-identical, so nothing rendered changes.

    prodockit moves two releases. What matters for anyone building from
    this template: the first push no longer forces over a README the host
    created, which GitLab refuses on a protected branch - that is every
    assessed repository, so students were hitting a rejected push after a
    successful build and commit. The site probe also works on Windows
    now; it had reported "could not check" about a site that was serving.

    `prodockit` had to be named explicitly when moving the pin, because
    it is still absent from the default managed package list
    ([#173](https://github.com/buckwem/prodockit-template/issues/173)).

- Drift analysis runs at all, for the first time
  ([#181](https://github.com/buckwem/prodockit-template/pull/181)).

    The job builds the docs twice and diffs them, but never fetched the
    citation style, so *both* builds died before anything was compared
    and it only ever reported its own missing file
    ([#180](https://github.com/buckwem/prodockit-template/issues/180)).
    Its first real result is
    [#182](https://github.com/buckwem/prodockit-template/issues/182).

## Earlier

Before this file existed, the history is in `git log`. The changes a
holder of an older clone would most want to know about:

- **2026-08-13** - Python pinned to 3.13 from `.python-version`, so CI,
  `pyenv` and `uv` all read one source (#175).
- **2026-08-11** - MathJax is installed by CI the same way `prodockit
  bootstrap` installs it locally, replacing a duplicated heredoc whose
  whole failure mode was being subtly wrong (#166, #167, #168). Sites
  built before this showed raw TeX where an equation should be.
- **2026-08-10** - third-party assets are no longer vendored; they are
  fetched at build time (#97, #162).
- **2026-08-02** - docs are no longer deployed from the release event
  (#144). Deploying from a tag ref reported `success` and went on
  serving the previous build - silently, which is why it took so long to
  find.
- **2026-08-02** - a delivery-verify job fails the run when the live site
  is not serving the build just uploaded (#145, #147). A successful
  deploy is not proof of delivery.
- **2026-07-31** - build inputs pinned exactly and managed with
  `prodockit pins`, with on-demand drift detection (#141, #142).
