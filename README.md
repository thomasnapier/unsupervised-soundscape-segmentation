# Efficient Unsupervised Segmentation of Heterogeneous Natural Soundscapes

This repository supports the paper:

**“An Efficient Pipeline for the Unsupervised Segmentation of Heterogeneous Natural Soundscapes”**

It provides the data snapshots, result files, figures, and reconstruction notebooks used to inspect and reproduce the analysis. The study uses an unsupervised ecoacoustic workflow to organise heterogeneous soundscapes into acoustically coherent and ecologically interpretable units.

The manuscript workflow is:

1. systematic sampling of long-duration recordings;
2. sound event detection and segmentation into 4.5-second non-overlapping windows;
3. MFCC-based feature extraction;
4. dimensionality reduction using PCA, t-SNE, and UMAP;
5. clustering using k-means, DBSCAN, HDBSCAN, and hierarchical clustering;
6. internal validation using Silhouette, Calinski-Harabasz, Davies-Bouldin, Dunn, and Composite Score;
7. post-hoc ecological validation using partially labelled annotation files.

<p align="center"><img width="80%" src="./data/figures/overall.png"></p>

---

## Table of contents

- [Quick start guide](#quick-start-guide)
- [Full reconstruction workflow](#full-reconstruction-workflow)
- [Repository structure](#repository-structure)
- [Data and annotation files](#data-and-annotation-files)
- [Installation](#installation)
- [Outputs and figures](#outputs-and-figures)
- [Validation logic](#validation-logic)
- [Reproducibility notes](#reproducibility-notes)
- [Data availability](#data-availability)
- [Citation](#citation)
- [Related software](#related-software)

---

## Quick start guide

For most users, the easiest and quickest way to inspect the analysis is to use the **existing-data figures and tables notebook**.

Use this notebook when you want to:

- view the manuscript-style tables and figures;
- inspect the supplied result files;
- avoid rerunning the full clustering grid search;
- avoid creating new output folders;
- avoid overwriting repository files.

Recommended notebook:

```text
quick_reconstruction_notebook.ipynb
```

This notebook reads the existing repository data only and displays outputs inline in Jupyter. It does **not** save CSV files, PNG files, LaTeX files, or audit folders.

It reconstructs or displays:

- internal metric tables from the supplied Round 2 CSV files;
- Figure 2-style boxplots for Silhouette, Calinski-Harabasz, Davies-Bouldin, Dunn, and Composite Score;
- Figure 4-style UMAP spider/radar plots;
- Table 2-style post-hoc external validation values;
- Table 3-style best internal result values;
- Figure 5-style Voronoi/site plots from the existing figure files or annotation coordinates, depending on availability.

### Non-technical steps

1. Download this repository from GitHub as a ZIP file.
2. Extract the ZIP file somewhere easy to find.
3. Install Python 3.10, 3.11, or 3.12.
4. Open a terminal or command prompt in the repository folder.
5. Install the requirements:

```bash
pip install -r requirements.txt
```

6. Start Jupyter:

```bash
jupyter lab
```

7. Open the print-only notebook:

```text
quick_reconstruction_notebook.ipynb
```

8. Select:

```text
Run > Run All Cells
```

The figures and tables will appear inside the notebook.

---

## Full reconstruction workflow

The full reconstruction notebook is intended for users who want to regenerate intermediate artefacts, not just inspect the supplied results.

Use the full reconstruction notebook when you want to:

- derive or regenerate feature files where audio paths are available;
- rerun dimensionality reduction;
- rerun clustering and internal validation;
- checkpoint long-running clustering jobs;
- compare regenerated outputs against the supplied repository snapshot.

Main full reconstruction notebook:

```text
full_reconstruction_notebook.ipynb
```

The full reconstruction workflow writes new outputs to a timestamped folder such as:

```text
reconstruction_runs/reconstruction_YYYYMMDD_HHMMSS/
```

It should not overwrite original repository files.

A typical reconstruction folder contains:

```text
reconstruction_runs/reconstruction_YYYYMMDD_HHMMSS/
├── source_original/
├── originals_for_comparison/
├── reconstructed/
│   ├── audio_index/
│   ├── processed_features/
│   ├── processed_features_normalized/
│   ├── embeddings/
│   ├── grid_search_raw/
│   │   └── checkpoints_by_embedding_method/
│   ├── results_round2/
│   ├── internal_analysis/
│   ├── external_validation/
│   └── figures/
└── audit/
```

### Resuming after a kernel crash

The clustering stage can be computationally expensive. If the notebook stops or the Jupyter kernel dies:

1. keep the latest `reconstruction_runs/reconstruction_.../` folder;
2. reopen the full reconstruction notebook;
3. set `RESUME_RUN_DIR` near the top of the notebook to that folder;
4. rerun the notebook.

Completed feature files, embeddings, and clustering checkpoints will be reused.

For lower-memory systems, reduce the number of clustering jobs per run:

```python
MAX_CLUSTER_JOBS_PER_RUN = 10
```

Then rerun the notebook repeatedly until all checkpoints are complete.

---

## Repository structure

The repository snapshot is organised approximately as follows:

```text
.
├── data/
│   ├── annotations/
│   │   ├── DUVAL-DRYA-20210419T000000+1000_REC_annotations.csv
│   │   ├── MOURACHAN-WETA-20210509T000000+1000_REC_annotations.csv
│   │   ├── RINYIRRU-WETB-20210615T080000+1000_REC_annotations.csv
│   │   ├── TARCUTTA-DRYA-20210430T100000+1000_REC_annotations.csv
│   │   ├── UNDARA-DRYB-20210604T080000+1000_REC_annotations.csv
│   │   └── WAMBIANA-WETB-20210625T080000+1000_REC_annotations.csv
│   │
│   ├── processed_features/
│   │   ├── 39-features-Duval-DryA-20min-full-day.csv
│   │   ├── 39-features-Mourachan-WetA-20min-full-day.csv
│   │   ├── 39-features-Rinyirru-WetB-20min-full-day.csv
│   │   ├── 39-features-Undara-DryB-20min-full-day.csv
│   │   └── 39-features-Wambiana-WetA-20min-full-day.csv
│   │
│   ├── results/
│   │   ├── DBSCAN_results_round2PCA.csv
│   │   ├── DBSCAN_results_round2UMAP.csv
│   │   ├── DBSCAN_results_tsne_Round2.csv
│   │   ├── HCA_results_round2PCA.csv
│   │   ├── HCA_results_tsne.csv
│   │   ├── HCA_results_umap.csv
│   │   ├── HDBSCAN_results_round2PCA.csv
│   │   ├── HDBSCAN_results_round2UMAP.csv
│   │   ├── HDBSCAN_results_tsne_Round2.csv
│   │   ├── KMeans_results_round2PCA.csv
│   │   ├── KMeans_results_tsne.csv
│   │   └── KMeans_results_umap.csv
│   │
│   ├── figures/
│   │   ├── overall.png
│   │   ├── SC.png
│   │   ├── CH.png
│   │   ├── DB.png
│   │   ├── DI.png
│   │   ├── CS.png
│   │   ├── spider-plots.png
│   │   ├── scalability.png
│   │   ├── Duval.png
│   │   ├── Mourachan.png
│   │   ├── Rinyirru.png
│   │   ├── Tarcutta.png
│   │   ├── Undara.png
│   │   └── Wambiana.png
│   │
│   └── zenodo_manifest/
│       ├── generate_zenodo_manifest.py
│       ├── manifest.csv
│       └── Zenodo_README.md
│
├── quick_reconstruction_notebook.ipynb
├── full_reconstruction_notebook.ipynb
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Data and annotation files
[![DOI](https://img.shields.io/badge/DOI-10.55281%2Fzenodo.19757414-blue)](https://doi.org/10.5281/zenodo.19757414)

The complete dataset used in this study is available at the link above. It includes audio segments, annotations, processed features, and experimental results required to reproduce all analyses.

Six ecoacoustic datasets are used:
Duval, Mourachan, Rinyirru, Tarcutta, Undara, Wambiana.
```
data/annotations/
├── DUVAL-DRYA-20210419T000000+1000_REC_annotations.csv
├── MOURACHAN-WETA-20210509T000000+1000_REC_annotations.csv
├── RINYIRRU-WETB-20210615T080000+1000_REC_annotations.csv
├── TARCUTTA-DRYA-20210430T100000+1000_REC_annotations.csv
├── UNDARA-DRYB-20210604T080000+1000_REC_annotations.csv
└── WAMBIANA-WETB-20210604T080000+1000_REC_annotations.csv
```
Annotations are included and follow:
x, y, z, class, start_time, end_time, start_date, end_date, sound_path, sampled, background, birds, frogs, human_speech, insects, mammals, misc/uncertain, rain(heavy), rain(light), vehicles (aircraft/cars), wind (strong), wind (light), propagated class

Annotations were generated by the LEAVES tool: https://github.com/thomasnapier/LEAVES

The repository does **not** bundle the complete original Australian Acoustic Observatory audio archive. If annotation files contain `sound_path` values that are valid on your machine, the full reconstruction notebook can use them. If not, it logs missing files and continues using the included processed feature and result snapshots where appropriate.

---

## Installation

A Python environment from **Python 3.10 to 3.12** is recommended. Some scientific audio and machine learning packages may not install reliably on very new Python versions.

Install dependencies with:

```bash
pip install -r requirements.txt
```

For Jupyter:

```bash
pip install jupyterlab ipykernel
python -m ipykernel install --user --name soundscape-reconstruction
```

---

## Outputs and figures

The repository contains the manuscript figures and supporting plots in:

```text
data/figures/
```

Key figures include:

```text
overall.png          pipeline overview
SC.png               Silhouette boxplot
CH.png               Calinski-Harabasz boxplot
DB.png               Davies-Bouldin boxplot
DI.png               Dunn boxplot
CS.png               Composite Score boxplot
spider-plots.png     UMAP method/site radar plots
scalability.png      runtime/scalability plot
Duval.png            Voronoi/site plot
Mourachan.png
Rinyirru.png
Tarcutta.png
Undara.png
Wambiana.png
```

The existing-data notebook displays figures and tables inline. The full reconstruction notebook writes regenerated outputs to a new timestamped reconstruction folder.

---

## Validation logic

### Internal validation

Internal validation is label-free. It evaluates cluster structure using:

- Silhouette Coefficient;
- Calinski-Harabasz Index;
- Davies-Bouldin Index;
- Dunn Index;
- Composite Score.

These metrics are used to compare clustering algorithms and dimensionality reduction methods across normalised scores.

### Post-hoc external validation

External validation is post-hoc. Labels are **not** used to train embeddings, select clustering hyperparameters, or fit clustering models.

The external validation stage uses:

- the unsupervised cluster label column, usually `class`;
- the propagated ecological class label, usually `propagated_class`;
- manually sampled rows, usually `sampled == True`, for MACPC and sound-type summaries where applicable.

For Wambiana and Tarcutta, local reconstruction may require explicit fallback/reference handling if corresponding source annotation or feature files are incomplete or absent.

---

## Reproducibility notes

- The easiest reproducibility path is the existing-data print-only notebook.
- The full reconstruction path is slower and may require multiple resumed runs.
- The repository contains processed feature and result snapshots, but not the full original A2O raw audio archive.
- Annotation `sound_path` values may refer to paths from the original machine or prior data layout.
- t-SNE, UMAP, and clustering can vary unless package versions, random seeds, and backends match the original environment.
- HDBSCAN results may differ between `sklearn.cluster.HDBSCAN` and the external `hdbscan` package.
- Reconstructed outputs should be written to timestamped reconstruction directories, not over the repository originals.

---

## Data availability

The code and processed feature data are associated with the manuscript repository:

```text
https://github.com/thomasnapier/unsupervised-soundscape-segmentation
```

The original raw audio recordings are publicly available from the Australian Acoustic Observatory:

```text
https://data.acousticobservatory.org/
```

Dataset snapshot:

```text
https://doi.org/10.5281/zenodo.19757414
```

---

## Citation

```bibtex
@article{Napier2026UnsupervisedSegmentation,
  author  = {Napier, Thomas James and others},
  title   = {An Efficient Pipeline for the Unsupervised Segmentation of Heterogeneous Natural Soundscapes},
  year    = {2026},
  note    = {Manuscript under review / preprint details to be updated}
}
```

---

## Related software

Annotations and cluster-based labelling are associated with LEAVES:

```text
https://github.com/thomasnapier/LEAVES
```

LEAVES is an open-source web-based tool for scalable annotation and visualisation of ecoacoustic datasets using cluster analysis.
