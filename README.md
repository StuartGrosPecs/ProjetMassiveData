# ProjetMassiveData

Sur ma machine:
Dans ton terminal WSL, exécute :

sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates gnupg


Puis ajoute la clé Google :

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | 
sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | 
sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg


Puis installe :

sudo apt-get update && sudo apt-get install -y google-cloud-sdk
-----------------------------------------------------------------------------------------
En gros j'ai fais un gcloud init

----------------

Installer les librairies pythons

pip install matplotlib
pip install pandas


chmod +x experiments/exp1_concurrency/seed_exp1.sh
