from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QFormLayout, QLabel, QPushButton, QWidget

from app.models.generated_image import GeneratedImage
from app.views import theme


def _value_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    return label


class PropertiesDialog(QDialog):
    """Shows metadata about a generated image."""

    def __init__(self, parent: QWidget, generated_image: GeneratedImage, model_endpoint: str):
        super().__init__(parent)
        self.setWindowTitle("Image Properties")
        self.setStyleSheet(theme.STYLESHEET)
        self.setMinimumWidth(380)

        image = generated_image.image
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setVerticalSpacing(10)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addRow("Prompt:", _value_label(generated_image.prompt))
        layout.addRow("Dimensions:", _value_label(f"{image.width()} x {image.height()} px"))
        layout.addRow("File size:", _value_label(f"{len(generated_image.image_bytes) / 1024:.1f} KB"))
        layout.addRow("Generated at:", _value_label(generated_image.generated_at.strftime("%Y-%m-%d %H:%M:%S")))
        layout.addRow("Model endpoint:", _value_label(model_endpoint))

        close_btn = QPushButton("Close")
        close_btn.setProperty("cssClass", "secondary")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        layout.addRow(close_btn)
