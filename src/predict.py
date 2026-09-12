"""Student starter: implement the Azure OpenAI Responses classification path."""

import os

try:  # Works both as `python src/predict.py` and `import src.predict`.
    from .datasets import labels_path
except ImportError:  # pragma: no cover - direct-script fallback for students.
    from datasets import labels_path


# Set ROUTELAB_DATASET=challenge to work on the harder track. The standard
# track remains the default so existing beginner instructions keep working.
DATASET = os.getenv("ROUTELAB_DATASET", "standard")
LABELS_PATH = labels_path(DATASET)


def predict(text: str) -> str:
    """Return one valid routing label.

    TODO: build a prompt, call client.responses.create(...), read the response,
    and validate the label. Do not put an API key in this file.
    """
    raise NotImplementedError("Implement your LLM classifier")


if __name__ == "__main__":
    # TODO: add a small CLI that reads a split and writes prediction records.
    raise SystemExit("Student task: implement the prediction CLI")
