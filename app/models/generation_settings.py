from dataclasses import dataclass
from enum import Enum


class AspectRatio(Enum):
    SQUARE = "1:1"
    LANDSCAPE = "16:9"
    PORTRAIT = "9:16"
    TALL = "1:2"

    @property
    def ratio(self) -> tuple[int, int]:
        width, _, height = self.value.partition(":")
        return int(width), int(height)


class Quality(Enum):
    STANDARD = "Standard"
    HIGH = "High"

    @property
    def long_edge(self) -> int:
        return _LONG_EDGE[self]

    @property
    def display_label(self) -> str:
        return f"{self.value} ({self.long_edge}px)"


_LONG_EDGE = {
    Quality.STANDARD: 1024,
    Quality.HIGH: 1536,
}


def _round_to_16(value: float) -> int:
    return max(16, round(value / 16) * 16)


@dataclass(frozen=True)
class GenerationSettings:
    """User-facing generation options, translated into concrete request dimensions.

    The long edge is capped at Quality.HIGH's 1536px: FLUX.1-schnell is a distilled
    model tuned around ~1024-1536px and its output coherence degrades noticeably
    beyond that, so "4K" is intentionally not offered as a direct request size.
    """
    aspect_ratio: AspectRatio = AspectRatio.SQUARE
    quality: Quality = Quality.STANDARD

    @property
    def dimensions(self) -> tuple[int, int]:
        width_ratio, height_ratio = self.aspect_ratio.ratio
        long_edge = self.quality.long_edge
        if width_ratio >= height_ratio:
            width = long_edge
            height = _round_to_16(long_edge * height_ratio / width_ratio)
        else:
            height = long_edge
            width = _round_to_16(long_edge * width_ratio / height_ratio)
        return width, height
