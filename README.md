# Godot STEX to PNG Converter

A command-line tool for converting `.stex` image files from the Godot Engine into standard `.png` images by stripping the first 32-byte header.

## 🧠 What is a `.stex` File?

Godot’s `.stex` files are texture files used internally by the engine. These files have a 32-byte header that must be removed to obtain a valid `.png` file. This script handles that process automatically.

---

## 🚀 Features

- Converts `.stex` to `.png` by skipping the 32-byte header.
- Displays a visual progress bar in the terminal.
- Handles edge cases such as very small or empty files.
- Provides clear, color-coded status messages using `colorama`.

---

## 📦 Requirements

- Python 3.6+
- [`colorama`](https://pypi.org/project/colorama/)

Install it with:

```bash
pip install colorama
```

---

## 🔧 Usage

```bash
python godotstex2png.py <your_file>.stex
```

Example:

```bash
python godotstex2png.py texture.stex
```

