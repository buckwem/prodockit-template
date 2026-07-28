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

The Mermaid and TeX detection itself now comes from `prodockit.testing`
rather than a copy kept here (issue #128). Two findings this project made
against its own build live upstream now, so every prodockit project gets
them:

- A keyword alone is not enough. Prose wrapping so an ordinary English word
  like "graph" begins a PDF line was read as an unrendered diagram - passing
  locally and failing in CI purely because different fonts wrapped the same
  sentence differently (prodockit-userguide#25).
- Nor are arrows alone. This project's PDF body font (JetBrains Mono, see
  zensical.toml's mono_font) has programming ligatures, so "-->" extracts
  back out of the PDF as "//>" - confirmed against the real built PDF, and
  confirmed the website's own HTML has the correct unmangled arrows, so it
  is an extraction artifact of the ligature glyph rather than a difference
  in what was written. Node-definition brackets survive intact and are
  checked as an equally valid signal (prodockit-extensions#135, released in
  0.15.2).

Accepting bracket syntax needed the keywords tightened upstream too, or it
would have fired on ordinary technical prose - "graph"/"flowchart" now
require their direction token, and the diagram types that are also plain
English words accept only arrow or entity-relationship evidence."""

import pytest
from prodockit.pdf.config import _find_mmdc_bin, _find_tex2svg_script
from prodockit.testing import (
    assert_no_unrendered_mermaid,
    assert_no_unrendered_tex,
    contains_unrendered_mermaid,
)


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


def test_no_page_contains_literal_mermaid_source(pdf_full_text):
    assert_no_unrendered_mermaid(pdf_full_text)


def test_no_page_contains_literal_tex_source(pdf_full_text):
    assert_no_unrendered_tex(pdf_full_text)


# Mermaid's default node fill (#ECECFF). Every node shape in a rendered
# diagram is painted with it, and nothing else in this document uses it -
# confirmed by scanning every page of the real built PDF, where it appears
# on exactly one page, exactly four times, matching the diagram's four
# nodes. That makes it a signal that is actually specific to the diagram.
_MERMAID_NODE_FILL = (0.925, 0.925, 1.0)
_FILL_TOLERANCE = 0.02


def _mermaid_node_shapes(page):
    """Vector shapes on `page` painted with Mermaid's node fill."""
    shapes = []
    for drawing in page.get_drawings():
        fill = drawing.get("fill")
        if fill and all(
            abs(channel - expected) <= _FILL_TOLERANCE
            for channel, expected in zip(fill, _MERMAID_NODE_FILL)
        ):
            shapes.append(drawing)
    return shapes


def test_the_diagram_is_actually_rendered_into_the_pdf(pdf_doc):
    """Counterpart to the literal-source check above, which on its own would
    still pass if the diagram vanished from the PDF entirely instead of
    reaching it as text.

    Asserts on Mermaid's own node fill, because the obvious signals here all
    fail to discriminate:

    - Not the node label text. WeasyPrint converts Mermaid's plain-SVG
      `<text>` labels to vector path outlines in this pipeline, so
      `page.get_text()` finds nothing where the diagram is - confirmed
      against the real built PDF. (prodockit-userguide's pipeline keeps them
      as text, which is why its own equivalent test can search for them.)
    - Not `page.get_images()`. The single raster image in this PDF's shared
      resource pool is reported for *every* page, diagram or not.
    - Not `page.get_drawings()` being non-empty. Every page has vector
      content - headers, footers, table rules - so that passes anywhere. The
      previous version of this test asserted exactly that, and located the
      page by the caption prose below the diagram. Those turn out to be on
      *different pages*: the diagram ends page 9 and its caption opens page
      10, so the assertion ran against a page the diagram was never on. It
      could not have failed.
    """
    pages_with_nodes = {
        number: len(_mermaid_node_shapes(page))
        for number, page in enumerate(pdf_doc)
        if _mermaid_node_shapes(page)
    }
    assert pages_with_nodes, (
        "No page of the PDF contains a shape filled with Mermaid's node colour - "
        "docs/section4.md's diagram did not render, or was removed"
    )
    assert sum(pages_with_nodes.values()) >= 4, (
        f"Found only {sum(pages_with_nodes.values())} Mermaid node shape(s) "
        f"across {pages_with_nodes} - the diagram rendered only partially"
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
    assert not contains_unrendered_mermaid(wrapped_prose)


def test_a_genuinely_unrendered_block_is_still_flagged():
    """The other half of the pair above - narrowing the check must not have
    cost it the failure it exists to catch."""
    unrendered = (
        "the page:\n"
        "graph LR\n"
        "  A[Start] --> B{Error?};\n"
        "  B -->|Yes| C[Hmm...];\n"
    )
    assert contains_unrendered_mermaid(unrendered)
