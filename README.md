# AI Image Generator

A PyQt6 desktop app that turns text prompts into images using
[**FLUX.1-schnell**](https://huggingface.co/black-forest-labs/FLUX.1-schnell)
by Black Forest Labs, served through the
[Hugging Face Inference API](https://huggingface.co/docs/api-inference/index).

FLUX.1-schnell is a distilled, "step-distilled" variant of FLUX.1 tuned for
very fast text-to-image generation (as few as 1-4 diffusion steps) while
staying coherent up to around 1536px on its long edge. It's openly licensed
(Apache 2.0), which is why it's used here instead of the non-commercial
FLUX.1-dev.

## Features

- Prompt-to-image generation against the FLUX.1-schnell endpoint
- Aspect ratio presets: `1:1`, `16:9`, `9:16`, `1:2`
- Quality presets: Standard (1024px) / High (1536px), capped at what
  schnell can render coherently — true 4K would need a separate upscaling
  step, which isn't implemented here
- Save to disk with real PNG/JPEG re-encoding (not just a renamed file)
- Image properties dialog (prompt, dimensions, file size, generated-at, endpoint)
- Non-blocking UI — generation runs on a background thread

## Project structure

The app follows an MVVM layout:

```
app/
  models/         Plain data + settings (GeneratedImage, GenerationSettings)
  services/       ImageApiClient — the HF Inference API network call (QThread)
  viewmodels/     ImageGeneratorViewModel — state, validation, save/delete logic
  views/          ImageGeneratorWindow, theme, icons, and supporting widgets
main.py           Entry point
```

## Setup

### Prerequisites

- Python 3.13+ (developed against 3.13.3)
- A [Hugging Face account](https://huggingface.co/join) and an
  [access token](https://huggingface.co/settings/tokens) (a read-scoped
  token is enough)

### Install

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root (this file is git-ignored — never commit it):

```
API_URL=https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell
HF_TOKEN=hf_your_token_here
```

### Run

```powershell
python main.py
```

Type a prompt, pick an aspect ratio and quality, and click **Generate**.
