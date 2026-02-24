# Data-assets scripts

Offline utilities for generating and normalizing reproducibility metadata.

## Camera intrinsics generation

Script:
- `scripts/data_assets/generate_camera_intrinsics.py`

What it uses as authoritative source:
- `objectnav.sim.config.SimConfig` sensor defaults (`rgb_height`, derived `rgb_width`, `hfov_deg`).

What it does **not** do:
- It does not launch Habitat-Sim.
- It does not use Hydra run directories.

Why:
- This script is intended as one-off reproducibility tooling, separate from experiment execution.

### Usage

```bash
python scripts/data_assets/generate_camera_intrinsics.py \
  --output datasets/data_assets/objectnav/v1/camera_intrinsics.json
```

If the output file already exists, pass `--overwrite` explicitly:

```bash
python scripts/data_assets/generate_camera_intrinsics.py \
  --output datasets/data_assets/objectnav/v1/camera_intrinsics.json \
  --overwrite
```

### Recommended workflow

1. Generate to a temporary output path and review values.
2. Promote to canonical path under `datasets/data_assets/objectnav/v1/`.
3. Commit only after verifying consistency with expected camera convention.
