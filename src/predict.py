"""Student starter: implement the Azure OpenAI Responses classification path."""

from pathlib import Path


LABELS_PATH = Path(__file__).parents[1] / "data" / "labels.json"


def predict(text: str) -> str:
    """Return one valid routing label.

    TODO: build a prompt, call client.responses.create(...), read the response,
    and validate the label. Do not put an API key in this file.
    """
    raise NotImplementedError("Implement your LLM classifier")


if __name__ == "__main__":
    # TODO: add a small CLI that reads a split and writes prediction records.
    raise SystemExit("Student task: implement the prediction CLI")
