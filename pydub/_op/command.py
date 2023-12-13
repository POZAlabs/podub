from dataclasses import asdict, dataclass, field
from typing import Any

from ..audio_segment import AudioSegment
from . import enums


@dataclass
class AudioMergeOptions:
    def to_overlay_options(self, *args, **kwargs) -> list[dict[str, Any]]:
        return [asdict(self)]


@dataclass
class StaticMergeOptions(AudioMergeOptions):
    position: int = 0
    loop: bool = False
    times: int | None = None
    gain_during_overlay: float | None = None


@dataclass
class DynamicMergeOptions(AudioMergeOptions):
    loop_interval: int
    start: int = 0
    gain_during_overlay: float | None = None

    def to_overlay_options(self, source_duration: int) -> list[dict[str, Any]]:
        num_loops = (source_duration - self.start) // self.loop_interval

        return [
            StaticMergeOptions(
                position=(
                    self.start + (i * self.loop_interval)
                    if self.start
                    else (i + 1) * self.loop_interval
                ),
                gain_during_overlay=self.gain_during_overlay,
            ).to_overlay_options()[0]
            for i in range(num_loops)
        ]


@dataclass
class AudioMergeInput:
    audio: AudioSegment
    options: AudioMergeOptions = field(default_factory=StaticMergeOptions)


@dataclass
class MergeAudioCommand:
    to: AudioSegment
    input: AudioMergeInput


@dataclass
class MergeAudiosCommand:
    inputs: list[AudioMergeInput]
    policy: enums.OverlayPolicy = enums.OverlayPolicy.FIRST
