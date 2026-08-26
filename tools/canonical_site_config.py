#!/usr/bin/env python3
"""Add consent-gated analytics to the canonical template website build.

The committed Zensical configuration is deliberately analytics-free because
it is copied into projects created from this template.  The upstream GitHub
Pages workflow writes a temporary configuration with analytics enabled and
uses that file only for the canonical website build.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path


MEASUREMENT_ID = re.compile(r"G-[A-Z0-9]+")


def with_analytics(source: str, measurement_id: str) -> str:
    """Return *source* with consent-gated Google Analytics configured."""

    if not MEASUREMENT_ID.fullmatch(measurement_id):
        raise ValueError(f"invalid Google Analytics measurement ID: {measurement_id!r}")

    project = tomllib.loads(source).get("project", {})
    extra = project.get("extra", {})
    if "analytics" in extra or "consent" in extra:
        raise ValueError("source configuration already defines analytics or consent")

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
    generated = source.rstrip() + analytics

    parsed_extra = tomllib.loads(generated)["project"]["extra"]
    assert parsed_extra["analytics"]["property"] == measurement_id
    assert parsed_extra["consent"]["cookies"]["analytics"]["checked"] is False
    return generated


def write_config(source_path: Path, destination_path: Path, measurement_id: str) -> None:
    """Write and validate the canonical website configuration."""

    destination_path.write_text(
        with_analytics(source_path.read_text(encoding="utf-8"), measurement_id),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("measurement_id")
    args = parser.parse_args()
    write_config(args.source, args.destination, args.measurement_id)


if __name__ == "__main__":
    main()
