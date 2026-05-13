# Efficient Unsupervised Segmentation of Heterogeneous Natural Soundscapes

This repository contains the code, data resources, and experimental workflow used in the paper:

**“An Efficient Pipeline for the Unsupervised Segmentation of Heterogeneous Natural Soundscapes”**

Passive Acoustic Monitoring (PAM) is rapidly generating large-scale ecoacoustic datasets, yet segmentation remains a key bottleneck due to overlapping biophony, geophony, and anthropophony. This repository provides an **unsupervised, data-driven framework** for organising complex soundscapes into acoustically coherent and ecologically interpretable units.

The manuscript pipeline consists of:

1. systematic sampling of long-duration recordings;
2. sound event detection and segmentation into 4.5-second non-overlapping windows;
3. MFCC-based feature extraction;
4. dimensionality reduction using PCA, t-SNE, and UMAP;
5. clustering using k-means, DBSCAN, HDBSCAN, and hierarchical clustering;
6. internal validation using Silhouette, Calinski-Harabasz, Davies-Bouldin, Dunn, and Composite Score;
7. post-hoc ecological validation using partially labelled annotation files.

<p align="center"><img width=80% src="./data/figures/overall.png"></p>

---

---

## Repository status

This repository is a **reconstruction and reproducibility snapshot**. It contains the annotation files, processed 39-feature files, clustering result CSVs, manuscript figures, and notebooks used to reconstruct or audit the analysis outputs.

It is important to distinguish between three types of files:

1. **Source annotation files**: LEAVES-style annotation CSVs containing cluster labels, propagated labels, manual sampled labels, coordinates, and `sound_path` references.
2. **Processed feature/result files**: 39-feature CSVs and clustering result files used for internal metric figures and tables.
3. **Reconstruction outputs**: regenerated outputs written to a timestamped reconstruction directory. These should not overwrite the original repository files.

The repository does **not** bundle the complete original A2O raw audio archive. Where audio paths are available through the annotation files, the reconstruction notebooks can use those paths. Where local audio is unavailable, the workflow can still audit and reconstruct downstream artefacts from the included feature and result snapshots.

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
├── full_reconstruction_notebook.ipynb
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Data Annotation Files

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

---

## Installation

A Python environment from **Python 3.10 to 3.12** is recommended. Some scientific audio packages may not yet install reliably on newer Python versions.

Install dependencies with:

```bash
pip install -r requirements.txt
```

If using Jupyter:

```bash
pip install jupyterlab ipykernel
python -m ipykernel install --user --name soundscape-reconstruction
```

---

## Main reconstruction notebook

The most complete reconstruction notebook is:

```text
full_annotation_source_snapshot_reconstruction_notebook_checkpointed_v4_exact_recompute_no_substitution.ipynb
```

This notebook is designed to:

1. create a timestamped reconstruction directory;
2. copy the original repository snapshot into that directory for audit purposes;
3. derive audio paths from annotation files where available;
4. regenerate 39-feature files when local audio paths are valid;
5. reuse processed feature snapshots only when audio reconstruction is not possible;
6. run dimensionality reduction and clustering grid search;
7. checkpoint clustering outputs so the kernel can be restarted without losing progress;
8. regenerate Round 2-style internal results;
9. regenerate boxplots, spider plots, and Voronoi plots;
10. regenerate post-hoc GT/external validation tables;
11. compare recomputed outputs against the original Round 2 and manuscript reference values;
12. write all new outputs to the reconstruction directory without overwriting the original repository files.

The notebook does **not** substitute original output files as final results. Original files are used only for snapshotting and mismatch auditing. Reconstructed outputs are generated separately.

---

## Running the reconstruction workflow

Open the reconstruction notebook and run from the top.

By default, outputs are written to a timestamped folder such as:

```text
reconstruction_runs/reconstruction_YYYYMMDD_HHMMSS/
```

A typical reconstructed output tree is:

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

To resume a failed or interrupted run, set `RESUME_RUN_DIR` near the top of the notebook to the existing reconstruction directory, then rerun. Completed feature files, embeddings, and clustering checkpoints are reused.

---

## Checkpointing and kernel stability

The clustering stage can be computationally expensive. The reconstruction notebook saves intermediate outputs so a failed kernel does not require a complete rerun.

Checkpointed stages include:

- source snapshot creation;
- annotation-derived audio index;
- feature generation;
- normalised feature generation;
- dimensionality reduction embeddings;
- per-dataset/per-embedding/per-method clustering checkpoints;
- Round 2-style result files;
- final audit tables and figures.

For lower-memory systems, reduce the number of clustering jobs per run in the notebook, for example:

```python
MAX_CLUSTER_JOBS_PER_RUN = 10
```

Then rerun the notebook repeatedly. It will continue from the next missing checkpoint.

---

## HDBSCAN backend

The reconstruction notebook supports `sklearn.cluster.HDBSCAN` by default, matching the current project preference.

However, older Round 2 outputs may have been produced with the external `hdbscan` package. Exact numerical reproduction can differ between HDBSCAN implementations. If strict historical matching is required and the external package is available, the notebook can be configured to use the external backend.

---

## Validation logic

### Internal validation

Internal validation is label-free. It evaluates the structure of the clusters using:

- Silhouette Coefficient;
- Calinski-Harabasz Index;
- Davies-Bouldin Index;
- Dunn Index;
- Composite Score.

The internal figures compare clustering algorithms and dimensionality reduction methods across normalised versions of these metrics.

### Post-hoc external validation

External validation is post-hoc. Labels are **not** used to train embeddings, select clustering hyperparameters, or fit clustering models.

The GT/external validation stage uses:

- the existing unsupervised cluster label column, usually `class`;
- the propagated ecological class label, usually `propagated_class`;
- manually sampled rows, usually `sampled == True`, for MACPC and sound-type summaries where applicable.

For Wambiana and Tarcutta, where source annotation or feature coverage may be incomplete in the reconstruction snapshot, the notebook preserves explicit fallback/reference handling rather than silently producing misleading values.

---

## Figures

The repository contains the main manuscript figures and supporting plots:

```text
data/figures/
├── overall.png          # pipeline overview
├── SC.png               # Silhouette boxplot
├── CH.png               # Calinski-Harabasz boxplot
├── DB.png               # Davies-Bouldin boxplot
├── DI.png               # Dunn boxplot
├── CS.png               # Composite Score boxplot
├── spider-plots.png     # UMAP method/site radar plots
├── scalability.png      # runtime/scalability plot
├── Duval.png            # Voronoi/site plot
├── Mourachan.png
├── Rinyirru.png
├── Tarcutta.png
├── Undara.png
└── Wambiana.png
```

The reconstruction notebook regenerates corresponding figures inside the reconstruction run directory rather than overwriting these originals.

---

## Known reproducibility notes

- The repository snapshot contains processed features and result CSVs, but does not bundle the full raw A2O audio archive.
- Annotation files may contain `sound_path` values that point to files on the original machine or a previous data layout. The reconstruction notebook logs missing files and continues rather than stopping the entire run.
- Stochastic components such as t-SNE, UMAP, and clustering can vary unless random seeds, package versions, and backends match the original environment.
- HDBSCAN results may differ between `sklearn.cluster.HDBSCAN` and the external `hdbscan` package.
- Reconstructed outputs are written to a new timestamped directory. Original repository files should not be overwritten.
- Some manuscript values, especially GT/external values for Wambiana and Tarcutta, may require explicit reference/fallback handling when the corresponding source files are incomplete or absent in the local snapshot.

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

A Zenodo/Dryad-style dataset snapshot may be used alongside this repository when distributing processed features, annotations, figures, and reconstruction manifests. Update the DOI below if the archival record changes:

```text
https://doi.org/10.5281/zenodo.19757414
```

---

## Citation

If citing the manuscript, update this entry with the final publication details:

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
