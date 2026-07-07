"""Shared visual style for the application's views."""

PRIMARY = "#000000"
PRIMARY_HOVER = "#262626"
PRIMARY_DISABLED = "#9ca3af"
TEXT = "#000000"
MUTED_TEXT = "#6b7280"
BORDER = "#d1d5db"
BACKGROUND = "#ffffff"
SURFACE = "#ffffff"

STYLESHEET = f"""
QMainWindow, QDialog {{
    background-color: {BACKGROUND};
    font-family: "Segoe UI", sans-serif;
}}

QLabel#titleLabel {{
    font-size: 20px;
    font-weight: 600;
    color: {TEXT};
}}

QLabel#subtitleLabel {{
    font-size: 12px;
    color: {MUTED_TEXT};
}}

QLineEdit#promptInput {{
    padding: 10px 14px;
    border: 1px solid {BORDER};
    border-radius: 0px;
    font-size: 14px;
    background: {SURFACE};
    color: {TEXT};
}}

QLineEdit#promptInput:focus {{
    border: 1px solid {PRIMARY};
}}

QLabel#fieldLabel {{
    font-size: 12px;
    color: {MUTED_TEXT};
}}

QComboBox {{
    padding: 7px 12px;
    border: 1px solid {BORDER};
    border-radius: 0px;
    background: {SURFACE};
    color: {TEXT};
    font-size: 13px;
}}

QComboBox:focus {{
    border: 1px solid {PRIMARY};
}}

QComboBox::drop-down {{
    border: none;
    width: 22px;
}}

QComboBox QAbstractItemView {{
    background: {SURFACE};
    color: {TEXT};
    border: 1px solid black;
    selection-background-color: {PRIMARY};
    selection-color: white;
    outline: none;
}}

QPushButton#generateBtn {{
    background-color: {PRIMARY};
    color: white;
    border: none;
    border-radius: 0px;
    padding: 10px 22px;
    font-size: 14px;
    font-weight: 600;
}}

QPushButton#generateBtn:hover {{
    background-color: {PRIMARY_HOVER};
}}

QPushButton#generateBtn:disabled {{
    background-color: {PRIMARY_DISABLED};
}}

QPushButton[cssClass="secondary"] {{
    background-color: {SURFACE};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 0px;
    padding: 8px 14px;
    font-size: 13px;
}}

QPushButton[cssClass="secondary"]:hover:enabled {{
    background-color: #f3f4f6;
    border-color: #9ca3af;
}}

QPushButton[cssClass="secondary"]:disabled {{
    color: #b0b5bd;
    border-color: #e5e7eb;
}}

QProgressBar {{
    border: none;
    border-radius: 0px;
    background-color: #e5e7eb;
}}

QProgressBar::chunk {{
    background-color: {PRIMARY};
    border-radius: 0px;
}}

QLabel#imageLabel {{
    border: 2px dashed {BORDER};
    border-radius: 0px;
    background-color: {SURFACE};
    color: {MUTED_TEXT};
}}

QFormLayout QLabel {{
    font-size: 13px;
    color: {TEXT};
}}
"""

IMAGE_PLACEHOLDER_STYLE = f"""
    border: 2px dashed {BORDER};
    border-radius: 0px;
    background-color: {SURFACE};
    color: {MUTED_TEXT};
"""

IMAGE_LOADED_STYLE = f"""
    border: 1px solid #e5e7eb;
    border-radius: 0px;
    background-color: {SURFACE};
"""

IMAGE_ERROR_STYLE = """
    border: 2px dashed #f87171;
    border-radius: 0px;
    background-color: #fef2f2;
    color: #b91c1c;
"""
