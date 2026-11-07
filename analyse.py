import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
# =====================================
# PROJET DVF - NANTES 2025
# ETAPE 3 : ANALYSE EXPLORATOIRE
# =====================================

df = pd.read_csv("DVF_Nantes_2025_propre.csv", low_memory=False)
df["date_mutation"] = pd.to_datetime(df["date_mutation"])

print("=== ANALYSE 1 : STATISTIQUES GÉNÉRALES ===")
print("Nombre de ventes :", len(df))
print("Période :", df["date_mutation"].min().date(), "->", df["date_mutation"].max().date())

print("\nValeurs manquantes (colonnes clés) :")
print(df[["valeur_fonciere", "surface_reelle_bati",
          "nombre_pieces_principales", "longitude", "latitude"]].isna().sum())

print("\nPrix de vente (€)")
print("  Moyen   :", round(df["valeur_fonciere"].mean()))
print("  Médian  :", round(df["valeur_fonciere"].median()))
print("  Minimum :", round(df["valeur_fonciere"].min()))
print("  Maximum :", round(df["valeur_fonciere"].max()))

print("\nSurface habitable (m²)")
print("  Moyenne :", round(df["surface_reelle_bati"].mean(), 1))
print("  Médiane :", df["surface_reelle_bati"].median())

print("\nNombre moyen de pièces :", round(df["nombre_pieces_principales"].mean(), 1))

# =====================================
print("\n=== ANALYSE 2 : PRIX AU M² ===")
p = df["prix_m2"]
q1, q2, q3 = p.quantile([0.25, 0.5, 0.75])
iqr = q3 - q1

print("Moyen  :", round(p.mean()), "€/m²")
print("Médian :", round(q2), "€/m²")
print("Q1 (25 %) :", round(q1), "€/m²  |  Q3 (75 %) :", round(q3), "€/m²")
print("Écart interquartile (Q3 - Q1) :", round(iqr), "€/m²")
print("Écart-type :", round(p.std()), "€/m²")

# Détection des valeurs extrêmes (règle de Tukey)
borne_basse = q1 - 1.5 * iqr
borne_haute = q3 + 1.5 * iqr
extremes = df[(p < borne_basse) | (p > borne_haute)]
print("\nSeuils des valeurs extrêmes :", round(borne_basse), "à", round(borne_haute), "€/m²")
print("Ventes hors seuils :", len(extremes), f"({len(extremes) / len(df):.1%})")

colonnes = ["type_local", "surface_reelle_bati", "valeur_fonciere", "prix_m2", "adresse_nom_voie"]
print("\n5 prix au m² les plus élevés :")
print(df.nlargest(5, "prix_m2")[colonnes])
print("\n5 prix au m² les plus bas :")
print(df.nsmallest(5, "prix_m2")[colonnes])

# =====================================
print("\n=== ANALYSE 3 : MAISONS VS APPARTEMENTS ===")
comparaison = df.groupby("type_local").agg(
    nb_ventes=("id_mutation", "count"),
    prix_median=("valeur_fonciere", "median"),
    prix_m2_moyen=("prix_m2", "mean"),
    prix_m2_median=("prix_m2", "median"),
    surface_moyenne=("surface_reelle_bati", "mean"),
    surface_mediane=("surface_reelle_bati", "median"),
    pieces_moyennes=("nombre_pieces_principales", "mean"),
).round(1)
comparaison["part_ventes_%"] = (comparaison["nb_ventes"] / len(df) * 100).round(1)
print(comparaison.T)

ecart = (comparaison.loc["Maison", "prix_m2_median"]
         / comparaison.loc["Appartement", "prix_m2_median"] - 1)
print(f"\nÉcart de prix médian au m² (maisons vs appartements) : {ecart:+.1%}")

print("\nValeurs extrêmes par type de bien :")
print(extremes["type_local"].value_counts())

# =====================================
print("\n=== ANALYSE 4 : ÉVOLUTION MENSUELLE ===")
df["mois"] = df["date_mutation"].dt.to_period("M")

mensuel = df.groupby("mois").agg(
    nb_ventes=("id_mutation", "count"),
    prix_m2_median=("prix_m2", "median"),
)
mensuel["median_appart"] = (
    df[df["type_local"] == "Appartement"].groupby("mois")["prix_m2"].median()
)
mensuel["part_maisons_%"] = (
    df.groupby("mois")["type_local"].apply(lambda s: (s == "Maison").mean() * 100)
)
print(mensuel.round(0))

print("\nPar trimestre :")
df["trimestre"] = df["date_mutation"].dt.to_period("Q")
print(df.groupby("trimestre").agg(
    nb_ventes=("id_mutation", "count"),
    prix_m2_median=("prix_m2", "median"),
).round(0))

# =====================================
print("\n=== ANALYSE 5 : GÉOGRAPHIE ===")

# Contrôle des coordonnées : sont-elles bien dans Nantes ?
print("Longitude : de", round(df["longitude"].min(), 4), "à", round(df["longitude"].max(), 4))
print("Latitude  : de", round(df["latitude"].min(), 4), "à", round(df["latitude"].max(), 4))

# Prix par code postal
df["code_postal"] = df["code_postal"].astype("Int64").astype(str)

par_cp = df.groupby("code_postal").agg(
    nb_ventes=("id_mutation", "count"),
    prix_m2_median=("prix_m2", "median"),
)
par_cp["median_appart"] = (
    df[df["type_local"] == "Appartement"].groupby("code_postal")["prix_m2"].median()
)
par_cp["part_maisons_%"] = (
    df.groupby("code_postal")["type_local"].apply(lambda s: (s == "Maison").mean() * 100)
)
print("\nPrix par code postal (du plus cher au moins cher) :")
print(par_cp.sort_values("prix_m2_median", ascending=False).round(0))

# =====================================
print("\n=== ANALYSE 6 : NOMBRE DE PIÈCES (appartements) ===")
print("Répartition brute du nombre de pièces :")
print(df["nombre_pieces_principales"].value_counts().sort_index())

apparts = df[df["type_local"] == "Appartement"].copy()
apparts["pieces"] = (
    apparts["nombre_pieces_principales"].clip(upper=5).astype(int).astype(str)
    .replace("5", "5+")
)

par_pieces = apparts.groupby("pieces").agg(
    nb_ventes=("id_mutation", "count"),
    surface_mediane=("surface_reelle_bati", "median"),
    prix_median=("valeur_fonciere", "median"),
    prix_m2_median=("prix_m2", "median"),
)
print("\nAppartements par nombre de pièces :")
print(par_pieces.round(0))
print("\nPart des appartements situés en 44000, selon le nombre de pièces (%) :")
print(apparts.groupby("pieces")["code_postal"]
      .apply(lambda s: (s == "44000").mean() * 100).round(0))