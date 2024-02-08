![image](./litrevu/static/images/LITrevu_banner.png)

# LITRevu

### Installation et activation de l'environnement Virtuel
Ouvrez un nouveau terminal et taper  
```bash
python -m venv .env-projet9-litrevu
```
Selectionner l'environnement virtuel dans visual studio code ou l'activer en se plaçant dans le dossier **.env-litrevu/scripts** et taper
```bash
./activate
```
Installer les dependances necessaires au projet si requirements.txt est présent
```bash
pip install -r requirements.txt
```


## Projet  LITRevu

Son objectif est de commercialiser un produit permettant à une communauté d'utilisateurs de publier des critiques de livres ou d’articles et de consulter ou de solliciter une critique de livres à la demande.

Notre nouvelle application permet de demander ou publier des critiques de livres ou d’articles. L’application présente trois cas d’utilisation principaux :

1. la publication des critiques de livres ou d’articles ;
2. la demande des critiques sur un livre ou sur un article particulier ;
3. la recherche d’articles et de livres intéressants à lire, en se basant sur les critiques des autres.




Lancer le serveur de développement :
Exécutez la commande suivante pour lancer le serveur de développement :

```bash
python manage.py runserver
```

le serveur de développement a démarré à l'adresse http://127.0.0.1:8000/
 
---
### Vérification du Code : 

#### Procédure pour générer un rapport flake8 en HTML


Dans le terminal dans le dossier du projet , tapez la commande suivante pour afficher la politique d'exécution actuelle :
```
flake8 --format=html --htmldir=rapports_flake8 --exclude=.venv-projet7
```
Le rapport sera sauvegardé dans le dossier rapports_flake8, il suffira de lancer le fichier index.html


