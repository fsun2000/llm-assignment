"""Dataset selection helpers for the standard and challenge RouteLab tracks."""

from pathlib import Path


DATA_ROOT = Path(__file__).parents[1] / "data"
DATASETS = {
    "standard": DATA_ROOT,
    "challenge": DATA_ROOT / "challenge",
}


def dataset_path(dataset: str, split: str) -> Path:
    """Return a validated JSONL path for a named dataset and split."""
    if dataset not in DATASETS:
        choices = ", ".join(DATASETS)
        raise ValueError(f"Unknown dataset {dataset!r}. Choose one of: {choices}.")
    if split not in {"train", "dev", "final"}:
        raise ValueError("split must be 'train', 'dev', or 'final'.")
    return DATASETS[dataset] / f"{split}.jsonl"


def labels_path(dataset: str) -> Path:
    """Return the label-definition file for a named dataset."""
    if dataset not in DATASETS:
        choices = ", ".join(DATASETS)
        raise ValueError(f"Unknown dataset {dataset!r}. Choose one of: {choices}.")
    return DATASETS[dataset] / "labels.json"
