"""
Convert dark PNG backgrounds to actual alpha transparency.

For each input image:
  1. Pillow computes per-pixel luminance and sets alpha based on it.
  2. pngquant re-compresses the result with a lossy palette so the
     output PNG is comparable in size to the original.

Threshold tuning:
  - luminance below `threshold`            → alpha 0 (transparent)
  - luminance above `threshold + soft`     → alpha unchanged (opaque)
  - luminance between                      → smooth fade

Run from inside /home/claude/helios-site.
"""
from PIL import Image
import numpy as np
import subprocess
from pathlib import Path

# Rec. 601 luminance weights (good sRGB match)
LUM_R, LUM_G, LUM_B = 0.299, 0.587, 0.114


def make_transparent(input_path: Path, output_path: Path,
                     threshold: float = 24.0, soft: float = 28.0) -> None:
    """Convert dark pixels to transparent, then pngquant for size."""
    before_kb = input_path.stat().st_size / 1024

    # Step 1 — Pillow does the alpha transform
    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img, dtype=np.float32)

    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    lum = LUM_R * r + LUM_G * g + LUM_B * b

    factor = np.clip((lum - threshold) / soft, 0.0, 1.0)
    arr[..., 3] = a * factor

    # Write to a temp path so we can pngquant in place at the destination
    tmp = output_path.with_suffix(".tmp.png")
    Image.fromarray(arr.astype(np.uint8)).save(tmp, "PNG", optimize=True, compress_level=9)

    # Step 2 — pngquant for lossy palette compression
    subprocess.run([
        "pngquant",
        "--quality=80-95",
        "--speed=1",
        "--strip",
        "--force",
        "--output", str(output_path),
        str(tmp),
    ], check=True)
    tmp.unlink()

    after_kb = output_path.stat().st_size / 1024
    print(f"  {input_path.name}: {before_kb:.0f} KB → {after_kb:.0f} KB")


if __name__ == "__main__":
    base = Path("public/images")

    targets = [
        # (path, threshold, soft) — slightly different tuning per asset
        (base / "logos" / "helios-1993.png",  18.0, 32.0),  # softer to preserve amber glow
        (base / "logos" / "helios-2001.png",  24.0, 28.0),
        (base / "logos" / "iris-emblem.png",  20.0, 30.0),  # softer for ring glow
        (base / "products" / "nova.png",      24.0, 28.0),
        (base / "products" / "genesis.png",   24.0, 28.0),
        (base / "products" / "atlas.png",            18.0, 32.0),  # softer for amber screen glow
        (base / "products" / "titan.png",            24.0, 28.0),
        (base / "products" / "titan-display.png",    18.0, 32.0),  # softer for amber logo glow
        (base / "products" / "professional-hero.png", 18.0, 32.0),  # softer for amber terminal glow
        # The following are intentionally NOT processed — they are
        # lifestyle / composite scenes where dark areas are part of
        # the scene, not background:
        #   - nova-hero.png
        #   - consumer-home.png
        #   - professional-home.png
        #   - professional-hero.png
    ]

    print("Converting PNGs to true transparency:")
    for path, threshold, soft in targets:
        make_transparent(path, path, threshold=threshold, soft=soft)
    print("Done.")
