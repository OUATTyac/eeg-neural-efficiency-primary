import pandas as pd
import scipy.stats as stats
import pingouin as pg

df = pd.read_csv("data_study.csv", sep=";")

numeric_cols = df.columns[6:]
for col in numeric_cols:
df[col] = pd.to_numeric(df[col], errors='coerce')

# Theta ANOVA

df_theta = df.melt(
id_vars='subject_id',
value_vars=['Log_theta_paper','Log_theta_standard','Log_theta_adaptive'],
var_name='Condition',
value_name='Theta'
)

anova_theta = pg.rm_anova(data=df_theta, dv='Theta', within='Condition', subject='subject_id')
print(anova_theta)

# SES correlation

df_ses = df.dropna(subset=['z_ses_score_composite'])

rho, p = stats.spearmanr(
df_ses['z_ses_score_composite'],
df_ses['Diff_Theta_Adapt_Standard']
)

print("SES correlation:", rho, p)
