from dataclasses import dataclass
from datetime import datetime

from PyQt6.QtGui import QImage


@dataclass
class GeneratedImage:
    """A generated image together with the prompt/metadata that produced it."""
    prompt: str
    image_bytes: bytes
    image: QImage
    generated_at: datetime
