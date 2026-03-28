#Étape 1 : charger + transformer
import pandas as pd

df = pd.read_csv(data_study.csv", sep=';')

# passer en format long
df_long = pd.melt(df,
                  id_vars=['subject_id', 'conditions_order'],
                  value_vars=['theta_paper', 'theta_standard', 'theta_adaptive'],
                  var_name='condition',
                  value_name='theta')

# nettoyer noms conditions
df_long['condition'] = df_long['condition'].str.replace('Theta_', '')

#Étape 2 : modèle mixte
import statsmodels.formula.api as smf

model = smf.mixedlm("theta ~ condition * conditions_order",
                    df_long,
                    groups=df_long["subject_id"])

result = model.fit()
print(result.summary())
