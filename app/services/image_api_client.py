import requests
from PyQt6.QtCore import QThread, pyqtSignal

from app.config import API_URL, HF_TOKEN


class ImageApiClient(QThread):
    """Handles the network request in a separate thread to prevent UI freezing."""
    finished = pyqtSignal(bytes)
    error = pyqtSignal(str)

    def __init__(self, prompt: str, width: int, height: int):
        super().__init__()
        self.prompt = prompt
        self.width = width
        self.height = height

    def run(self):
        # Adding a common User-Agent forces CloudFront to allow the HTTP POST method
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        payload = {
            "inputs": self.prompt,
            "parameters": {"width": self.width, "height": self.height},
        }

        try:
            # Higher resolutions take noticeably longer than the model's default size
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

            if response.status_code == 200:
                self.finished.emit(response.content)
            else:
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    detail = response.json().get("error", response.text)
                else:
                    detail = f"Non-JSON response (Content-Type: {content_type or 'unknown'})"
                self.error.emit(f"API Error (Status {response.status_code}): {detail}")
        except requests.exceptions.ConnectionError:
            self.error.emit(f"Could not connect to {API_URL}. Check your internet connection and the API_URL value.")
        except Exception as e:
            self.error.emit(str(e))
