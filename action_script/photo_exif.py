#!/usr/bin/env python3
"""Extract EXIF data from photo posts and save exif.json next to each index.md."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from PIL import ExifTags, Image
from PIL.ExifTags import GPSTAGS

CONTENT_PHOTOS_DIR = Path(__file__).parent.parent / "content" / "photos"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".tiff", ".tif", ".png", ".webp"}

METERING_MODES = {
    0: "Unknown",
    1: "Average",
    2: "Center Weighted",
    3: "Spot",
    4: "Multi Spot",
    5: "Pattern",
    6: "Partial",
    255: "Other",
}
EXPOSURE_PROGRAMS = {
    0: "Not Defined",
    1: "Manual",
    2: "Normal Program",
    3: "Aperture Priority",
    4: "Shutter Priority",
    5: "Creative",
    6: "Action",
    7: "Portrait",
    8: "Landscape",
}
EXPOSURE_MODES = {0: "Auto", 1: "Manual", 2: "Auto Bracket"}


def _to_float(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if hasattr(value, "numerator") and hasattr(value, "denominator"):
        return 0.0 if value.denominator == 0 else value.numerator / value.denominator
    if isinstance(value, tuple) and len(value) == 2:
        return 0.0 if value[1] == 0 else value[0] / value[1]
    return float(value)


def _format_aperture(value) -> str:
    return f"f/{_to_float(value):.1f}"


def _format_shutter(value) -> str:
    f = _to_float(value)
    if f >= 1:
        return f"{f:.1f}s"
    frac = Fraction(f).limit_denominator(10000)
    return f"{frac.numerator}/{frac.denominator}s"


def _format_focal_length(value) -> str:
    return f"{_to_float(value):.0f}mm"


def _coerce(value) -> int | float | str:
    if isinstance(value, (int, float, str)):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").strip("\x00")
    return str(value)


def _dms_to_decimal(dms, ref: str) -> float | None:
    try:
        degrees = _to_float(dms[0])
        minutes = _to_float(dms[1])
        seconds = _to_float(dms[2])
        decimal = degrees + minutes / 60 + seconds / 3600
        return round(-decimal if ref in ("S", "W") else decimal, 6)
    except Exception:
        return None


def _process_tag(tag_name: str, value, result: dict) -> None:
    if tag_name == "FNumber":
        result["aperture"] = _format_aperture(value)
    elif tag_name == "ExposureTime":
        result["shutter_speed"] = _format_shutter(value)
    elif tag_name == "FocalLength":
        result["focal_length"] = _format_focal_length(value)
    elif tag_name == "FocalLengthIn35mmFilm":
        result["focal_length_35mm"] = f"{int(value)}mm"
    elif tag_name == "ISOSpeedRatings":
        result["iso"] = int(value)
    elif tag_name == "MeteringMode":
        result["metering_mode"] = METERING_MODES.get(int(value), str(value))
    elif tag_name == "ExposureProgram":
        result["exposure_program"] = EXPOSURE_PROGRAMS.get(int(value), str(value))
    elif tag_name == "ExposureMode":
        result["exposure_mode"] = EXPOSURE_MODES.get(int(value), str(value))
    elif tag_name == "WhiteBalance":
        result["white_balance"] = "Manual" if int(value) == 1 else "Auto"
    elif tag_name == "Flash":
        result["flash"] = "Fired" if int(value) & 0x1 else "Did not fire"
    elif tag_name == "ExposureBiasValue":
        result["exposure_bias"] = f"{_to_float(value):+.1f} EV"
    elif tag_name in ("Make", "Model", "LensModel", "LensMake", "DateTimeOriginal", "Software"):
        result[tag_name.lower()] = _coerce(value)


WANTED_TAGS = {
    "Make",
    "Model",
    "LensModel",
    "LensMake",
    "FNumber",
    "ExposureTime",
    "ISOSpeedRatings",
    "FocalLength",
    "FocalLengthIn35mmFilm",
    "DateTimeOriginal",
    "ExposureProgram",
    "ExposureMode",
    "ExposureBiasValue",
    "MeteringMode",
    "Flash",
    "WhiteBalance",
}


def extract_exif(image_path: Path) -> dict:
    result: dict = {}
    try:
        img = Image.open(image_path)
        raw = img.getexif()
        if not raw:
            return result

        tag_by_name = {v: k for k, v in ExifTags.TAGS.items()}

        # Main IFD (Make, Model, Software, …)
        for tag_name in WANTED_TAGS:
            tag_id = tag_by_name.get(tag_name)
            if tag_id is None:
                continue
            value = raw.get(tag_id)
            if value is not None:
                _process_tag(tag_name, value, result)

        # Exif sub-IFD (aperture, shutter, ISO, lens, …)
        exif_ifd = raw.get_ifd(0x8769)
        for tag_id, value in exif_ifd.items():
            tag_name = ExifTags.TAGS.get(tag_id)
            if tag_name in WANTED_TAGS:
                _process_tag(tag_name, value, result)

        # GPS IFD
        gps_ifd = raw.get_ifd(0x8825)
        if gps_ifd:
            gps: dict = {GPSTAGS.get(k, str(k)): v for k, v in gps_ifd.items()}
            lat = _dms_to_decimal(gps.get("GPSLatitude"), gps.get("GPSLatitudeRef", "N"))
            lon = _dms_to_decimal(gps.get("GPSLongitude"), gps.get("GPSLongitudeRef", "E"))
            if lat is not None and lon is not None:
                result["gps"] = {"latitude": lat, "longitude": lon}

    except Exception as exc:
        print(f"  Warning: cannot read EXIF from {image_path.name}: {exc}")

    return result


def find_images(post_dir: Path) -> list[Path]:
    return sorted(f for f in post_dir.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS)


def process_photos(dry_run: bool = False) -> None:
    index_files = sorted(CONTENT_PHOTOS_DIR.rglob("index.md"))
    print(f"Found {len(index_files)} photo posts")

    updated = skipped = 0
    for index_path in index_files:
        post_dir = index_path.parent
        images = find_images(post_dir)
        if not images:
            print(f"  [skip] {post_dir.name}: no image files")
            skipped += 1
            continue

        all_exif = {img.name: extract_exif(img) for img in images}

        output_path = post_dir / "exif.json"
        rel = output_path.relative_to(CONTENT_PHOTOS_DIR)
        if dry_run:
            print(f"  [dry-run] would write {rel} ({len(images)} image(s))")
        else:
            output_path.write_text(json.dumps(all_exif, indent=2, ensure_ascii=False) + "\n")
            print(f"  [ok] {rel} ({len(images)} image(s))")
        updated += 1

    print(f"\nDone: {updated} written, {skipped} skipped")


if __name__ == "__main__":
    import sys

    dry_run = "--dry-run" in sys.argv
    process_photos(dry_run=dry_run)
