import pandas as pd
import matplotlib.pyplot as plt
import os

# Trouver la racine du projet
ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

CSV_PATH = os.path.join(ROOT, "out", "post.csv")
PLOT_DIR = os.path.join(ROOT, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)
PLOT_PATH = os.path.join(PLOT_DIR, "post_barplot.png")

df = pd.read_csv(CSV_PATH)
df["AVG_TIME"] = df["AVG_TIME"].astype(float)

grouped = df.groupby("PARAM")["AVG_TIME"].agg(["mean", "std"]).reset_index()

plt.figure(figsize=(10, 6))
plt.bar(
    grouped["PARAM"].astype(str),
    grouped["mean"],
    yerr=grouped["std"],
    capsize=8,
    color="#77DD77",
    edgecolor="black",
    alpha=0.85
)

plt.title("Impact du nombre de posts par utilisateur", fontsize=16)
plt.xlabel("Posts par utilisateur", fontsize=13)
plt.ylabel("Temps moyen (ms)", fontsize=13)
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig(PLOT_PATH)
print(f"Graphique généré : {PLOT_PATH}")
