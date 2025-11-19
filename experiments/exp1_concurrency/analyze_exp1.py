import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../../out/conc.csv")

plt.figure(figsize=(8,5))
df.boxplot(column="AVG_TIME", by="PARAM")
plt.title("Scalabilité : Concurrence")
plt.suptitle("")
plt.xlabel("Concurrence")
plt.ylabel("Latency (ms)")
plt.savefig("../../plots/conc.png")
print("Plot conc.png généré !")
