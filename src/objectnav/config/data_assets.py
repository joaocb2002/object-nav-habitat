from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


@dataclass(frozen=True)
class CameraIntrinsics:
    """Pinhole camera intrinsics and image geometry."""

    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int
    hfov: float


@dataclass(frozen=True)
class DataAssetsConfig:
    """Resolved paths for versioned ObjectNav data assets."""

    camera_intrinsics_path: Path
    indoor_classes_path: Path
    object_class_bins_path: Path

    @classmethod
    def from_mapping(
        cls,
        cfg: Mapping[str, Any],
        *,
        resolve_path: Callable[[str], str] | None = None,
    ) -> "DataAssetsConfig":
        """Build config from a Hydra/OmegaConf mapping.

        Args:
            cfg: Mapping with keys for asset paths.
            resolve_path: Optional path resolver (for example
                ``hydra.utils.to_absolute_path``).
        """
        required_keys = {
            "camera_intrinsics_path",
            "indoor_classes_path",
            "object_class_bins_path",
        }
        unknown = set(cfg.keys()) - required_keys
        missing = required_keys - set(cfg.keys())
        if unknown:
            unknown_csv = ", ".join(sorted(unknown))
            raise ValueError(f"Unknown data_assets keys: {unknown_csv}")
        if missing:
            missing_csv = ", ".join(sorted(missing))
            raise ValueError(f"Missing required data_assets keys: {missing_csv}")

        def _resolve(value: Any) -> Path:
            path_str = str(value)
            if resolve_path is not None:
                path_str = resolve_path(path_str)
            path = Path(path_str)
            if not path.exists():
                raise FileNotFoundError(f"Data asset path does not exist: {path}")
            return path

        return cls(
            camera_intrinsics_path=_resolve(cfg["camera_intrinsics_path"]),
            indoor_classes_path=_resolve(cfg["indoor_classes_path"]),
            object_class_bins_path=_resolve(cfg["object_class_bins_path"]),
        )


@dataclass(frozen=True)
class ObjectNavDataAssets:
    """Container for ObjectNav reproducibility assets."""

    camera_intrinsics: CameraIntrinsics
    indoor_classes: Mapping[int, str]
    object_class_bins: Mapping[str, Sequence[float]]


def _read_json(path: Path) -> Any:
    """Read and decode a JSON file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_camera_intrinsics(path: Path) -> CameraIntrinsics:
    """Load and validate camera intrinsics JSON."""
    raw = _read_json(path)
    required = {"fx", "fy", "cx", "cy", "width", "height", "hfov"}
    missing = required - set(raw.keys())
    if missing:
        missing_csv = ", ".join(sorted(missing))
        raise ValueError(f"Missing keys in camera intrinsics file '{path}': {missing_csv}")

    return CameraIntrinsics(
        fx=float(raw["fx"]),
        fy=float(raw["fy"]),
        cx=float(raw["cx"]),
        cy=float(raw["cy"]),
        width=int(raw["width"]),
        height=int(raw["height"]),
        hfov=float(raw["hfov"]),
    )


def _load_indoor_classes(path: Path) -> Mapping[int, str]:
    """Load and validate class-id to class-name mapping."""
    raw = _read_json(path)
    mapping = raw.get("indoor_classes")
    if not isinstance(mapping, Mapping):
        raise ValueError(
            f"Expected object key 'indoor_classes' to be a mapping in '{path}'."
        )

    normalized: dict[int, str] = {}
    for k, v in mapping.items():
        normalized[int(k)] = str(v)
    return normalized


def _load_object_class_bins(path: Path) -> Mapping[str, Sequence[float]]:
    """Load and validate class-wise bin boundaries."""
    raw = _read_json(path)
    if not isinstance(raw, Mapping):
        raise ValueError(f"Expected top-level object in object class bins file '{path}'.")

    normalized: dict[str, tuple[float, ...]] = {}
    for class_name, bins in raw.items():
        if not isinstance(bins, Sequence) or isinstance(bins, (str, bytes)):
            raise ValueError(
                f"Bins for class '{class_name}' must be an array in file '{path}'."
            )
        normalized[str(class_name)] = tuple(float(x) for x in bins)
    return normalized


def load_objectnav_data_assets(cfg: DataAssetsConfig) -> ObjectNavDataAssets:
    """Load ObjectNav reproducibility data assets from configured JSON files."""
    return ObjectNavDataAssets(
        camera_intrinsics=_load_camera_intrinsics(cfg.camera_intrinsics_path),
        indoor_classes=_load_indoor_classes(cfg.indoor_classes_path),
        object_class_bins=_load_object_class_bins(cfg.object_class_bins_path),
    )
