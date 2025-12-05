import pandas as pd
import matplotlib.pyplot as plt
import os

# Chargement des données
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(ROOT, "out", "conc.csv")
PLOT_DIR = os.path.join(ROOT, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)
PLOT_PATH = os.path.join(PLOT_DIR, "conc_barplot.png")

df = pd.read_csv(CSV_PATH)

# Vérifier que les données sont bien en float
df["AVG_TIME"] = df["AVG_TIME"].astype(float)

# Agrégation : moyenne et écart-type
grouped = df.groupby("PARAM")["AVG_TIME"].agg(["mean", "std"]).reset_index()

# Création du graphique
plt.figure(figsize=(10, 6))

plt.bar(
    grouped["PARAM"].astype(str),
    grouped["mean"],
    yerr=grouped["std"],
    capsize=8,
    color="#72A0FF",
    edgecolor="black",
    alpha=0.8
)

plt.title("Temps moyen par requête selon la concurrence", fontsize=16)
plt.xlabel("Nombre d'utilisateurs concurrents", fontsize=13)
plt.ylabel("Temps moyen par requête (ms)", fontsize=13)
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig(PLOT_PATH)
print(f"Graphique généré : {PLOT_PATH}")
