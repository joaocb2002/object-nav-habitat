#!/usr/bin/env python3
"""Smoke test for ObjectNav data-assets loading."""

from __future__ import annotations

from pathlib import Path

from objectnav.config import DataAssetsConfig, load_objectnav_data_assets


def main() -> None:
    """Run a minimal loader check using repository default asset paths."""
    cfg = DataAssetsConfig(
        camera_intrinsics_path=Path("datasets/data_assets/objectnav/v1/camera_intrinsics.json"),
        indoor_classes_path=Path("datasets/data_assets/objectnav/v1/indoor_classes.json"),
        object_class_bins_path=Path("datasets/data_assets/objectnav/v1/object_class_bins.json"),
    )
    data_assets = load_objectnav_data_assets(cfg)

    print(
        "\nCamera intrinsics: "
        f"fx={data_assets.camera_intrinsics.fx}, "
        f"fy={data_assets.camera_intrinsics.fy}, "
        f"cx={data_assets.camera_intrinsics.cx}, "
        f"cy={data_assets.camera_intrinsics.cy}, "
        f"width={data_assets.camera_intrinsics.width}, "
        f"height={data_assets.camera_intrinsics.height}, "
        f"hfov={data_assets.camera_intrinsics.hfov}"
    )
    print(f"\nIndoor classes:")
    print("\n".join(f"  {k}: {v}" for k, v in data_assets.indoor_classes.items()))
    print(f"\nObject class bins:")
    for class_name, bins in data_assets.object_class_bins.items():
        bins_str = ", ".join(f"{b:.2f}" for b in bins)
        print(f"  {class_name}: [{bins_str}]")

    print("\nOK - data assets loader test passed.")


if __name__ == "__main__":
    main()
