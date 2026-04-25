"""
generate_zenodo_manifest.py

Create a Zenodo-ready manifest.csv for the ecoacoustic segmentation dataset.

This script is intentionally tolerant of inconsistent annotation files. If a file is
missing columns such as sound_path, start_time, end_time, or propagated_class, the
script continues and records unavailable values as blank/NA. Warnings are written to
manifest_warnings.csv.

Typical use:
    python generate_zenodo_manifest.py

Expected input:
    data/annotations/*.csv

Outputs:
    zenodo_manifest/manifest.csv
    zenodo_manifest/manifest_warnings.csv
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd


DEFAULT_CHUNK_DURATION_SECONDS = 4.5


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def normalise_column_name(name: str) -> str:
    """Normalise column names for flexible matching."""
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def find_column(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    """
    Return the first matching column from a list of candidate names.
    Matching is case-insensitive and punctuation-insensitive.
    """
    norm_to_original = {normalise_column_name(c): c for c in df.columns}

    for candidate in candidates:
        norm = normalise_column_name(candidate)
        if norm in norm_to_original:
            return norm_to_original[norm]

    return None


def parse_annotation_filename(path: Path) -> dict:
    """
    Parse filenames such as:
        DUVAL-DRYA-20210419T000000+1000_REC_annotations.csv
        DUVAL-DRYA-20210419T000000+1000_REC_annotations(1).csv
        WAMBIANA-WETBB.csv

    Returns available metadata. Missing parts are returned as blank strings.
    """
    stem = path.stem
    stem = re.sub(r"\(\d+\)$", "", stem)
    stem = stem.replace("_annotations", "")

    parts = stem.split("-", maxsplit=2)

    site = parts[0] if len(parts) >= 1 else ""
    area = parts[1] if len(parts) >= 2 else ""
    recording_name = parts[2] if len(parts) >= 3 else ""

    date_raw = ""
    date_iso = ""

    if recording_name:
        match = re.search(r"(\d{8})T(\d{6})([+-]\d{4})?_REC", recording_name)
        if match:
            date_raw = match.group(1)
            date_iso = f"{date_raw[0:4]}-{date_raw[4:6]}-{date_raw[6:8]}"

    recording_id_from_filename = stem if recording_name else ""

    return {
        "source_annotation_file": path.name,
        "site": site,
        "area": area,
        "recording_name": recording_name,
        "recording_id_from_filename": recording_id_from_filename,
        "date_raw": date_raw,
        "date": date_iso,
    }


def extract_chunk_index_from_sound_path(sound_path: str) -> Optional[int]:
    """
    Extract chunk index from a path ending like:
        20210419T000000+1000_REC_184.wav

    Returns None if unavailable.
    """
    if pd.isna(sound_path):
        return None

    filename = Path(str(sound_path).replace("\\", "/")).name
    match = re.search(r"_([0-9]+)\.wav$", filename)

    if not match:
        return None

    return int(match.group(1))


def clean_text_for_filename(value) -> str:
    """Make a string safe for filenames."""
    if pd.isna(value) or str(value).strip() == "":
        return "unknown"

    value = str(value).strip()
    value = re.sub(r"[^\w\-.+]+", "_", value)
    return value.strip("_") or "unknown"


def first_non_null(row: pd.Series, columns: list[Optional[str]]):
    """Return first non-null value from row using candidate columns."""
    for col in columns:
        if col is not None and col in row.index and not pd.isna(row[col]):
            return row[col]
    return pd.NA


def to_float_or_na(value):
    try:
        if pd.isna(value):
            return pd.NA
        return float(value)
    except Exception:
        return pd.NA


def infer_start_end(
    row: pd.Series,
    start_col: Optional[str],
    end_col: Optional[str],
    sound_path_col: Optional[str],
    chunk_duration: float,
) -> Tuple[object, object, object, str]:
    """
    Infer start/end time.

    Priority:
    1. Use explicit start/end columns if available.
    2. Use sound_path chunk index if available.
    3. Return NA values.
    """
    start = to_float_or_na(row[start_col]) if start_col else pd.NA
    end = to_float_or_na(row[end_col]) if end_col else pd.NA

    if not pd.isna(start) and not pd.isna(end):
        duration = end - start
        return start, end, duration, "columns"

    chunk_index = None
    if sound_path_col:
        chunk_index = extract_chunk_index_from_sound_path(row.get(sound_path_col, pd.NA))

    if chunk_index is not None:
        start = chunk_index * chunk_duration
        end = (chunk_index + 1) * chunk_duration
        duration = chunk_duration
        return start, end, duration, "sound_path_chunk_index"

    return pd.NA, pd.NA, pd.NA, "unavailable"


def infer_archive_file(site: str, area: str, date: str) -> str:
    if site and area and date:
        return f"audio_{site}_{area}_{date}.zip"
    if site and area:
        return f"audio_{site}_{area}.zip"
    if site:
        return f"audio_{site}.zip"
    return "audio_unknown.zip"


# ---------------------------------------------------------------------
# Manifest generation
# ---------------------------------------------------------------------

def process_annotation_file(path: Path, chunk_duration: float) -> tuple[pd.DataFrame, list[dict]]:
    metadata = parse_annotation_filename(path)
    warnings: list[dict] = []

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        warnings.append({
            "source_annotation_file": path.name,
            "row_index": "",
            "warning": f"Could not read CSV: {exc}",
        })
        return pd.DataFrame(), warnings

    # Flexible column matching
    sound_path_col = find_column(df, ["sound_path", "sound path", "filepath", "file_path", "path", "filename"])
    start_col = find_column(df, ["start_time", "start", "begin time (s)", "begin_time_s", "start_sec", "start_seconds"])
    end_col = find_column(df, ["end_time", "end", "end time (s)", "end_time_s", "end_sec", "end_seconds"])
    label_col = find_column(df, ["propagated_class", "label", "species", "class", "sound_type"])
    cluster_col = find_column(df, ["cluster", "cluster_id", "class"])
    sampled_col = find_column(df, ["sampled"])
    x_col = find_column(df, ["x", "umap_x"])
    y_col = find_column(df, ["y", "umap_y"])
    z_col = find_column(df, ["z", "umap_z"])

    required_for_audio = {
        "sound_path": sound_path_col,
        "start": start_col,
        "end": end_col,
    }

    for logical_name, col in required_for_audio.items():
        if col is None:
            warnings.append({
                "source_annotation_file": path.name,
                "row_index": "",
                "warning": f"Missing column: {logical_name}. Manifest will continue with blank/inferred values where possible.",
            })

    rows = []

    for idx, row in df.iterrows():
        sound_path = row[sound_path_col] if sound_path_col else pd.NA
        chunk_index = extract_chunk_index_from_sound_path(sound_path) if sound_path_col else None

        start_sec, end_sec, duration_sec, timing_source = infer_start_end(
            row=row,
            start_col=start_col,
            end_col=end_col,
            sound_path_col=sound_path_col,
            chunk_duration=chunk_duration,
        )

        label = first_non_null(row, [label_col])
        label_clean = clean_text_for_filename(label)

        site = metadata["site"]
        area = metadata["area"]
        date = metadata["date"]

        archive_file = infer_archive_file(site, area, date)

        if chunk_index is not None:
            audio_filename = f"{site}_{area}_{date}_chunk-{chunk_index:06d}_label-{label_clean}.wav"
        else:
            audio_filename = pd.NA
            warnings.append({
                "source_annotation_file": path.name,
                "row_index": idx,
                "warning": "Could not infer audio filename because sound_path/chunk index is unavailable.",
            })

        rows.append({
            "source_annotation_file": metadata["source_annotation_file"],
            "site": site,
            "area": area,
            "date": date,
            "date_raw": metadata["date_raw"],
            "recording_name": metadata["recording_name"],
            "recording_id_from_filename": metadata["recording_id_from_filename"],
            "row_index": idx,
            "chunk_index": chunk_index if chunk_index is not None else pd.NA,
            "start_sec": start_sec,
            "end_sec": end_sec,
            "duration_sec": duration_sec,
            "timing_source": timing_source,
            "label": label,
            "label_clean": label_clean,
            "cluster_or_class": row[cluster_col] if cluster_col else pd.NA,
            "sampled": row[sampled_col] if sampled_col else pd.NA,
            "sound_path": sound_path,
            "audio_filename": audio_filename,
            "archive_file": archive_file,
            "umap_x": row[x_col] if x_col else pd.NA,
            "umap_y": row[y_col] if y_col else pd.NA,
            "umap_z": row[z_col] if z_col else pd.NA,
            "has_audio_mapping": not pd.isna(audio_filename) and not pd.isna(start_sec) and not pd.isna(end_sec),
            "notes": "" if not pd.isna(audio_filename) else "Audio mapping unavailable from this annotation row.",
        })

    return pd.DataFrame(rows), warnings


def generate_manifest(annotation_dir: Path, output_dir: Path, chunk_duration: float) -> None:
    annotation_files = sorted(annotation_dir.glob("*.csv"))

    output_dir.mkdir(parents=True, exist_ok=True)

    if not annotation_files:
        raise FileNotFoundError(f"No CSV files found in {annotation_dir}")

    manifest_parts = []
    all_warnings = []

    for path in annotation_files:
        print(f"Processing {path.name}")
        part, warnings = process_annotation_file(path, chunk_duration)
        if not part.empty:
            manifest_parts.append(part)
        all_warnings.extend(warnings)

    if manifest_parts:
        manifest = pd.concat(manifest_parts, ignore_index=True)
    else:
        manifest = pd.DataFrame()

    manifest_path = output_dir / "manifest.csv"
    warnings_path = output_dir / "manifest_warnings.csv"

    manifest.to_csv(manifest_path, index=False)
    pd.DataFrame(all_warnings).to_csv(warnings_path, index=False)

    print()
    print(f"Manifest written to: {manifest_path}")
    print(f"Warnings written to: {warnings_path}")
    print(f"Rows in manifest: {len(manifest)}")
    print(f"Warnings: {len(all_warnings)}")

    if "has_audio_mapping" in manifest.columns:
        mapped = int(manifest["has_audio_mapping"].fillna(False).sum())
        print(f"Rows with audio mapping: {mapped}")
        print(f"Rows without audio mapping: {len(manifest) - mapped}")


def main():
    parser = argparse.ArgumentParser(description="Generate Zenodo manifest for ecoacoustic segmentation dataset.")
    parser.add_argument(
        "--annotation-dir",
        type=Path,
        default=Path("data/annotations"),
        help="Directory containing annotation CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("zenodo_manifest"),
        help="Directory where manifest.csv and manifest_warnings.csv will be written.",
    )
    parser.add_argument(
        "--chunk-duration",
        type=float,
        default=DEFAULT_CHUNK_DURATION_SECONDS,
        help="Duration of each audio chunk in seconds, used when inferring time from sound_path.",
    )

    args = parser.parse_args()

    generate_manifest(
        annotation_dir=args.annotation_dir,
        output_dir=args.output_dir,
        chunk_duration=args.chunk_duration,
    )


if __name__ == "__main__":
    main()
