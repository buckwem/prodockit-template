# Copyright (c) 2025-2026 Mark Buckwell, Zensical and contributors
# SPDX-License-Identifier: MIT

"""Guards against Mermaid diagrams and TeX maths silently reaching the PDF
as raw source instead of rendered images (prodockit-userguide#23, brought
across here per issue #125).

WeasyPrint has no JS engine, so unlike the website - which renders both
client-side via Mermaid.js and MathJax - the PDF build shells out to
mermaid-cli and mathjax-full to pre-render them to static images.
prodockit.pdf deliberately leaves the content unrendered rather than
failing the build when those aren't found, which is the right default for
a project that uses neither, but means a project that *does* use them gets
a quietly broken PDF and no error - exactly what happened to
prodockit-userguide before it added these same two checks.

test_zensical_basics.py's own mermaid/math tests already assert against
*synthetic* content built via build_synthetic_pdf(), which always supplies
whatever renderer this environment happens to have. The two config-vs-
tooling tests below are narrower and complementary: given this project's
own real zensical.toml, do the renderers the config implies actually
resolve - failing fast and naming the cause (which command to run) rather
than only surfacing as an assertion about leaked text several layers
downstream.

The literal-source checks below them are the other half: this project's
own docs previously demonstrated neither capability at all (issue #125),
so nothing actually exercised the real `prodockit pdf` build end to end -
a config/tooling mismatch here would have gone unnoticed exactly the way
it did in prodockit-userguide. docs/section4.md now has one real Mermaid
diagram and one real TeX equation (see "Diagrams"/"Maths" in its own
capabilities table), and these tests check the actual built
docs/site_documentation.pdf for either one having reached it as raw
source instead of a rendered image.

The Mermaid detection regex is ported from prodockit-userguide#25, not
reinvented: a keyword-only check flagged ordinary prose ("a visual commit
graph and richer history browsing") that happened to wrap so a diagram
keyword began a PDF line - passing locally and failing in CI purely
because different fonts wrapped the same sentence differently. Requiring
Mermaid's own link syntax nearby as well fixes that without weakening the
check: an unrendered fence dumps the whole block, so the arrows are always
there, while prose that merely starts a line with "graph" has nothing
resembling them."""

import re

import pytest
from prodockit.pdf.config import _find_mmdc_bin, _find_tex2svg_script


def _fence_is_configured(zensical_config, fence_name):
    extensions = zensical_config.get("project", {}).get("markdown_extensions", {})
    fences = extensions.get("pymdownx", {}).get("superfences", {}).get("custom_fences", [])
    return any(fence.get("name") == fence_name for fence in fences)


def _arithmatex_is_configured(zensical_config):
    extensions = zensical_config.get("project", {}).get("markdown_extensions", {})
    return "arithmatex" in extensions.get("pymdownx", {})


def test_mermaid_renderer_is_available_when_the_mermaid_fence_is_configured(zensical_config):
    """Fails fast, and names the cause, when tools/mermaid isn't installed -
    rather than leaving it to be inferred from odd-looking PDF content."""
    assert _fence_is_configured(zensical_config, "mermaid"), (
        "zensical.toml no longer configures the mermaid fence - this test (and "
        "the guarantee behind issue #125) assumes it does"
    )
    assert _find_mmdc_bin(None) is not None, (
        "zensical.toml configures the mermaid fence, but no mmdc binary was found - "
        "run `npm ci --prefix tools/mermaid`, or Mermaid diagrams will silently "
        "render as raw source in the PDF"
    )


def test_maths_renderer_is_available_when_arithmatex_is_configured(zensical_config):
    assert _arithmatex_is_configured(zensical_config), (
        "zensical.toml no longer enables pymdownx.arithmatex - this test (and the "
        "guarantee behind issue #125) assumes it does"
    )
    assert _find_tex2svg_script(None) is not None, (
        "zensical.toml enables pymdownx.arithmatex, but no tex2svg script was found - "
        "run `npm ci --prefix tools/mathjax`, or maths will silently render as raw "
        "LaTeX in the PDF"
    )


# A rendered diagram contributes vector drawings, not text, so a Mermaid
# diagram-type keyword still present as text means the fenced ```mermaid
# block was passed through as a literal code block.
#
# The keyword alone is not enough to conclude that, though (prodockit-
# userguide#25): line breaks in a PDF fall wherever the text happens to
# wrap, and several of these words are ordinary English - a false positive
# there was "graph" starting a line inside an unrelated sentence. So
# require a diagram-type keyword *and* Mermaid's own syntax shortly after
# it: an unrendered fence dumps the whole block, so that syntax is always
# there, while prose that happens to start a line with "graph" has nothing
# resembling it.
#
# Confirmed directly against this project's own real built PDF (with the
# renderer genuinely absent) that its arrow syntax alone isn't a reliable
# signal here: this project's PDF body font (JetBrains Mono, see
# zensical.toml's mono_font) has programming ligatures, and "-->"/"-->|"
# extract back from the PDF as "//>"/"//>|" instead of literal text -
# confirmed the website's own HTML has the correct, unmangled "-->", so
# this is a PDF-text-extraction artifact of the ligature glyph, not a
# genuine difference in what was written. Node-definition bracket syntax
# (`id[Label]`/`id{Label}`) isn't part of any ligature substitution and
# survives extraction intact, so it's checked as an equally-valid signal
# alongside the arrow syntax rather than in place of it - either one, on
# its own, still requires the diagram keyword to have matched first.
_MERMAID_KEYWORD_RE = re.compile(
    r"^\s*(graph|flowchart|sequenceDiagram|stateDiagram(?:-v2)?|classDiagram|erDiagram|"
    r"gantt|journey|pie|gitGraph|mindmap|timeline)\b",
)
_MERMAID_LINK_RE = re.compile(
    r"--+>|--+\||-\.->|==+>|->>|--\s*$|\w+\[[^\]\n]+\]|\w+\{[^}\n]+\}"
)
# How far after the keyword line to look for that syntax - a diagram's first
# link is on the very next line in practice; a few lines of slack covers a
# declaration or comment in between.
_MERMAID_LOOKAHEAD_LINES = 6


def find_literal_mermaid_source(text):
    """Returns True if `text` (one PDF page) looks like it contains a
    Mermaid block that was never rendered."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not _MERMAID_KEYWORD_RE.match(line):
            continue
        window = lines[i : i + 1 + _MERMAID_LOOKAHEAD_LINES]
        if any(_MERMAID_LINK_RE.search(candidate) for candidate in window):
            return True
    return False


# Likewise for maths: rendered output is an image, so a surviving TeX
# delimiter or command means the formula was never pre-rendered.
_TEX_SOURCE_RE = re.compile(r"\\\[|\\\]|\\sum_|\\frac\{|\\infty|\\begin\{|\\cos ")


def test_no_page_contains_literal_mermaid_source(pdf_full_text):
    offenders = [i for i, text in enumerate(pdf_full_text) if find_literal_mermaid_source(text)]
    assert not offenders, (
        f"Literal Mermaid source found on PDF page(s) {offenders} - the diagram was "
        "passed through as a code block instead of being pre-rendered to an image"
    )


def test_no_page_contains_literal_tex_source(pdf_full_text):
    offenders = [i for i, text in enumerate(pdf_full_text) if _TEX_SOURCE_RE.search(text)]
    assert not offenders, (
        f"Literal TeX source found on PDF page(s) {offenders} - the formula was not "
        "pre-rendered to an image"
    )


# The paragraph immediately following docs/section4.md's own diagram -
# unique to that page, so it locates the diagram's page reliably regardless
# of where page breaks happen to fall.
_DIAGRAM_CAPTION_TEXT = "Above is an example of a Mermaid diagram"


def test_the_diagrams_section_diagram_is_actually_present(pdf_doc):
    """Counterpart to the literal-source check above, which on its own would
    still pass if the diagram vanished from the PDF entirely instead of
    rendering as text - confirms real vector content backs it up, the same
    signal test_zensical_basics.py's own synthetic mermaid test uses.

    Not the diagram's own node label text: confirmed directly against this
    project's real built PDF that WeasyPrint's SVG rendering here converts
    Mermaid's plain-SVG `<text>` labels to vector path outlines rather than
    extractable PDF text objects, so `page.get_text()` finds nothing where
    the diagram is - a different result from prodockit-userguide's own
    pipeline, not a discrepancy to paper over by asserting label text that
    doesn't actually appear here. Also deliberately not `page.get_images()`:
    the one raster image already on this page (this template's own cover/
    branding asset, not the diagram) would make that check pass even with
    the diagram missing."""
    for page in pdf_doc:
        if _DIAGRAM_CAPTION_TEXT in page.get_text():
            assert page.get_drawings(), (
                "The diagram's own caption text is present but the page has no vector "
                "drawings - its boxes and arrows did not render"
            )
            return
    pytest.fail(
        f"No PDF page contains {_DIAGRAM_CAPTION_TEXT!r} - docs/section4.md's Mermaid "
        "example appears to have been removed or moved"
    )


def test_prose_that_merely_starts_a_line_with_a_diagram_keyword_is_not_flagged():
    """Regression test (prodockit-userguide#25) for the false positive that
    a keyword-only check produced: prose wrapping so an ordinary English
    word like "graph" begins a PDF line must not be read as an unrendered
    diagram."""
    wrapped_prose = (
        "annotations - showing who last changed each line, and when -\n"
        "directly above your text, along with a visual commit\n"
        "graph and richer history browsing. It's especially useful once\n"
        "you're using the branches and issues workflow.\n"
    )
    assert not find_literal_mermaid_source(wrapped_prose)


def test_a_genuinely_unrendered_block_is_still_flagged():
    """The other half of the pair above - narrowing the check must not have
    cost it the failure it exists to catch."""
    unrendered = (
        "the page:\n"
        "graph LR\n"
        "  A[Start] --> B{Error?};\n"
        "  B -->|Yes| C[Hmm...];\n"
    )
    assert find_literal_mermaid_source(unrendered)
