# Efficient Unsupervised Segmentation of Heterogeneous Natural Soundscapes

This repository contains the code, data resources, and experimental workflow used in the paper:

**“An Efficient Pipeline for the Unsupervised Segmentation of Heterogeneous Natural Soundscapes”**

Passive Acoustic Monitoring (PAM) is rapidly generating large-scale ecoacoustic datasets, yet segmentation remains a key bottleneck due to overlapping biophony, geophony, and anthropophony. This repository provides an **unsupervised, data-driven framework** for organising complex soundscapes into acoustically coherent and ecologically interpretable units.

The pipeline integrates:
- Systematic data sampling  
- Sound Event Detection (SED)  
- MFCC feature extraction  
- Dimensionality reduction (PCA, t-SNE, UMAP)  
- Clustering (HDBSCAN, DBSCAN, k-means, hierarchical clustering)  
- Post-hoc validation using internal and ecological metrics  

---

## Repository Overview

```
.
├── data/
│   ├── annotations/          # Ground-truth / expert annotation files
│   ├── raw/                  # Downloaded A2O audio clips
│   ├── processed/            # Feature representations and intermediate outputs
│   ├── results/              # Experimental results and evaluation outputs
│   └── figures/              # Generated figures for analysis/paper
│
├── notebooks/
│   └── segmentation.ipynb    # Main experimental workflow
│
├── scripts/
│   └── download_A2O_data.py  # A2O audio downloader
│
├── src/                      # (Recommended modular structure)
│   ├── preprocessing.py
│   ├── feature_extraction.py
│   ├── dimensionality_reduction.py
│   ├── clustering.py
│   ├── evaluation.py
│   ├── visualisation.py
│   └── runtime_analysis.py
│
├── requirements.txt
└── README.md
```

---

## Data

Six ecoacoustic datasets are used:
Duval, Mourachan, Rinyirru, Tarcutta, Undara, Wambiana.

data/annotations/
├── DUVAL-DRYA-20210419T000000+1000_REC_annotations.csv
├── MOURACHAN-WETA-20210509T000000+1000_REC_annotations.csv
├── RINYIRRU-WETB-20210615T080000+1000_REC_annotations.csv
├── TARCUTTA-DRYA-20210430T100000+1000_REC_annotations.csv
├── UNDARA-DRYB-20210604T080000+1000_REC_annotations.csv
└── WAMBIANA-WETBB.csv

Annotations are included and follow:
Begin Time (s), End Time (s), Low Freq (Hz), High Freq (Hz), Label

---

## Downloading Audio (A2O)

Run:
```
python scripts/download_A2O_data.py
```

This downloads clips from the Australian Acoustic Observatory API.

---

## Requirements

Install:
```
pip install -r requirements.txt
```

---

## Workflow

1. Data preparation  
2. Feature extraction (MFCC)  
3. Dimensionality reduction  
4. Clustering  
5. Hyperparameter tuning  
6. Evaluation  
7. Visualisation  
8. Runtime analysis  

---

## Outputs

Results are stored in:
data/results/ and data/figures/

data/results/
├── clustering_results.csv
├── evaluation_metrics.csv
├── grid_search_results.csv
├── runtime_analysis.csv
└── site_level_summary.csv

data/figures/
├── cluster_plots/
├── voronoi_plots/
├── metric_radar/
└── runtime_curves/

---

## Citation

```
@article{Napier2026,
  author  = {Thomas James Napier et al.},
  title   = {An Efficient Pipeline for the Unsupervised Segmentation of Heterogeneous Natural Soundscapes},
  year    = {2026}
}
```
