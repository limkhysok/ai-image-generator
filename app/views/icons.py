import base64

import qtawesome as qta
from PyQt6.QtCore import QBuffer, QByteArray, QIODevice
from PyQt6.QtGui import QIcon


def icon(name: str, color: str) -> QIcon:
    """A qtawesome vector icon. Must only be called after a QApplication exists."""
    return qta.icon(name, color=color)


def icon_data_uri(name: str, color: str, size: int = 40) -> str:
    """Render a qtawesome icon to a base64 PNG data URI, for embedding in rich-text QLabels."""
    pixmap = icon(name, color).pixmap(size, size)
    buffer = QByteArray()
    device = QBuffer(buffer)
    device.open(QIODevice.OpenModeFlag.WriteOnly)
    pixmap.save(device, "PNG")
    device.close()
    encoded = base64.b64encode(bytes(buffer)).decode("ascii")
    return f"data:image/png;base64,{encoded}"
