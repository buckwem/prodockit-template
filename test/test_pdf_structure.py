# Copyright (c) 2025-2026 Mark Buckwell, Zensical and contributors
# SPDX-License-Identifier: MIT

"""pdf_structure batch: checks the PDF-only scaffolding around the actual
content - the cover page's computed fields, and the auto-generated Table of
Contents - is present and looks like real data, not a placeholder or an
empty result."""

import re


def test_cover_page_has_a_real_word_count(pdf_full_text):
    match = re.search(r"Word count:\s*([\d,]+)", pdf_full_text[0])
    assert match, "No 'Word count: N' line on the cover page"
    assert int(match.group(1).replace(",", "")) > 0


def test_cover_page_has_a_repo_url(pdf_full_text):
    match = re.search(r"Repo:\s*(\S+)", pdf_full_text[0])
    assert match, "No 'Repo: <url>' line on the cover page"
    assert match.group(1).startswith(("http://", "https://"))


def test_table_of_contents_exists(pdf_full_text):
    assert any("Table of Contents" in text for text in pdf_full_text)


def test_footer_clearance_survives_a_printers_unprintable_margin(pdf_doc):
    """Regression test (issue #151): the two-line footer (copyright +
    "Made with" credit) is top-aligned in pdf_margin_bottom and grows
    downward, so whatever the margin doesn't use is what's left before the
    paper edge. At the un-overridden 2cm default that left only 4.0mm -
    inside what most consumer/office printers physically cannot print
    (commonly 5-6.4mm) - so the second line would be clipped on an actual
    print even though the PDF itself renders correctly on screen. Checks a
    body page's lowest text block leaves at least 8mm, comfortably past
    that floor, rather than trusting zensical.toml's margin value in
    isolation - a change to the footer's font size or line count could
    erode the same clearance without touching the margin at all."""
    page = pdf_doc[min(5, len(pdf_doc) - 1)]
    lowest_y = max(block[3] for block in page.get_text("blocks"))
    clearance_mm = (page.rect.height - lowest_y) / 72 * 25.4
    assert clearance_mm >= 8.0, (
        f"Footer clearance is only {clearance_mm:.1f}mm - the second footer "
        "line risks being clipped on a physical print"
    )


_BOLD_FLAG = 1 << 4


def test_cover_page_title_is_bold_and_centered(pdf_doc, macros):
    """Regression test (prodockit-template#93): Pandoc's native Para AST node
    has no attribute field at all - a <p class="title-ctr-b4"> (the cover
    page's own title lines - see docs/index.md) came out the other end as
    a bare Para with the class silently dropped, losing both the bold
    weight and the centering pdk.css's .title-ctr-b4 rule provides.
    render_page_html() retags any classed/id'd <p> to a <div> (which
    Pandoc's reader does preserve attributes on) to fix this - checks the
    real cover page title line is both bold and horizontally centered.

    docs/index.md's cover page has two {% if is_surrey %} branches with
    different title text (see test_customisation.py's
    test_correct_branding_shown_for_this_repo, which checks the same split) -
    which one actually rendered depends on which remote *this* checkout is
    building against, so the search text has to follow macros._detect_is_surrey()
    rather than hardcoding the non-Surrey branch's text. That mismatch is
    exactly why this test failed on this project's own Surrey GitLab mirror
    pipeline while passing everywhere else (issue #139)."""
    title_text = (
        "Faculty of Engineering and Physical Sciences"
        if macros._detect_is_surrey()
        else "Crested Eagle Labs"
    )
    page = pdf_doc[0]
    page_center = page.rect.width / 2
    found = False
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line["spans"]:
                if title_text not in span["text"]:
                    continue
                found = True
                assert span["flags"] & _BOLD_FLAG, "Expected the cover page title to be bold"
                text_center = (span["bbox"][0] + span["bbox"][2]) / 2
                assert abs(text_center - page_center) < 5, (
                    f"Expected the cover page title centered on the page (page center "
                    f"{page_center}), found it centered at {text_center} instead"
                )
    assert found, f"Expected to find the cover page title {title_text!r} on the first PDF page"
