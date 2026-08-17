# Changelog

What has changed in this template, for whoever maintains it.

Deliberately at the repository root rather than under `docs/`. In this
repository `docs/` *is* the report - `section1.md`, `originality.md`,
`references.md` - so anything put there is published into every document
built from the template, and would land inside a student's assessed
submission (issue #184).

A student clones this once, at the start of a module, and never pulls
again. So this is not a curiosity: it is the record of how two cohorts'
copies came to differ, and what someone who cloned early would have to
redo by hand.

Newest first.

## Unreleased

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
