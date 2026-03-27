import pandas as pd
import numpy as np

df_eeg = pd.read_csv("data/processed/eeg_results_primary.csv")

df_clean = df_eeg.copy()
df_clean = df_clean.dropna()

df_36 = df_clean.copy()

eeg_columns = [
'theta_paper','alpha_paper',
'theta_standard','alpha_standard',
'theta_adaptive','alpha_adaptive'
]

# Winsorization

for col in eeg_columns:
upper_limit = df_36[col].quantile(0.95)
df_36[col] = df_36[col].clip(upper=upper_limit)

# Log transform

for col in eeg_columns:
df_36[f'Log_{col}'] = 10 * np.log10(df_36[col])

df_36.to_csv("data/processed/eeg_clean.csv", index=False)
