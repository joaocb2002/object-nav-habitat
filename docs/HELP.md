# Maintainer Help 🛠️

This page collects maintainer-facing operations intentionally kept out of the main README.

---

## 1) 📦 Dependency management and lockfiles

The project uses a two-layer Docker image design:

1. `docker/base/` → heavy, slow-changing dependencies (Habitat-Sim / Habitat-Lab, CUDA, system libs)
2. `docker/project/` → repo-specific Python dependencies that change more frequently

### 1.1 Base image (conda lock)

Source:
- `docker/base/environment.yml`

Lockfile:
- `docker/base/conda-lock.yml`

Regenerate:

```bash
conda-lock -f docker/base/environment.yml -p linux-64 --lockfile docker/base/conda-lock.yml
```

Notes:
- Use the same `conda-lock` version expected by the base Dockerfile.
- If Python version changes, re-check all lock/build tooling.

### 1.2 Project image (pip lock via pip-tools)

Source:
- `docker/project/requirements.txt`

Lockfile:
- `docker/project/requirements.lock` (hashed, reproducible)

Regenerate (inside matching Python/image context):

```bash
python -m piptools compile \
  --generate-hashes \
  --allow-unsafe \
  -o docker/project/requirements.lock \
  docker/project/requirements.txt
```

---

## 2) 🚀 Image build / publish behavior

CI rebuild rules:

1. Changes under `docker/base/` → rebuild base image
2. Changes under `docker/project/` → rebuild project image

Published images (GHCR):
- `ghcr.io/joaocb2002/object-nav-habitat/habitat-base`
- `ghcr.io/joaocb2002/object-nav-habitat/habitat-project`

Tags:
- `:main` → latest from main
- `:sha-<commit>` → immutable/reproducible build

---

## 3) ▶️ Canonical run commands

1. Interactive dev container:

```bash
./scripts/run_dev.sh bash
```

2. Smoke test / import sanity:

```bash
./scripts/run_dev.sh python scripts/sanity_check.py
```

3. Non-interactive long runs:

```bash
./scripts/run_train.sh python <script>.py
```

Optional faster loop (skip editable reinstall):

```bash
SKIP_EDITABLE_INSTALL=1 ./scripts/run_dev.sh python <script>.py
SKIP_EDITABLE_INSTALL=1 ./scripts/run_train.sh python <script>.py
```

---

## 4) 🧭 Configuration mutability policy (important)

To keep the repo clear for future developers, treat configs by intent:

### 4.1 Experiment-facing (expected to vary)
- CLI overrides
- `configs/experiment/`
- `configs/perception/`
- `configs/scene/` (scene selection per experiment)
- `configs/runs/` (local dev overrides)

### 4.2 Authoritative defaults / invariants (change carefully)
- Core sim defaults in code: `src/objectnav/sim/config.py`
- Data-assets schema/loader: `src/objectnav/config/data_assets.py`
- Canonical data-assets files under `datasets/data_assets/...`

Rule of thumb:
- If value is part of an experiment design, vary it via YAML/CLI.
- If value defines canonical sensor/infrastructure assumptions, change deliberately and version outputs.

---

## 5) 🗂️ Datasets and outputs

- Datasets expected at `${DATA_DIR:-$PWD/datasets}` (host) and mounted into container.
- Outputs expected at `${OUTPUT_DIR:-$PWD/outputs}` and mounted to `/outputs`.
- Do not commit large artifacts in `outputs/` or full datasets.

For reproducibility metadata (small files), version under:
- `datasets/data_assets/objectnav/...`
