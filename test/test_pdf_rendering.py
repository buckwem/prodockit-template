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
whatever renderer this environment happens to have. These two tests are
narrower and complementary: given this project's own real zensical.toml,
do the renderers the config implies actually resolve - failing fast and
naming the cause (which command to run) rather than only surfacing as an
assertion about leaked text several layers downstream."""

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
