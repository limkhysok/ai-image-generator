from PyQt6.QtCore import Qt, QPropertyAnimation, QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget


class Toast(QLabel):
    """A small self-dismissing notification bubble overlaid on the parent window."""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._parent_widget = parent
        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 220);
            color: white;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 13px;
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hide()

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)
        self._animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._animation.finished.connect(self._on_fade_finished)

    def show_message(self, text: str, duration_ms: int = 2200):
        self.setText(text)
        self.adjustSize()

        parent_rect = self._parent_widget.rect()
        x = (parent_rect.width() - self.width()) // 2
        y = parent_rect.height() - self.height() - 30
        self.move(x, y)

        self._opacity_effect.setOpacity(1.0)
        self.show()
        self.raise_()
        QTimer.singleShot(duration_ms, self._fade_out)

    def _fade_out(self):
        self._animation.stop()
        self._animation.setDuration(400)
        self._animation.setStartValue(1.0)
        self._animation.setEndValue(0.0)
        self._animation.start()

    def _on_fade_finished(self):
        self.hide()
