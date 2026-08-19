# Changelog

What has changed in this template. A clone does not pull, so this is
what someone who cloned earlier has not got.

At the repository root rather than under `docs/`, because `docs/` is the
report here - anything put there is published into every document built
from the template (issue #184).

Newest first.

## Unreleased

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

## Unreleased

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
