import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================
# PROJET DVF - NANTES 2025
# ETAPE 4 : VISUALISATIONS
# =====================================

df = pd.read_csv("DVF_Nantes_2025_propre.csv", low_memory=False)
os.makedirs("graphiques", exist_ok=True)
sns.set_theme(style="whitegrid")

# Graphique 1 : distribution des prix au m²
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x="prix_m2", bins=50, color="steelblue")
mediane = df["prix_m2"].median()
plt.axvline(mediane, color="red", linestyle="--",
            label=f"Médiane : {mediane:,.0f} €/m²".replace(",", " "))
plt.title("Distribution des prix au m² à Nantes (janvier-septembre 2025)")
plt.xlabel("Prix au m² (€)")
plt.ylabel("Nombre de ventes")
plt.legend()
plt.tight_layout()
plt.savefig("graphiques/01_distribution_prix_m2.png", dpi=150)
plt.close()

# Graphique 2 : appartements vs maisons
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="type_local", y="prix_m2",
            hue="type_local", palette="Set2", legend=False)
plt.title("Prix au m² : appartements vs maisons (Nantes, janv.-sept. 2025)")
plt.xlabel("")
plt.ylabel("Prix au m² (€)")
plt.tight_layout()
plt.savefig("graphiques/02_boxplot_maison_appartement.png", dpi=150)
plt.close()

print("Graphiques enregistrés dans le dossier graphiques/")
# Graphique 3 : évolution mensuelle du prix médian au m²
df["date_mutation"] = pd.to_datetime(df["date_mutation"])
df["mois"] = df["date_mutation"].dt.to_period("M").dt.to_timestamp()

median_global = df.groupby("mois")["prix_m2"].median()
median_appart = df[df["type_local"] == "Appartement"].groupby("mois")["prix_m2"].median()

plt.figure(figsize=(10, 6))
plt.plot(median_global.index, median_global.values, marker="o", label="Tous biens")
plt.plot(median_appart.index, median_appart.values, marker="o", label="Appartements seuls")
plt.axvspan(pd.Timestamp("2025-08-16"), pd.Timestamp("2025-09-15"),
            color="grey", alpha=0.15, label="Septembre incomplet")
plt.ylim(2500, 4500)
plt.title("Évolution du prix médian au m² à Nantes (janvier-septembre 2025)")
plt.xlabel("Mois")
plt.ylabel("Prix médian au m² (€)")
plt.legend()
plt.tight_layout()
plt.savefig("graphiques/03_evolution_mensuelle.png", dpi=150)
plt.close()
print("Graphique 3 enregistré")