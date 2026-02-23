# ObjectNav-Habitat 🧭

This repository is a **reproducible research stack** for running *Habitat-Sim / Habitat-Lab* experiments with a focus on the **ObjectNav** task. The long-term research direction is to combine:

- **Deep reinforcement learning** for control and policy learning
- **Probabilistic / Bayesian inference** for state estimation and decision-making under uncertainty

The codebase is intentionally structured to separate **infrastructure** (Docker images, scripts, dependency pinning) from **research logic** (agents, belief updates, perception, evaluation).

> Status: early-stage and evolving. Expect breaking changes while APIs and experiment protocols stabilize. 🚧

---

## Quickstart (Docker, recommended)

### Host prerequisites

- Linux (Ubuntu 22.04 recommended)
- NVIDIA GPU + recent driver
- Docker Engine
- NVIDIA Container Toolkit (required for GPU access)

### Sanity check

```bash
./scripts/bootstrap.sh
./scripts/run_dev.sh python scripts/sanity_check.py
```

### Interactive development

```bash
./scripts/run_dev.sh bash
```

Inside the container, the repository is mounted at `/workspace`; datasets are available at `/workspace/datasets` (also `/data`, read-only), and outputs at `/workspace/outputs` (also `/outputs`).

---

## Data and outputs

- Datasets are **not** bundled in the images.
- Code and configs use repository-relative paths (for example `datasets/...`, `outputs/...`).
- By default, `${DATA_DIR:-$PWD/datasets}` on the host is mounted to `/workspace/datasets` (and also `/data` for compatibility).
- By default, `${OUTPUT_DIR:-$PWD/outputs}` on the host is mounted to `/workspace/outputs` (and also `/outputs` for compatibility).
- This means `DATA_DIR` and `OUTPUT_DIR` choose the **host source directories** for bind mounts; they do not change path strings inside configs.

To override dataset/output locations:

```bash
export DATA_DIR=/path/to/datasets
export OUTPUT_DIR=/path/to/outputs
```

---

## Repository layout

```
.
├── configs/                 # Experiment configuration files
├── docker/                  # Reproducible images (base + project)
├── scripts/                 # Container entrypoints and helpers
├── src/objectnav/           # Research code (agents, belief, perception, sim utils)
├── datasets/                # (Optional) local datasets (not versioned in practice)
└── outputs/                 # Run artifacts (not versioned)
```

---

## Running experiments

This repo is evolving towards configuration-driven experiments under `configs/` and research modules under `src/objectnav/`.

- Use `./scripts/run_dev.sh python <script>.py` for iterative runs.
- Use `./scripts/run_train.sh python <script>.py` for non-interactive, long runs.

If you are adding new research components, prefer placing them under `src/objectnav/` and keeping them composable and seedable.

---

## Docker images (GHCR)

Prebuilt images are published to GitHub Container Registry:

- `ghcr.io/joaocb2002/object-nav-habitat/habitat-base`
- `ghcr.io/joaocb2002/object-nav-habitat/habitat-project`

Tags:

- `:main` — latest build from the main branch
- `:sha-<commit>` — immutable builds for exact reproducibility

---

## Troubleshooting

- GPU not visible in container: verify NVIDIA Container Toolkit installation.
- `import habitat_sim` fails: check driver compatibility and base image.
- Unexpected behavior after dependency changes: pull the latest image, or rebuild locally.

---

## Viewer utility

To inspect a digital scene visually (inside a Habitat environment):

```bash
habitat-viewer --dataset /path/to/<scene_dataset_config>.json <scene_name>
# Example (from repo root):
# habitat-viewer --dataset datasets/ai2thor-hab/ai2thor-hab/ai2thor-hab.scene_dataset_config.json FloorPlan1_physics
```

---

## Maintainer notes

Notes on updating dependency lockfiles, rebuilding/publishing images, and other repo maintenance live in `HELP.md`.

