import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# PROJET DVF - NANTES 2025
# ETAPE 5 : CARTOGRAPHIE
# =====================================

df = pd.read_csv("DVF_Nantes_2025_propre.csv", low_memory=False)
os.makedirs("graphiques", exist_ok=True)

# Corrige la déformation : à la latitude de Nantes,
# un degré de longitude est plus court qu'un degré de latitude
ratio = 1 / np.cos(np.radians(47.22))

# Carte 1 : toutes les ventes
fig, ax = plt.subplots(figsize=(10, 9))
points = ax.scatter(df["longitude"], df["latitude"], c=df["prix_m2"],
                    cmap="RdYlGn_r", vmin=2000, vmax=6000, s=8, alpha=0.7)
fig.colorbar(points, ax=ax, label="Prix au m² (€)")
ax.set_aspect(ratio)
ax.set_title("Ventes immobilières à Nantes (janv.-sept. 2025)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("graphiques/04_carte_ventes.png", dpi=150)
plt.close()

# Carte 2 : prix médian par zone (hexagones)
fig, ax = plt.subplots(figsize=(10, 9))
zones = ax.hexbin(df["longitude"], df["latitude"], C=df["prix_m2"],
                  reduce_C_function=np.median, gridsize=25, mincnt=5,
                  cmap="RdYlGn_r", vmin=2000, vmax=6000)
fig.colorbar(zones, ax=ax, label="Prix médian au m² (€)")
ax.set_aspect(ratio)
ax.set_title("Prix médian au m² par zone à Nantes (janv.-sept. 2025)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("graphiques/05_carte_prix_median.png", dpi=150)
plt.close()

print("Cartes enregistrées dans le dossier graphiques/")