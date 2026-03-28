# Compute cognitive efficiency index (performance / theta power)
df['Efficiency_Paper'] = df['perf_paper_corsi_span'] / df['theta_paper']
df['Efficiency_Adaptive'] = df['difficulty_mean_adaptive'] / df['theta_adaptive']

plt.figure(figsize=(8, 6))

eff_data = [
    df['Efficiency_Paper'],
    df['Efficiency_Adaptive']
]

eff_labels = [
    'No-screen',
    'Adaptive screen'
]

sns.barplot(data=eff_data, palette=['grey', 'orange'], capsize=0.1)
plt.xticks([0, 1], eff_labels, fontsize=12, fontweight='bold')

#plt.title("Cognitive efficiency index\n(Performance per unit of neural effort)", fontsize=14)
plt.ylabel("Efficiency index (Performance / Theta power)", fontsize=12)
plt.rcParams['pdf.fonttype'] = 42
plt.savefig("EN-cognitive_efficiency.pdf", bbox_inches='tight')
#plt.savefig("EN-cognitive_efficiency.png", dpi=300)
plt.show()
