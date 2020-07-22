"# halitev4"

# TODO :

## Fonctions d'utils :

Class Board : Récupère toute la liste des infos

Class Ship : un uid fixe tout au long de la partie / Ennemis tués/ Halite/

Class Shipyard : un uid fixe tout au long de la partie / Cb de vaisseau il crée / halite récupéré ...

# IDEAS :

## Learning to act by predicting the future :

Un agent pour les vaisseaux et un agent pour les shipyards

Sensory :

- For each player :
  - Maps of shipyards
  - Maps of ships
  - Maps of cargo in ships
- Halite en cargo current ship
- Halite déposé
- Halite volé
- Vivant ou pas
- Ennemis tués
- Map of Halite

A prédire :

- Halite en cargo current ship (\tick)
- Halite déposé (\tick)
- Halite volé
- Vivant ou pas (\tick)
- Ennemis tués (\tick)
- Prédiction Halite

## Automate cellulaire

force attractive ou répulsive
valeur de chaque force donné par un vaisseau mère

## Implémentation Learning to Act

- https://flyyufelix.github.io/2017/11/17/direct-future-prediction.html

## Stratégies de jeu :

- Construire un shipyard déponse instantanément la halite AVANT les collisions => maneuvre d'urgence intéressante
- Construire un shipyard detruit la halite a cette case => construire des shipyards sur les meilleures cases adverses
- Construire un ship dans un shipyard juste avant qu'un vaisseau ennemi essaie de lui rentrer dedans
- Attention : construciton des ships dans un shipyard se fait en premier, donc si un autre ship essaie de déposer de la halite dans le shipyard a ce moment il est détruit

## Algo génétique

- [Lien utile](https://www.kaggle.com/c/halite/discussion/159843) pour faire des tournois entre différentes versions de nos bots et évaluer leurs performances (d'une manière proche du classement Kaggle) => permet de séléctionner (et ensuite evoluer) nos meilleurs bots pour l'algo génétique
