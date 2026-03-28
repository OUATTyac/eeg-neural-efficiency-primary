1. Description
This repository contains the analysis pipeline for the study:

"Neural efficiency of visuospatial working memory across learning modalities in primary school children"

The project investigates EEG markers of cognitive load (theta) and attentional engagement (alpha) across three learning conditions:

No-screen (paper)
Standard digital
Adaptive digital

2. Pipeline

1. XDF → PSD → band power extraction
2. Cleaning (NA removal, winsorization, log transform)
3. Statistical analyses (mixed_linear_model_regression, t-tests, RM-ANOVA)
4. SES and behavioral correlations
5. Visualization (boxplots, topomaps)
-----------------------------------------------------------------------------------------------------------------
1. EEG preprocessing
XDF loading (pyxdf)
Conversion to MNE format
Band-pass filtering (1–40 Hz)
Average referencing
Power spectral density (Welch)

2. Feature extraction
Theta (4–8 Hz)
Alpha (8–12 Hz)
ROI-based averaging

3. Data cleaning
Removal of missing data
Winsorization (95th percentile)
Log transformation (dB)

4. Statistical analysis
mixed linear model regression
Paired t-tests
Repeated-measures ANOVA
Bonferroni post hoc tests

5. Additional analyses
SES correlations (Spearman)
Performance correlations (Pearson)

6. Visualization
Boxplots + swarmplots
EEG topographies (MNE)
Regression plots
-------------------------------------------------------------------------------------------------------------------------
3. Reproducibility

python scripts/01_preprocessing/extract_band_power.py
python scripts/02_cleaning/cleaning_winsor_log.py
python scripts/03_statistics/ttests_theta_alpha.py
python scripts/03_statistics/anova_and_correlations.py
python scripts/03_statistics/mixed_linear_model_regression.py

4. Dependencies

See requirements.txt


