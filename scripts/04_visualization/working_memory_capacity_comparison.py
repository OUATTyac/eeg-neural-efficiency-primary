import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("data_study.csv", sep=";")

plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")

data = [
    df['perf_paper_corsi_span'],
    df['difficulty_mean_adaptive']
]

labels = [
    'No-screen\n(Max span)',
    'Adaptive screen\n(Mean level)'
]

ax = sns.barplot(data=data, palette=['mediumseagreen', 'cornflowerblue'], capsize=0.1)
ax.set_xticklabels(labels, fontsize=12, fontweight='bold')

#plt.title("Comparison of working memory capacity across learning conditions", fontsize=14, pad=20)
plt.ylabel("Sequence length (number of blocks)", fontsize=12)
plt.ylim(0, 5)

x1, x2 = 0, 1
y, h = 4.3, 0.1
plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5)
plt.text((x1 + x2) * 0.5, y + h, "p = 0.0319 *", ha='center', va='bottom', fontweight='bold')
plt.rcParams['pdf.fonttype'] = 42
plt.savefig("EN-working_memory_capacity.pdf", bbox_inches='tight')
#plt.savefig("EN-working_memory_capacity_comparison.png", dpi=300)
plt.show()
