import pandas as pd

# =====================================
# PROJET DVF - NANTES 2025
# ETAPE 2 : NETTOYAGE DES DONNEES (v2)
# =====================================

print("Chargement des données...")
df = pd.read_csv("DVF_Nantes_2025.csv", sep=",", low_memory=False)
print("Nombre de lignes initial :", len(df))

# 0. Harmoniser le nom de la colonne prix
df = df.rename(columns={"valeurfonciere": "valeur_fonciere"})

# 1. Supprimer les doublons stricts
df = df.drop_duplicates()
print("Après doublons :", len(df))

# 2. Convertir en nombres
for col in ["valeur_fonciere", "surface_reelle_bati"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 3. Garder uniquement les vraies ventes
df = df[df["nature_mutation"].isin(
    ["Vente", "Vente en l'état futur d'achèvement"]
)].copy()
print("Après filtre ventes :", len(df))

# 4. Garder les prix et surfaces valides
df = df[(df["valeur_fonciere"] > 0) & (df["surface_reelle_bati"] > 0)].copy()
print("Après prix/surface valides :", len(df))

# 5. Garder les maisons et appartements
df = df[df["type_local"].isin(["Maison", "Appartement"])].copy()
print("Après maisons/appartements :", len(df))

# 6. Retirer les ventes de plusieurs logements
nb_lignes = df.groupby("id_mutation")["id_mutation"].transform("count")
df = df[nb_lignes == 1].copy()
print("Après ventes d'un seul logement :", len(df))

# 7. Calculer le prix au m²
df["prix_m2"] = df["valeur_fonciere"] / df["surface_reelle_bati"]

# 8. Retirer les prix au m² aberrants (bornes provisoires)
print("1 % des ventes sous :", round(df["prix_m2"].quantile(0.01)), "€/m²")
print("1 % des ventes au-dessus de :", round(df["prix_m2"].quantile(0.99)), "€/m²")
df = df[df["prix_m2"].between(1000, 15000)].copy()
print("Après filtre prix au m² :", len(df))

# 9. Enregistrer
df.to_csv("DVF_Nantes_2025_propre.csv", index=False, encoding="utf-8-sig")
print("Nettoyage terminé !")
print("Lignes :", len(df), "| ventes distinctes :", df["id_mutation"].nunique())
print("Fichier enregistré : DVF_Nantes_2025_propre.csv (racine du projet)")