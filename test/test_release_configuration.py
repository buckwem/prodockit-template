"""Release-floor, website-style and upstream-domain configuration checks."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_required_tool_version_floors_are_consistent() -> None:
    declarations = "\n".join(
        _text(path)
        for path in (
            "requirements.txt",
            ".github/workflows/docs.yml",
            ".gitlab-ci.yml",
        )
    )

    assert "prodockit==" not in declarations
    assert "prodockit>=0.48.0" in _text("requirements.txt")
    assert "prodockit>=0.48.0" in _text(".github/workflows/docs.yml")
    assert _text(".gitlab-ci.yml").count("prodockit>=0.48.0") == 1
    assert "prodockit[testing]>=0.48.0" in _text("testrequirements.txt")
    assert "zensical>=0.0.57" in _text("requirements.txt")
    assert '"zensical==0.0.57"' in _text(".github/workflows/docs.yml")
    assert _text(".gitlab-ci.yml").count('"zensical==0.0.57"') == 1


def test_python_artifact_builds_use_the_version_file() -> None:
    version = _text(".python-version").strip()
    github = _text(".github/workflows/docs.yml")
    gitlab = _text(".gitlab-ci.yml")

    assert version == "3.14"
    assert "python-version-file: .python-version" in github
    assert f"image: python:{version}" in gitlab


def test_shared_file_manifest_is_delivered_by_template_sync() -> None:
    manifest = _text(".prodockit-shared-files.toml")
    template = _text(".prodockit-template.toml")

    assert 'source = "pdk.css"' in manifest
    assert 'target = "docs/stylesheets/pdk.css"' in manifest
    assert 'source = "pdk-pdf.css"' in manifest
    assert 'target = "docs/stylesheets/pdk-pdf.css"' in manifest
    assert '".prodockit-shared-files.toml"' in template
    assert '"docs/stylesheets/pdk.css"' in template
    assert '"docs/stylesheets/pdk-pdf.css"' in template
    assert '"docs/stylesheets/extra.css"' in template
    assert '"docs/stylesheets/print.css"' in template
    assert '"docs/stylesheets/**"' not in template


def test_dependency_drift_automation_is_not_shipped() -> None:
    assert not (ROOT / ".github" / "workflows" / "drift.yml").exists()
    assert "\ndrift:" not in _text(".gitlab-ci.yml")
    assert "DRIFT_TOKEN" not in _text(".gitlab-ci.yml")


def test_website_table_styles_support_grid_and_cell_shading() -> None:
    css = _text("docs/stylesheets/pdk.css")
    example = _text("docs/section4.md")

    assert "border-collapse: collapse" in css
    assert "--prodockit-table-shade-rgb" in css
    assert "background-color: rgba(var(--prodockit-table-shade-rgb), 0.05)" in css
    assert "table th.prodockit-table-cell-shaded" in css
    assert "table td.prodockit-table-cell-unshaded" in css
    assert ".md-typeset th.prodockit-rotate" in css
    assert ".md-typeset span.prodockit-rotate" in css
    assert 'Cell shading {: shade="8%" }' in example


def test_pdf_code_is_one_point_smaller_than_body_text() -> None:
    print_css = _text("docs/stylesheets/print.css")

    assert "html body {" in print_css
    assert "html body pre, html body code {" in print_css
    assert "font-size: 11pt !important; /* Base text size layout */" in print_css
    assert "line-height: 1.4;" in print_css
    assert "font-size: 10pt !important;" in print_css


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


def test_all_capability_examples_are_in_section_five() -> None:
    section_five = _text("docs/section4.md")
    earlier_sections = "\n".join(
        _text(path) for path in ("docs/section1.md", "docs/section2.md", "docs/section3.md")
    )
    example_ids = (
        "bibliography-example",
        "acronyms-example",
        "glossary-example",
        "cross-reference-example",
        "figure-caption-example",
        "table-caption-example",
        "diagrams-example",
        "maths-example",
        "tree-example",
        "steps-example",
        "code-example",
    )

    for example_id in example_ids:
        marker = f"{{: #{example_id} }}"
        assert marker not in earlier_sections
        assert marker in section_five


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
