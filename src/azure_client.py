"""Azure OpenAI connection setup supplied for the lab.

This helper intentionally stops before making a model request. Students build
the Responses API classification call in ``predict.py``.
"""

import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


def create_client() -> OpenAI:
    """Create an OpenAI SDK client configured for an Azure OpenAI resource."""
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    return OpenAI(
        base_url=f"{endpoint}/openai/v1/",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )


def deployment_name() -> str:
    """Return the Azure model deployment name used in ``model=...``."""
    return os.environ["AZURE_OPENAI_DEPLOYMENT"]
