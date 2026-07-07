from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QComboBox, QFileDialog, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QMessageBox,
                             QProgressBar, QPushButton, QVBoxLayout, QWidget)

from app.models.generated_image import GeneratedImage
from app.models.generation_settings import AspectRatio, GenerationSettings, Quality
from app.viewmodels.image_generator_view_model import ImageGeneratorViewModel
from app.views import icons, theme
from app.views.widgets.properties_dialog import PropertiesDialog
from app.views.widgets.toast import Toast

GENERATING_TEXT = "<div style='font-size:13px;'>Generating image&hellip; please wait</div>"


def _make_secondary_button(text: str, tooltip: str, icon_name: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setProperty("cssClass", "secondary")
    btn.setToolTip(tooltip)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setIcon(icons.icon(icon_name, color=theme.TEXT))
    btn.setIconSize(QSize(15, 15))
    return btn


class ImageGeneratorWindow(QMainWindow):
    def __init__(self, view_model: ImageGeneratorViewModel | None = None):
        super().__init__()
        self.view_model = view_model or ImageGeneratorViewModel()
        self._init_ui()
        self._bind_view_model()

    def _init_ui(self):
        self.setWindowTitle("AI Image Generator")
        self.setStyleSheet(theme.STYLESHEET)
        self.resize(640, 760)
        self.setMinimumSize(480, 560)

        self._placeholder_html = (
            f"<div><img src='{icons.icon_data_uri('fa5s.image', theme.MUTED_TEXT)}'></div>"
            "<div style='margin-top:6px;'>Your generated image will appear here</div>"
        )
        self._failed_html = (
            f"<div><img src='{icons.icon_data_uri('fa5s.exclamation-triangle', '#b91c1c')}'></div>"
            "<div style='margin-top:6px;'>Generation failed</div>"
        )

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(14)

        # Header
        title_label = QLabel("AI Image Generator")
        title_label.setObjectName("titleLabel")
        subtitle_label = QLabel("Describe anything and turn it into an image")
        subtitle_label.setObjectName("subtitleLabel")
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addSpacing(6)

        # Input Row
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        self.prompt_input = QLineEdit()
        self.prompt_input.setObjectName("promptInput")
        self.prompt_input.setPlaceholderText("Enter your prompt here (e.g., 'A cute astronaut cat')...")
        self.prompt_input.returnPressed.connect(self._on_generate_clicked)

        self.generate_btn = QPushButton("Generate")
        self.generate_btn.setObjectName("generateBtn")
        self.generate_btn.setToolTip("Generate image (Enter)")
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_btn.setIcon(icons.icon("fa5s.magic", color="white"))
        self.generate_btn.clicked.connect(self._on_generate_clicked)

        input_layout.addWidget(self.prompt_input, stretch=1)
        input_layout.addWidget(self.generate_btn)
        main_layout.addLayout(input_layout)

        # Generation Settings Row
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(10)

        aspect_label = QLabel("Aspect ratio")
        aspect_label.setObjectName("fieldLabel")
        self.aspect_combo = QComboBox()
        self.aspect_combo.setObjectName("aspectCombo")
        for ratio in AspectRatio:
            self.aspect_combo.addItem(ratio.value, ratio)

        quality_label = QLabel("Quality")
        quality_label.setObjectName("fieldLabel")
        self.quality_combo = QComboBox()
        self.quality_combo.setObjectName("qualityCombo")
        for quality in Quality:
            self.quality_combo.addItem(quality.display_label, quality)

        settings_layout.addWidget(aspect_label)
        settings_layout.addWidget(self.aspect_combo)
        settings_layout.addSpacing(12)
        settings_layout.addWidget(quality_label)
        settings_layout.addWidget(self.quality_combo)
        settings_layout.addStretch(1)
        main_layout.addLayout(settings_layout)

        # Indeterminate progress bar, only visible while a request is in flight
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        # Image Display Area
        self.image_label = QLabel()
        self.image_label.setObjectName("imageLabel")
        self.image_label.setMinimumHeight(340)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(theme.IMAGE_PLACEHOLDER_STYLE)
        self.image_label.setText(self._placeholder_html)
        main_layout.addWidget(self.image_label, stretch=1)

        # Action Row - only relevant once an image has been generated
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)
        self.save_btn = _make_secondary_button("Save", "Save this image to disk", "fa5s.save")
        self.save_btn.clicked.connect(self._on_save_clicked)
        self.create_more_btn = _make_secondary_button("Create More", "Generate another image", "fa5s.redo-alt")
        self.create_more_btn.clicked.connect(self._on_generate_clicked)
        self.delete_btn = _make_secondary_button("Delete", "Discard this image", "fa5s.trash-alt")
        self.delete_btn.clicked.connect(self.view_model.delete_image)
        self.properties_btn = _make_secondary_button("Properties", "View image metadata", "fa5s.info-circle")
        self.properties_btn.clicked.connect(self._on_properties_clicked)

        for btn in (self.save_btn, self.create_more_btn, self.delete_btn, self.properties_btn):
            btn.setEnabled(False)
            action_layout.addWidget(btn)
        main_layout.addLayout(action_layout)

        self.toast = Toast(central_widget)

    def _bind_view_model(self):
        vm = self.view_model
        vm.busy_changed.connect(self._on_busy_changed)
        vm.image_generated.connect(self._on_image_generated)
        vm.image_cleared.connect(self._on_image_cleared)
        vm.error_occurred.connect(self._on_error)
        vm.validation_error.connect(self._on_validation_error)
        vm.toast_requested.connect(self.toast.show_message)

    def _on_generate_clicked(self):
        settings = GenerationSettings(
            aspect_ratio=self.aspect_combo.currentData(),
            quality=self.quality_combo.currentData(),
        )
        self.view_model.generate_image(self.prompt_input.text(), settings)

    def _on_busy_changed(self, busy: bool):
        self.generate_btn.setEnabled(not busy)
        self.prompt_input.setEnabled(not busy)
        self.aspect_combo.setEnabled(not busy)
        self.quality_combo.setEnabled(not busy)
        self.progress_bar.setVisible(busy)
        if busy:
            self._set_actions_enabled(False)
            self.image_label.setStyleSheet(theme.IMAGE_PLACEHOLDER_STYLE)
            self.image_label.setText(GENERATING_TEXT)
        else:
            self._set_actions_enabled(self.view_model.has_image)

    def _on_image_generated(self, generated_image: GeneratedImage):
        pixmap = QPixmap.fromImage(generated_image.image)
        scaled_pixmap = pixmap.scaled(self.image_label.size(),
                                      Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.image_label.setStyleSheet(theme.IMAGE_LOADED_STYLE)
        self.image_label.setPixmap(scaled_pixmap)

    def _on_image_cleared(self):
        self.image_label.clear()
        self.image_label.setStyleSheet(theme.IMAGE_PLACEHOLDER_STYLE)
        self.image_label.setText(self._placeholder_html)
        self._set_actions_enabled(False)

    def _on_error(self, error_message: str):
        QMessageBox.critical(self, "Error", f"Failed to generate image:\n{error_message}")
        self.image_label.clear()
        self.image_label.setStyleSheet(theme.IMAGE_ERROR_STYLE)
        self.image_label.setText(self._failed_html)

    def _on_validation_error(self, message: str):
        QMessageBox.warning(self, "Warning", message)

    def _set_actions_enabled(self, enabled: bool):
        for btn in (self.save_btn, self.create_more_btn, self.delete_btn, self.properties_btn):
            btn.setEnabled(enabled)

    def _on_save_clicked(self):
        if not self.view_model.has_image:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "generated_image.png", "PNG Image (*.png);;JPEG Image (*.jpg)"
        )
        if not file_path:
            return
        self.view_model.save_image(file_path)

    def _on_properties_clicked(self):
        current_image = self.view_model.current_image
        if current_image is None:
            return
        dialog = PropertiesDialog(self, current_image, self.view_model.model_endpoint)
        dialog.exec()
