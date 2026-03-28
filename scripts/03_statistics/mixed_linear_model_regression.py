#Étape 1 : charger + transformer
import pandas as pd

df = pd.read_csv(r"C:\Users\ouatt\Downloads\donnees_global_primaire.csv", sep=';')

# passer en format long
df_long = pd.melt(df,
                  id_vars=['ID_participant', 'ordre_conditions'],
                  value_vars=['Theta_papier', 'Theta_Standard', 'Theta_Adaptatif'],
                  var_name='condition',
                  value_name='theta')

# nettoyer noms conditions
df_long['condition'] = df_long['condition'].str.replace('Theta_', '')

#Étape 2 : modèle mixte
import statsmodels.formula.api as smf

model = smf.mixedlm("theta ~ condition * ordre_conditions",
                    df_long,
                    groups=df_long["ID_participant"])

result = model.fit()
print(result.summary())
