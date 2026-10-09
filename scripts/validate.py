#!/usr/bin/env python3

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def repository_file(reference: str, owner: Path) -> Path:
    path = (ROOT / reference).resolve()
    if path != ROOT and ROOT not in path.parents:
        raise ValueError(f"{owner.relative_to(ROOT)}: path escapes repository: {reference}")
    if not path.is_file():
        raise ValueError(f"{owner.relative_to(ROOT)}: missing file: {reference}")
    return path


pending = sorted(ROOT.glob("*.json"))
visited = set()
while pending:
    manifest = pending.pop(0)
    if manifest in visited:
        continue
    visited.add(manifest)
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{manifest.relative_to(ROOT)}: root must be an object")

    for reference in data.get("imports", []):
        if not isinstance(reference, str):
            raise ValueError(f"{manifest.relative_to(ROOT)}: imports must contain strings")
        pending.append(repository_file(reference, manifest))

    for mapping in data.get("files", []):
        if not isinstance(mapping, dict) or not isinstance(mapping.get("from"), str) or not isinstance(mapping.get("to"), str):
            raise ValueError(f"{manifest.relative_to(ROOT)}: invalid file mapping: {mapping!r}")
        repository_file(mapping["from"], manifest)

build_file = (ROOT / "gradle/build.gradle").read_text(encoding="utf-8")
properties = (ROOT / "gradle/gradle/wrapper/gradle-wrapper.properties").read_text(encoding="utf-8")
configured = re.search(r"wrapper\.gradleVersion\s*=\s*['\"]([^'\"]+)", build_file)
distributed = re.search(r"gradle-([0-9.]+)-bin\.zip", properties)
if not configured or not distributed or configured.group(1) != distributed.group(1):
    raise ValueError("Gradle wrapper version differs between build.gradle and gradle-wrapper.properties")

print(f"Validated {len(visited)} JSON manifests and Gradle {configured.group(1)} wrapper resources.")
