# 📦 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.8] – 2025-07-05

### ✨ Added
- ➕ `--border` flag to draw rounded border around image content
- ➕ `--text` flag to enable left, right, top, and bottom edge text
- ➕ `--left`, `--right`, `--top`, `--bottom` flags for customizable annotations
- ➕ `--a4` flag to generate paginated A4 collage output
- ➕ `--size WxH` flag to resize final output in `mm` or `cm` units

### 🛠️ Fixed
- ✅ Resolved OpenCV image save error on empty/missing images
- ✅ Fixed bottom text rendering bug where top text was reused

---

## [0.1.5] – 2025-06-01

### ✨ Added
- ✨ Added `--mode gradient` for gradient-colored borders
- ✨ Added `--mode solid` for solid-colored borders
- ✨ Added `--mode blur` for blur borders
- ⚡ Support for shorthand flags:
  - `-s` for solid mode
  - `-b` for blur mode
  - `-g` for gradient mode

---

## [0.1.4] – 2025-05-08

### ✨ Added
- 🚀 Initial CLI tool with default `blur` mode.
