# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""Project integrity and built-output checks that remain valid as authors edit."""

from prodockit.testing import (
    assert_no_unrendered_mermaid,
    assert_no_unrendered_tex,
    assert_project_integrity,
)


def test_the_source_project_is_complete() -> None:
    assert_project_integrity()


def test_the_pdf_built(prodockit_pdf) -> None:
    assert prodockit_pdf.page_count > 0


def test_diagrams_and_maths_actually_rendered(prodockit_pdf_page_texts) -> None:
    assert_no_unrendered_mermaid(prodockit_pdf_page_texts)
    assert_no_unrendered_tex(prodockit_pdf_page_texts)
