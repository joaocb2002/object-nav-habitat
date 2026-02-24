"""Generate camera intrinsics JSON from authoritative `SimConfig` sensor defaults.

This is an offline reproducibility utility script. It does not spin up a simulator
and it does not use Hydra run directories.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from objectnav.sim.config import SimConfig


def _compute_intrinsics(width: int, height: int, hfov_deg: float) -> dict[str, float | int]:
    """Compute pinhole intrinsics from image size and horizontal field of view."""
    hfov = math.radians(hfov_deg)
    fx = (width / 2.0) / math.tan(hfov / 2.0)

    # Compute vertical FOV from aspect ratio.
    vfov = 2.0 * math.atan(math.tan(hfov / 2.0) * (height / width))
    fy = (height / 2.0) / math.tan(vfov / 2.0)

    # Pixel-center principal point convention.
    cx = width / 2.0
    cy = height / 2.0

    return {
        "fx": float(fx),
        "fy": float(fy),
        "cx": float(cx),
        "cy": float(cy),
        "width": int(width),
        "height": int(height),
        "hfov": float(hfov_deg),
    }


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help=(
            "Output JSON path. Example: "
            "datasets/data_assets/objectnav/v1/camera_intrinsics.json"
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing an existing output file.",
    )
    return parser.parse_args()


def main() -> None:
    """Generate camera intrinsics from `SimConfig` defaults and write JSON output."""
    args = _parse_args()
    output_path = args.output.expanduser().resolve()

    if output_path.exists() and not args.overwrite:
        raise FileExistsError(
            f"Refusing to overwrite existing file: {output_path}. "
            "Pass --overwrite to replace it."
        )

    sim_cfg = SimConfig()
    payload = _compute_intrinsics(
        width=int(sim_cfg.rgb_width),
        height=int(sim_cfg.rgb_height),
        hfov_deg=float(sim_cfg.hfov_deg),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")

    print("Generated intrinsics at:", output_path)
    print(
        "Intrinsics summary:",
        f"fx={payload['fx']:.6f}, fy={payload['fy']:.6f},",
        f"cx={payload['cx']:.6f}, cy={payload['cy']:.6f},",
        f"size={payload['width']}x{payload['height']}, hfov={payload['hfov']:.3f}",
    )


if __name__ == "__main__":
    main()