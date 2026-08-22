"""Release-floor, website-style and upstream-domain configuration checks."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prodockit_042_floor_is_consistent() -> None:
    declarations = "\n".join(
        _text(path)
        for path in (
            "requirements.txt",
            ".github/workflows/docs.yml",
            ".github/workflows/drift.yml",
            ".gitlab-ci.yml",
        )
    )

    assert "prodockit==" not in declarations
    assert "prodockit>=0.42.0" in _text("requirements.txt")
    assert "prodockit>=0.42.0" in _text(".github/workflows/docs.yml")
    assert "prodockit>=0.42.0" in _text(".github/workflows/drift.yml")
    assert _text(".gitlab-ci.yml").count("prodockit>=0.42.0") == 2


def test_website_table_styles_support_grid_and_cell_shading() -> None:
    css = _text("docs/stylesheets/extra.css")
    example = _text("docs/section4.md")

    assert "border-collapse: collapse" in css
    assert "--prodockit-table-shade-rgb" in css
    assert "background-color: rgba(var(--prodockit-table-shade-rgb), 0.05)" in css
    assert "table th.prodockit-table-cell-shaded" in css
    assert "table td.prodockit-table-cell-unshaded" in css
    assert 'Cell shading {: shade="8%" }' in example


def test_pdf_subsection_heading_is_not_absorbed_by_the_table_caption() -> None:
    example = _text("docs/section4.md")
    print_css = _text("docs/stylesheets/print.css")

    table_end = "| Numbered steps | `/// steps` | this section |"
    assert f"{table_end}\n/// table-caption | <" in example
    assert example.index("## SubSection {: #table-caption-example }") < example.index(table_end)
    assert "h2 { font-size: 18pt; margin-top: 20pt; }" in print_css
    assert "h2 { font-size: 18pt; margin-top: 20pt; border-bottom:" not in print_css


def test_section_five_uses_the_prodockit_tree_extension() -> None:
    config = _text("zensical.toml")
    example = _text("docs/section4.md")

    assert '[project.markdown_extensions."prodockit.tree"]' in config
    assert "## SubSection {: #tree-example }\n\n/// tree\n" in example


def test_custom_domain_is_applied_only_to_the_upstream_build() -> None:
    config = _text("zensical.toml")
    workflow = _text(".github/workflows/docs.yml")
    readme = _text("README.md")

    # A generated project needs this replaceable Pages URL so sync-repo can
    # derive its own; the custom URL and CNAME exist only in the upstream job.
    assert 'site_url = "https://buckwem.github.io/prodockit-template/"' in config
    assert workflow.count("if: github.repository == 'buckwem/prodockit-template'") == 2
    assert 'site_url = "https://template.prodockit.org/"' in workflow
    assert "printf 'template.prodockit.org\\n' > public/CNAME" in workflow
    assert "https://template.prodockit.org/" in readme
    assert not (ROOT / "docs" / "CNAME").exists()
