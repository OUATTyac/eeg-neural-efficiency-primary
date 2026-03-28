import seaborn as sns
import matplotlib.pyplot as plt

# Theta

# Prepare data for plotting
df_plot_36 = pd.melt(
    df_36,
    id_vars=['subject_id'],
    value_vars=['Log_theta_paper', 'Log_theta_standard', 'Log_theta_adaptive'],
    var_name='Condition',
    value_name='Theta Power (dB)'
)

df_plot_36['Condition'] = df_plot_36['Condition'].replace({
    'Log_theta_paper': 'No-screen',
    'Log_theta_standard': 'Standard screen',
    'Log_theta_adaptive': 'Adaptive screen'
})
plt.figure(figsize=(10, 6))

sns.boxplot(
    x='Condition',
    y='Theta Power (dB)',
    data=df_plot_36,
    palette="Set2",
    width=0.4
)

sns.swarmplot(
    x='Condition',
    y='Theta Power (dB)',
    data=df_plot_36,
    color=".2",
    alpha=0.5
)

# Significance annotation
x1, x2 = 0, 2
y = df_plot_36['Theta Power (dB)'].max() + 0.2
h = 0.1

plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5)
plt.text((x1 + x2) / 2, y + h, f"p = {p_val:.4f}", ha='center', va='bottom', fontsize=12)

#plt.title(f"Theta cognitive load across conditions (N={len(df_36)})", fontsize=14)
plt.ylabel("Theta Power (dB)")
plt.xlabel("Condition")
plt.rcParams['pdf.fonttype'] = 42
plt.tight_layout()
plt.savefig("EN-theta_three_conditions.pdf", bbox_inches='tight')
#plt.savefig("EN-theta_three_conditions.png", dpi=300)
plt.show()

#alpha

# Prepare data for plotting
df_plot_36 = pd.melt(
    df_36,
    id_vars=['subject_id'],
    value_vars=['Log_alpha_paper', 'Log_alpha_standard', 'Log_alpha_adaptive'],
    var_name='Condition',
    value_name='Alpha Power (dB)'
)

df_plot_36['Condition'] = df_plot_36['Condition'].replace({
    'Log_alpha_paper': 'No-screen',
    'Log_alpha_standard': 'Standard screen',
    'Log_alpha_adaptive': 'Adaptive screen'
})

# Visualization
plt.figure(figsize=(10, 6))

sns.boxplot(
    x='Condition',
    y='Alpha Power (dB)',
    data=df_plot_36,
    palette="Set2",
    width=0.4
)

sns.swarmplot(
    x='Condition',
    y='Alpha Power (dB)',
    data=df_plot_36,
    color=".2",
    alpha=0.5
)

# Significance annotations
y = df_plot_36['Alpha Power (dB)'].max() + 0.2
h = 0.1

x1, x2 = 0, 2
plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5)
plt.text((x1 + x2) / 2, y + h, "p = 0.0001", ha='center', va='bottom', fontsize=12)

y2 = y + 0.5
x1b, x2b = 1, 2
plt.plot([x1b, x1b, x2b, x2b], [y2, y2+h, y2+h, y2], lw=1.5)
plt.text((x2b + x2b) / 2, y2 + h, "p = 0.0096", ha='center', va='bottom', fontsize=12)

#plt.title(f"Alpha attentional engagement across conditions (N={len(df_36)})", fontsize=14)
plt.ylabel("Alpha Power (dB)")
plt.xlabel("Condition")
plt.rcParams['pdf.fonttype'] = 42
plt.tight_layout()
plt.savefig("EN-alpha_three_conditions.pdf", bbox_inches='tight')
#plt.savefig("EN-alpha_three_conditions_significant.png", dpi=300)
plt.show()
