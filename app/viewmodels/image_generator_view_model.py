import os
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QImage

from app.config import API_URL
from app.models.generated_image import GeneratedImage
from app.models.generation_settings import GenerationSettings
from app.services.image_api_client import ImageApiClient


class ImageGeneratorViewModel(QObject):
    """Owns application state and business rules; the View binds to its signals."""

    busy_changed = pyqtSignal(bool)
    image_generated = pyqtSignal(GeneratedImage)
    image_cleared = pyqtSignal()
    error_occurred = pyqtSignal(str)
    validation_error = pyqtSignal(str)
    toast_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_image: GeneratedImage | None = None
        self._worker: ImageApiClient | None = None

    @property
    def has_image(self) -> bool:
        return self.current_image is not None

    @property
    def model_endpoint(self) -> str:
        return API_URL

    def generate_image(self, prompt: str, settings: GenerationSettings | None = None):
        prompt = prompt.strip()
        if not prompt:
            self.validation_error.emit("Prompt cannot be empty!")
            return

        width, height = (settings or GenerationSettings()).dimensions

        self.busy_changed.emit(True)

        self._worker = ImageApiClient(prompt, width, height)
        self._worker.finished.connect(lambda data: self._on_success(data, prompt))
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_success(self, image_bytes: bytes, prompt: str):
        image = QImage.fromData(image_bytes)
        self.current_image = GeneratedImage(
            prompt=prompt,
            image_bytes=image_bytes,
            image=image,
            generated_at=datetime.now(),
        )
        self.busy_changed.emit(False)
        self.image_generated.emit(self.current_image)
        self.toast_requested.emit("Image generated!")

    def _on_error(self, error_message: str):
        self.busy_changed.emit(False)
        self.error_occurred.emit(error_message)

    def save_image(self, file_path: str):
        if self.current_image is None:
            return
        if not self.current_image.image.save(file_path):
            self.error_occurred.emit(f"Could not save image to {file_path}")
            return
        self.toast_requested.emit(f"Saved to {os.path.basename(file_path)}")

    def delete_image(self):
        self.current_image = None
        self.image_cleared.emit()
        self.toast_requested.emit("Image deleted")
