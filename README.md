# SoftCropper

[![PyPI version](https://badge.fury.io/py/softcropper.svg)](https://pypi.org/project/softcropper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/khaledalam/softcropper/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/khaledalam/softcropper/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/python-≥3.7-blue.svg)](https://www.python.org/)

**SoftCropper** is a powerful CLI tool that transforms rectangular images into square, print-ready formats with aesthetic borders and customizable text annotations — built for precision and automation.

> _Actively used by [CanvasMagnet](https://www.instagram.com/canvamagnet/) for order prep and A4 layout automation._

---

<img src="https://raw.githubusercontent.com/khaledalam/softcropper/main/tests/softcropper.png" />

---

### 📸 Example Results

| Before | ➡️ | After |
|--------|----|-------|
| <sub>Baby.webp (600×900)</sub><br><img src="https://raw.githubusercontent.com/khaledalam/softcropper/main/tests/assets/baby.webp" width="150"/> |  | <sub>Output (900×900)</sub><br><img src="https://raw.githubusercontent.com/khaledalam/softcropper/main/tests/assets/output/baby.webp" width="150"/> |
| <sub>Kid.jpg (1100×733)</sub><br><img src="https://raw.githubusercontent.com/khaledalam/softcropper/main/tests/assets/kid.jpg" width="150"/> |  | <sub>Output (1100×1100)</sub><br><img src="https://raw.githubusercontent.com/khaledalam/softcropper/main/tests/assets/output/kid.jpg" width="150"/> |

---

A4:
<img src="https://raw.githubusercontent.com/khaledalam/softcropper/main/tests/assets/a4_page_01.jpg" width="600"/>

## 🚀 Features

- ✅ Auto-square images with optional blurred/solid/gradient padding
- 🖼️ Add customizable **rounded borders** around photos
- ✍️ Annotate left/right/top/bottom with vertical or centered text (great for branding)
- 📄 Generate auto-arranged **A4 collage pages** from processed photos
- 📐 Resize final output by target size (e.g. `--size 5.5x5.5cm` or `--size 55x55mm`)
- 🧪 Includes CLI, Makefile, tests, and PyPI packaging

---

## 📦 Requirements

- Python `>= 3.7`
- `opencv-python`
- `numpy`

---

## 🔧 Installation

```bash
pip install softcropper
```

For local development:

```bash
make venv
make install
```

---

## ⚙️ CLI Usage

```bash
softcropper ./input_photos --mode blur --border --text \
  --left "@CanvaMagnet" \
  --right "+971 545800462" \
  --top "Preview" \
  --bottom "www.CanvaMagnet.com" \
  --size 5.5x5.5cm \
  --a4
```

### Options

| Flag           | Description                                               |
|----------------|-----------------------------------------------------------|
| `--mode`       | One of: `blur` (default), `solid`, `gradient`             |
| `--border`     | Add rounded frame around photo                            |
| `--text`       | Enable text mode (requires at least one `--left/right/top/bottom`) |
| `--left`       | Vertical text on left side                                |
| `--right`      | Vertical text on right side                               |
| `--top`        | Centered text above the image                             |
| `--bottom`     | Centered text below the image                             |
| `--size`       | Resize output image (supports `mm` or `cm`, e.g. `55x55mm`) |
| `--a4`         | Generate A4 page(s) from processed images                 |

---

## ✅ Testing

```bash
make test
```

Or manually:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/ -v
```

---

## 🛠️ Makefile Commands

```bash
make venv         # Create .venv
make install      # Install locally in editable mode
make test         # Run tests
make build        # Build wheel and source dist
make deploy       # Deploy to PyPI
make clean        # Remove virtualenv + build artifacts
```

---

## 📄 Changelog

See [CHANGELOG.md](./CHANGELOG.md)

---

## 🤝 Contribution

Pull requests are welcome! Open an issue or fork and submit a PR if you'd like to improve SoftCropper.

---

## Author

**Khaled Alam**  
📧 [khaledalam.net@gmail.com](mailto:khaledalam.net@gmail.com)  
🌍 [Website](https://khaledalam.net/) | [LinkedIn](https://www.linkedin.com/in/khaledalam/) | [Twitter/X](https://x.com/khaledalamxyz)
