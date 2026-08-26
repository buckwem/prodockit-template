"""The upstream website alone receives consent-gated analytics."""

import importlib.util
import tomllib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "canonical_site_config.py"


def _tool_module():
    spec = importlib.util.spec_from_file_location("canonical_site_config", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generated_config_adds_opt_in_analytics(tmp_path: Path) -> None:
    destination = tmp_path / "zensical.toml"
    _tool_module().write_config(
        ROOT / "zensical.toml",
        destination,
        "G-TEST123",
        "https://template.prodockit.org/",
    )

    generated = destination.read_text(encoding="utf-8")
    project = tomllib.loads(generated)["project"]
    extra = project["extra"]
    assert project["site_url"] == "https://template.prodockit.org/"
    assert extra["analytics"] == {"provider": "google", "property": "G-TEST123"}
    assert extra["consent"]["cookies"]["analytics"]["checked"] is False
    assert generated.count("G-TEST123") == 1


@pytest.mark.parametrize("measurement_id", ["", "1Y63EJRYX4", "G-invalid id"])
def test_invalid_measurement_id_is_rejected(measurement_id: str) -> None:
    with pytest.raises(ValueError, match="invalid Google Analytics measurement ID"):
        _tool_module().with_canonical_site(
            _text("zensical.toml"), measurement_id, "https://template.prodockit.org/"
        )


@pytest.mark.parametrize(
    "site_url",
    ["", "http://template.prodockit.org/", "https://user@example.com/", "not a URL"],
)
def test_invalid_canonical_site_url_is_rejected(site_url: str) -> None:
    with pytest.raises(ValueError, match="invalid canonical website URL"):
        _tool_module().with_canonical_site(_text("zensical.toml"), "G-TEST123", site_url)


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")
