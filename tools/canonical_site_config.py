#!/usr/bin/env python3
"""Configure the canonical template website build.

The committed Zensical configuration is deliberately analytics-free because
it is copied into projects created from this template.  The upstream GitHub
Pages workflow writes a temporary configuration with its domain and analytics
enabled, and uses that file only for the canonical website build.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path
from urllib.parse import urlsplit


MEASUREMENT_ID = re.compile(r"G-[A-Z0-9]+")


def with_canonical_site(source: str, measurement_id: str, site_url: str) -> str:
    """Return *source* configured for the canonical website only."""

    if not MEASUREMENT_ID.fullmatch(measurement_id):
        raise ValueError(f"invalid Google Analytics measurement ID: {measurement_id!r}")

    parsed_url = urlsplit(site_url)
    if (
        parsed_url.scheme != "https"
        or not parsed_url.hostname
        or parsed_url.username
        or parsed_url.password
        or parsed_url.query
        or parsed_url.fragment
        or '"' in site_url
        or "\\" in site_url
    ):
        raise ValueError(f"invalid canonical website URL: {site_url!r}")

    project = tomllib.loads(source).get("project", {})
    extra = project.get("extra", {})
    if "analytics" in extra or "consent" in extra:
        raise ValueError("source configuration already defines analytics or consent")

    canonical_source, replacements = re.subn(
        r'(?m)^site_url\s*=\s*"[^"]*"\s*$',
        f'site_url = "{site_url}"',
        source,
        count=1,
    )
    if replacements != 1:
        raise ValueError("source configuration must define one quoted site_url")

    analytics = f'''\n\n# Added only by the canonical template website workflow.
[project.extra.analytics]
provider = "google"
property = "{measurement_id}"

[project.extra.consent]
title = "Cookie consent"
description = """
    We use optional analytics cookies to understand which parts of the
    template are useful and improve prodockit. Google Analytics remains
    disabled unless you choose to accept it.
"""
actions = ["accept", "reject", "manage"]

[project.extra.consent.cookies]
analytics.name = "Google Analytics"
analytics.checked = false
'''
    generated = canonical_source.rstrip() + analytics

    parsed_project = tomllib.loads(generated)["project"]
    parsed_extra = parsed_project["extra"]
    assert parsed_project["site_url"] == site_url
    assert parsed_extra["analytics"]["property"] == measurement_id
    assert parsed_extra["consent"]["cookies"]["analytics"]["checked"] is False
    return generated


def write_config(
    source_path: Path,
    destination_path: Path,
    measurement_id: str,
    site_url: str,
) -> None:
    """Write and validate the canonical website configuration."""

    destination_path.write_text(
        with_canonical_site(
            source_path.read_text(encoding="utf-8"), measurement_id, site_url
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("measurement_id")
    parser.add_argument("site_url")
    args = parser.parse_args()
    write_config(args.source, args.destination, args.measurement_id, args.site_url)


if __name__ == "__main__":
    main()
