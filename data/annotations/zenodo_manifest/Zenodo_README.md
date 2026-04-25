# Dataset: An Efficient Pipeline for the Unsupervised Segmentation of Heterogeneous Natural Soundscapes

## Overview

This dataset accompanies the paper:

**An Efficient Pipeline for the Unsupervised Segmentation of Heterogeneous Natural Soundscapes**

The dataset contains the audio clips, annotation files, processed features, and experimental outputs used to evaluate an unsupervised segmentation pipeline for heterogeneous ecoacoustic soundscapes.

The study uses fixed-length soundscape segments extracted from continuous passive acoustic recordings. These segments were processed using feature extraction, dimensionality reduction, clustering, and post-hoc ecological labelling. The resulting data support the analysis of how unsupervised clustering can organise complex natural soundscapes into acoustically coherent and ecologically interpretable groups.

## Dataset Structure

```text
.
├── README.md
├── manifest.csv
├── annotations.zip
├── audio_datasets/
│   └── uploads/
│       ├── DUVAL/
│       ├── MOURACHAN/
│       ├── RINYIRRU/
│       ├── TARCUTTA/
│       ├── UNDARA/
│       └── WAMBIANA/
├── processed_features.zip
└── results.zip
```

## Study Sites

The dataset contains six site-level soundscape subsets:

```text
DUVAL
MOURACHAN
RINYIRRU
TARCUTTA
UNDARA
WAMBIANA
```

Each site corresponds to a selected recording day and recorder area used in the segmentation study. The recordings contain heterogeneous natural soundscapes, including mixtures of biological, geophysical, anthropogenic, and uncertain acoustic sources.

## Audio Data

Audio clips are stored under:

```text
audio_datasets/uploads/{SITE}/
```

For example:

```text
audio_datasets/uploads/DUVAL/
audio_datasets/uploads/MOURACHAN/
audio_datasets/uploads/RINYIRRU/
```

Each site folder contains the extracted audio segments used in the study.

The audio clips correspond to fixed-length segments from the original continuous recordings. In the experiment, segments are approximately:

```text
4.5 seconds
```

The `sound_path` field in the annotation files links each annotation row to its corresponding audio clip.

## Annotation Files

The file:

```text
annotations.zip
```

contains the annotation CSV files for the study sites.

Example annotation files include:

```text
DUVAL-DRYA-20210419T000000+1000_REC_annotations.csv
MOURACHAN-WETA-20210509T000000+1000_REC_annotations.csv
RINYIRRU-WETB-20210615T080000+1000_REC_annotations.csv
TARCUTTA-DRYA-20210430T100000+1000_REC_annotations.csv
UNDARA-DRYB-20210604T080000+1000_REC_annotations.csv
WAMBIANA-WETB-20210604T080000+1000_REC_annotations.csv
```

Each annotation file represents one site-level recording subset and contains the segment-level metadata and labels used in the analysis.

A typical annotation file contains columns such as:

```text
x
y
z
class
start_time
end_time
start_datetime
end_datetime
sound_path
sampled
background_silence
birds
frogs
human_speech
insects
mammals
misc/uncertain
rain_(heavy)
rain_(light)
vehicles_(aircraft/cars)
wind_(strong)
wind_(light)
propagated_class
```

## Column Descriptions

```text
| Column | Description |
|---|---|
| `x`, `y`, `z` | Low-dimensional embedding coordinates used for visualisation and clustering analysis. |
| `class` | Cluster assignment produced by the unsupervised segmentation workflow. |
| `start_time` | Segment start time relative to the source recording. |
| `end_time` | Segment end time relative to the source recording. |
| `start_datetime` | Absolute start datetime of the segment where available. |
| `end_datetime` | Absolute end datetime of the segment where available. |
| `sound_path` | Path to the corresponding audio clip. |
| `sampled` | Indicates whether the segment was part of the manually reviewed sample. |
| sound-type columns | Binary columns indicating manually assigned or propagated sound categories. |
| `propagated_class` | Final propagated sound-type label assigned to the segment. |
```
The sound-type columns include categories such as birds, frogs, insects, mammals, rain, wind, vehicles, human speech, background silence, and uncertain or mixed sounds.

## Manifest File

The file:

```text
manifest.csv
```

provides a consolidated index of the dataset. It is intended to help users map between site, annotation rows, audio files, and processed outputs.

The manifest should be used together with the annotation files when reconstructing the analysis workflow.

## Processed Features

The file:

```text
processed_features.zip
```

contains feature representations and intermediate processed files used by the segmentation pipeline.

These include extracted acoustic features, dimensionality reduction outputs, clustering-ready tables, and other intermediate data products used to generate the reported results.

## Results

The file:

```text
results.zip
```

contains the outputs of the experiments reported in the paper.

These include clustering outputs, evaluation summaries, visualisation data, and site-level result tables.

## Reproducibility

To use this dataset:

1. Download the complete Zenodo record.
2. Extract `annotations.zip`.
3. Ensure the audio clips remain under:

```text
audio_datasets/uploads/
```

4. Extract `processed_features.zip` and `results.zip` as needed.
5. Use the accompanying code repository to run the analysis notebooks or scripts.

The expected local structure after extraction is:

```text
data/
├── annotations/
├── audio_datasets/
│   └── uploads/
│       ├── DUVAL/
│       ├── MOURACHAN/
│       ├── RINYIRRU/
│       ├── TARCUTTA/
│       ├── UNDARA/
│       └── WAMBIANA/
├── processed_features/
└── results/
```

## Notes on Interpretation

This dataset is designed for exploratory ecoacoustic segmentation research.

The labels should be interpreted as soundscape-level acoustic categories rather than exhaustive fine-grained event boundaries. A segment may contain overlapping sources, and the propagated class represents the dominant or most relevant sound type assigned during the study workflow.

The dataset is intended to support:

- reproduction of the segmentation experiments
- inspection of cluster-level acoustic structure
- comparison of unsupervised soundscape segmentation outputs
- further analysis of heterogeneous ecoacoustic recordings

## License and Usage

Please follow the licensing and usage conditions specified on the Zenodo record and any applicable conditions associated with the source recordings.

## Contact

For questions about the dataset or reproducibility materials, please contact the corresponding author listed in the associated paper.
