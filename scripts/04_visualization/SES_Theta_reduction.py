import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data_study.csv", sep=";")

plt.figure(figsize=(10, 6))

sns.regplot(
    x='z_ses_score_composite',
    y='Diff_theta_Adapt_standard',
    data=df_ses,
    color='teal',
    line_kws={"color": "red"}
)

#plt.title("Impact of Adaptive Learning by Socioeconomic Status (Primary School)", fontsize=14)
plt.xlabel("Socioeconomic Status (Composite Z-score)", fontsize=12)
plt.ylabel("Cognitive Load Reduction (Adaptive - Standard)", fontsize=12)

plt.axhline(0, linestyle='--')
plt.rcParams['pdf.fonttype'] = 42
plt.savefig("EN-impact_adaptive_learning_ses.pdf", bbox_inches='tight')
#plt.savefig("EN-impact_adaptive_learning_ses.png", dpi=300)
plt.show()
