#!/usr/bin/env python3
"""Normalize legacy ObjectNav data-asset files into canonical repository format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


def _read_json(path: Path) -> Any:
    """Read a JSON file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, payload: Any) -> None:
    """Write JSON with deterministic formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _normalize_indoor_classes(raw: Mapping[str, Any]) -> dict[str, dict[str, str]]:
    """Convert legacy indoor_classes list-of-singleton-maps to one mapping."""
    classes_raw = raw.get("indoor_classes")
    if not isinstance(classes_raw, list):
        raise ValueError("Expected 'indoor_classes' to be a list in legacy file.")

    merged: dict[str, str] = {}
    for item in classes_raw:
        if not isinstance(item, Mapping) or len(item) != 1:
            raise ValueError("Each indoor class entry must be a single-key object.")
        key, value = next(iter(item.items()))
        merged[str(key)] = str(value)

    return {"indoor_classes": merged}


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera-intrinsics", type=Path, required=True)
    parser.add_argument("--indoor-classes", type=Path, required=True)
    parser.add_argument("--object-bins", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    camera_intrinsics = _read_json(args.camera_intrinsics)
    indoor_classes_legacy = _read_json(args.indoor_classes)
    object_bins = _read_json(args.object_bins)

    indoor_classes_canonical = _normalize_indoor_classes(indoor_classes_legacy)

    _write_json(args.out_dir / "camera_intrinsics.json", camera_intrinsics)
    _write_json(args.out_dir / "indoor_classes.json", indoor_classes_canonical)
    _write_json(args.out_dir / "object_class_bins.json", object_bins)

    print("Wrote normalized assets to", args.out_dir)


if __name__ == "__main__":
    main()
