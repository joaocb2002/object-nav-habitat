# Configs

This project uses a Hydra-style configuration layout.

- `config.yaml` is the root composition file (shared `paths` + `hydra.run.dir`).
- `config.yaml` intentionally composes `experiment` only; it does **not** directly select `data_assets`.
- `scene/` and `perception/` are config groups for environment and model settings.
- `data_assets/` selects versioned, reproducibility-critical data files (camera intrinsics, class ids, bins).
- `experiment/` contains reproducible experiment presets (compositions).
- `runs/` contains ad-hoc developer run presets (non-reproducible, local overrides).

How `data_assets` gets selected:
- Experiment presets (for example `experiment=baseline`) inject `/data_assets: default`.
- If you create a new experiment preset, include an explicit `/data_assets: ...` entry.

Why have `runs/` if we already have `experiment/`?
- `experiment/` is for versioned, reproducible presets (papers/benchmarks).
- `runs/` is for quick local overrides (debugging, profiling) without polluting experiment configs.

Precedence (highest to lowest):
1. CLI overrides
2. YAML composition (`configs/*.yaml`)
3. Code defaults (structured configs / dataclasses)

Typical usage:
- Reproducible run preset:
  - `python <entrypoint>.py experiment=baseline`
- Local debug override layered on top:
  - `python <entrypoint>.py experiment=baseline +runs=debug`
