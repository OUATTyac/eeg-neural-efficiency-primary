import pandas as pd

print("SOCIODEMOGRAPHIC CHARACTERISTICS (N=36)")

# Age statistics
age_stats = df['age'].describe()
print("\nAge:")
print(f"  - Mean: {age_stats['mean']:.2f} years")
print(f"  - SD: {age_stats['std']:.2f}")
print(f"  - Range: {age_stats['min']:.0f} to {age_stats['max']:.0f} years")

# Sex distribution
sex_counts = df['gender'].value_counts()
sex_percent = df['gender'].value_counts(normalize=True) * 100
print("\nSex distribution:")
for label in sex_counts.index:
    print(f"  - {label}: {sex_counts[label]} ({sex_percent[label]:.1f}%)")

# School grade
grade_counts = df['grade'].value_counts()
print("\nSchool grade:")
for label in grade_counts.index:
    print(f"  - {label}: {grade_counts[label]} participants")

# Counterbalancing (condition order)
order_counts = df['conditions_order'].value_counts()
print("\nCounterbalancing (condition order):")
for label in order_counts.index:
    print(f"  - Order {label}: {order_counts[label]} participants")
