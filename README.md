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
