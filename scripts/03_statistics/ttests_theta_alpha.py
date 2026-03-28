import pandas as pd
from scipy import stats

df = pd.read_csv("data/processed/eeg_clean.csv")

# Theta

t1, p1 = stats.ttest_rel(df['Log_theta_paper'], df['Log_theta_standard'])
t2, p2 = stats.ttest_rel(df['Log_theta_standard'], df['Log_theta_adaptive'])
t3, p3 = stats.ttest_rel(df['Log_theta_paper'], df['Log_theta_adaptive'])

print("Theta results")
print(p1, p2, p3)

# Alpha

t1_a, p1_a = stats.ttest_rel(df['Log_alpha_paper'], df['Log_alpha_standard'])
t2_a, p2_a = stats.ttest_rel(df['Log_alpha_standard'], df['Log_alpha_adaptive'])
t3_a, p3_a = stats.ttest_rel(df['Log_alpha_paper'], df['Log_alpha_adaptive'])

print("Alpha results")
print(p1_a, p2_a, p3_a)
