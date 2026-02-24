# ObjectNav-Habitat 🧭

Reproducible research stack for Habitat-Sim / Habitat-Lab experiments focused on ObjectNav.

Research direction:
- Deep reinforcement learning for control/policy learning
- Probabilistic / Bayesian inference for uncertainty-aware decision making

> Status: early-stage and evolving 🚧

---

## 1) What this repository provides

1. Docker-first, reproducible runtime setup
2. Hydra-based experiment/config composition
3. Research modules under `src/objectnav/` (belief, sim, perception, utilities)
4. Versioned lightweight data assets for reproducibility

---

## 2) Quickstart ⚡

### 2.1 Host prerequisites

- Linux (Ubuntu 22.04 recommended)
- NVIDIA GPU + recent driver
- Docker Engine
- NVIDIA Container Toolkit

### 2.2 Bootstrap and sanity check

```bash
./scripts/bootstrap.sh
./scripts/run_dev.sh python scripts/sanity_check.py
```

### 2.3 Open an interactive dev shell

```bash
./scripts/run_dev.sh bash
```

Container mount layout:
- Repo: `/workspace`
- Datasets: `/workspace/datasets` (also `/data`, read-only compatibility)
- Outputs: `/workspace/outputs` (also `/outputs` compatibility)

---

## 3) Data and reproducibility 📦

### 3.1 Runtime path behavior

1. Datasets are not bundled in Docker images.
2. Configs/scripts use repository-relative paths (for example `datasets/...`, `outputs/...`).
3. `${DATA_DIR:-$PWD/datasets}` selects host dataset bind source.
4. `${OUTPUT_DIR:-$PWD/outputs}` selects host output bind source.

Override mounts (host-side):

```bash
export DATA_DIR=/path/to/datasets
export OUTPUT_DIR=/path/to/outputs
```

### 3.2 Versioned data-assets (tracked in git)

Canonical assets are stored at:

- `datasets/data_assets/objectnav/v1/camera_intrinsics.json`
- `datasets/data_assets/objectnav/v1/indoor_classes.json`
- `datasets/data_assets/objectnav/v1/object_class_bins.json`

Hydra config group: `data_assets` (default: `data_assets=default`).

Note: this repository keeps `data_assets` composition at the experiment level.
The root config composes `experiment`, and presets such as `experiment=baseline`
inject `/data_assets: default`.

### 3.3 Regenerating / normalizing data-assets

```bash
python scripts/data_assets/normalize_data_assets.py \
  --camera-intrinsics <path/to/camera-intrinsics.json> \
  --indoor-classes <path/to/indoor-objects.json> \
  --object-bins <path/to/object-classes-bins.json> \
  --out-dir datasets/data_assets/objectnav/v1
```

Smoke test:

```bash
./scripts/run_dev.sh python scripts/tests/test_data_assets_loader.py
```

---

## 4) Running workflows 🧪

### 4.1 Iterative development runs

```bash
./scripts/run_dev.sh python <script>.py
```

Optional faster loop (skip editable reinstall on each invocation):

```bash
SKIP_EDITABLE_INSTALL=1 ./scripts/run_dev.sh python <script>.py
```

### 4.2 Long / non-interactive runs

```bash
./scripts/run_train.sh python <script>.py
```

Optional faster loop:

```bash
SKIP_EDITABLE_INSTALL=1 ./scripts/run_train.sh python <script>.py
```

---

## 5) Repository layout

```text
.
├── configs/                 # Hydra composition (experiments, sim, perception, data_assets)
├── docker/                  # Reproducible images (base + project)
├── scripts/                 # Entrypoints and helper scripts
│   ├── data_assets/         # Data-asset normalization/regeneration scripts
│   └── tests/               # Lightweight test scripts
├── src/objectnav/           # Core research code
├── datasets/                # Local datasets + tracked lightweight data-assets
└── outputs/                 # Run artifacts (ignored)
```

---

## 6) Docker images (GHCR)

Published images:
- `ghcr.io/joaocb2002/object-nav-habitat/habitat-base`
- `ghcr.io/joaocb2002/object-nav-habitat/habitat-project`

Tags:
- `:main` → latest main branch build
- `:sha-<commit>` → immutable reproducible build

---

## 7) Viewer utility 👀

```bash
habitat-viewer --dataset /path/to/<scene_dataset_config>.json <scene_name>
# Example:
# habitat-viewer --dataset datasets/ai2thor-hab/ai2thor-hab/ai2thor-hab.scene_dataset_config.json FloorPlan1_physics
```

---

## 8) Troubleshooting

1. GPU not visible in container → check NVIDIA Container Toolkit.
2. `import habitat_sim` fails → verify driver/image compatibility.
3. Dependency drift issues → pull latest image or rebuild.

---

## 9) Additional docs

- `configs/README.md` for config composition conventions
- `HELP.md` for maintainer workflows (locks, rebuild, publish)

