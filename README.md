# **Projet Données Massives & Cloud — Benchmark TinyInsta**

Ce projet analyse les performances de l’application **TinyInsta**, un mini-réseau social permettant de :

* créer des posts,
* suivre des utilisateurs,
* visualiser une timeline.

L’objectif est d’étudier :

* **L’impact de la concurrence**
* **L’impact de la taille des données**

---

## **🔗 Webapp GCP déployée**

 [https://projetmassivedata.appspot.com](https://projetmassivedata.appspot.com)

---

# **Structure du dépôt**

```
├── experiments
│   ├── exp1_concurrency
│   ├── exp2_datasize
│   └── wipe_datastore.py
├── massive-gcp-master/      # Backend TinyInsta
├── out/                     # CSV du rendu final
│   ├── conc.csv
│   ├── post.csv
│   └── fanout.csv
├── plots/                   # Graphiques finaux
│   ├── conc_barplot.png
│   ├── post_barplot.png
│   └── fanout_barplot.png
└── README.md
```

---

# **2. Initialisation du projet**

## **2.1. Installation & environnement**

```sh
git clone https://github.com/StuartGrosPecs/ProjetMassiveData
cd ProjetMassiveData
python3 -m venv .venv
source .venv/bin/activate
pip install -r massive-gcp-master/requirements.txt
```

---

## **2.2. Configuration GCP**

```sh
gcloud init
gcloud config set project projetmassivedata
```

---

## **2.3. Déploiement App Engine**

```sh
cd massive-gcp-master
gcloud app deploy
```

L’application sera accessible ici :
➡️ [https://projetmassivedata.appspot.com](https://projetmassivedata.appspot.com)

---


# **3. Utilisation des expériences**

Les trois étapes sont indépendantes et doivent être lancées séparément.
---

# **Étape 1 — Expérience 1 : Concurrency**

### **Objectif**

Mesurer la latence pour 1, 10, 20, 50, 100 et 1000 requêtes simultanées.

### **1. Seed**

```sh
cd experiments/exp1_concurrency
chmod +x seed_exp1.sh
./seed_exp1.sh
```

### **2. Exécution du benchmark**

```sh
python3 benchmark_exp1.py
```

    Génère : `out/conc.csv`

### **3. Analyse graphique**

```sh
python3 analyze_exp1.py
```

    Produit : `plots/conc_barplot.png`

---

# **Étape 2 — Expérience 2A : Variation du nombre de posts**

### **Objectif**

Tester l’effet de 10, 100, 1000 posts par utilisateur.

### **1. Seed**

```sh
cd experiments/exp2_datasize/posts
chmod +x seed_posts.sh
./seed_posts.sh 10
```

Chaque seed prépare le Datastore pour le benchmark correspondant.

### **2. Exécution du benchmark**

```sh
python3 benchmark_exp2_posts.py --posts 10
```

    Génère : `out/post.csv`

**Répétez ensuite les étapes de seed et de benchmark avec les valeurs 100 puis 1000 en paramètre.**

### **3. Analyse graphique**

```sh
python3 analyze_exp2_posts.py
```

    Produit : `plots/post_barplot.png`

---

# **Étape 3 — Expérience 2B : Variation du fanout (followees)**

### **Objectif**

Tester l’effet de 10, 50, 100 followees.

### **1. Seed (obligatoire)**

```sh
cd experiments/exp2_datasize/fanout
chmod +x seed_fanout.sh
./seed_fanout.sh 10
```

### **2. Exécution du benchmark**

```sh
python3 benchmark_exp2_fanout.py --followees 10
```

    Génère : `out/fanout.csv`

**Répétez ensuite les étapes de seed et de benchmark avec les valeurs 50 puis 100 en paramètre.**

### **3. Analyse graphique**

```sh
python3 analyze_exp2_fanout.py
```

    Produit : `plots/fanout_barplot.png`

---

# **4. Format des CSV** Format des CSV**

Tous les fichiers possèdent le header :

```
PARAM,AVG_TIME,RUN,FAILED
```

Exemple :

```
10,0.2589,1,0
10,0.1794,2,0
```

---

# **5. Analyse globale**

* Plus la **concurrence** augmente → latence plus élevée.


---

# **6. Nettoyage du Datastore**

```sh
cd experiments
python3 wipe_datastore.py
```


# **7. Outils**

Pour vérifier le contenu du Datastore :
```sh
python3 tools/count_posts.py
python3 tools/count_users.py
```

# **8. Auteur**

Projet réalisé par **Yanis Dabin**,
dans le cadre du module **Données Massives & Cloud — 2025**.
