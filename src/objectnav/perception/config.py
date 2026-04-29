from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple, Union


@dataclass(frozen=True)
class YoloConfig:
    """Configuration for YOLO-based perception.

    Prefer overriding via a run config (YAML) rather than editing code.
    """

    # --- Model parameters ---
    weights_path: Union[str, Path] = field(
        default=Path("datasets/models/yolo11x.pt"),
        metadata={"help": "Path to YOLO weights file."},
    )
    device: str = field(
        default="cuda:0",
        metadata={
            "help": "Torch device specifier. Supports 'auto', 'cpu', 'cuda', 'cuda:0', 'cuda:1', etc."
        },
    )

    # --- Inference parameters ---
    conf: float = field(default=0.25, metadata={"help": "Confidence threshold."})
    iou: float = field(default=0.7, metadata={"help": "IoU threshold for NMS."})
    imgsz: Tuple[int, int] = field(
        default=(1088, 1920),
        metadata={"help": "Image (height, width) for inference."},
    )
    rect: bool = field(default=True, metadata={"help": "Enable rectangular inference."})
    half: bool = field(default=False, metadata={"help": "Use half precision when supported."})
    max_det: int = field(default=30, metadata={"help": "Maximum detections per image."})
    verbose: bool = field(default=False, metadata={"help": "Enable per-inference logging."})

    # --- Patches ---
    use_softmax_patch: bool = field(
        default=True,
        metadata={"help": "Apply softmax patch to expose class probabilities."},
    )
    softmax_temperature: float = field(
        default=2.4,
        metadata={"help": "Softmax temperature for class probabilities."},
    )

    def weights_path_str(self) -> str:
        return str(self.weights_path)

    @classmethod
    def from_mapping(
        cls,
        cfg: Mapping[str, Any],
        *,
        resolve_path: Optional[Callable[[str], str]] = None,
    ) -> "YoloConfig":
        """Build a :class:`YoloConfig` from a mapping-like config object.

        This is intended for Hydra/OmegaConf integration while keeping a typed,
        immutable dataclass for downstream code.

        Args:
            cfg: Mapping with YOLO configuration keys.
            resolve_path: Optional path resolver (e.g., ``hydra.utils.to_absolute_path``)
                applied to ``weights_path``.

        Raises:
            ValueError: If unknown keys are present or if ``imgsz`` is malformed.
        """
        field_names = set(cls.__dataclass_fields__.keys())
        cfg_keys = set(cfg.keys())
        unknown = cfg_keys - field_names
        if unknown:
            unknown_csv = ", ".join(sorted(unknown))
            raise ValueError(f"Unknown YOLO config keys: {unknown_csv}")

        data = dict(cfg)

        if "imgsz" in data:
            imgsz_val = data["imgsz"]
            if not isinstance(imgsz_val, Sequence) or isinstance(imgsz_val, (str, bytes)):
                raise ValueError("'imgsz' must be a 2-element sequence [height, width].")
            if len(imgsz_val) != 2:
                raise ValueError("'imgsz' must have exactly 2 elements: [height, width].")
            data["imgsz"] = (int(imgsz_val[0]), int(imgsz_val[1]))

        if "weights_path" in data:
            weights_path = str(data["weights_path"])
            if resolve_path is not None:
                weights_path = resolve_path(weights_path)
            data["weights_path"] = Path(weights_path)

        return cls(**data)
