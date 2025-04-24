# IntelligentCar

## Nom du projet
**IntelligentCar** — Framework transversal intégrant systèmes embarqués, vision par ordinateur et intelligence artificielle.

## Description
**IntelligentCar** est un projet académique transversal réalisé par **Alec Waumans** dans le cadre de son cursus en informatique industrielle. Il regroupe plusieurs disciplines étudiées, notamment les systèmes embarqués, la vision par ordinateur et les bases de données locales. Le projet vise à démontrer l'intégration cohérente de ces domaines au sein d'une même architecture logicielle destinée au contrôle intelligent de véhicules.

### Objectifs clés
- Développer un prototype fonctionnel d’IA embarquée.
- Mettre en œuvre la détection visuelle de scènes à partir d’une caméra embarquée.
- Contrôler un véhicule à distance ou de manière autonome.
- Utiliser une base de données locale pour le stockage des données d’apprentissage ou des logs d’utilisation.

### Différenciateurs
- Intégration complète IA + embarqué + base de données.
- Projet modulaire et réutilisable.
- Orienté démonstration pédagogique et réutilisation pour d’autres projets.

## Badges
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Computer Vision](https://img.shields.io/badge/Vision-OpenCV-red)](https://opencv.org/)
[![AI](https://img.shields.io/badge/AI-PyTorch-yellow)](https://pytorch.org/)
[![Database](https://img.shields.io/badge/Database-Local-lightgrey)](https://en.wikipedia.org/wiki/Database)

## Visuels

Go to issues ! 

## Installation

### Prérequis
- Python 3.8+
- pip

### Dépendances
```bash
pip install -r requirements.txt
```
> Si `requirements.txt` est absent, installer manuellement : `numpy`, `opencv-python`, `torch`, `flask`, etc.

### Cloner le projet
```bash
git clone https://github.com/votre-utilisateur/IntelligentCar.git
cd IntelligentCar/TransProject
```

## Utilisation

### Entraîner un modèle IA
```bash
python scripts/train_model.py
```

### Contrôle IA du véhicule
```bash
python scripts/car_control.py
```

### Lancer le client de contrôle
```bash
python scripts/Client/test.py
```

### Exemple de sortie attendue
- Modèle sauvegardé dans `models/`
- Retour visuel sur les frames analysées
- Logs d’inférences, prédictions, classes détectées

## Feuille de route
- [x] Système de classification d’image
- [x] Contrôle client-serveur fonctionnel
- [ ] Intégration de modèles pré-entraînés (YOLO, EfficientNet)
- [ ] Ajout du support caméra réelle
- [ ] Visualisation embarquée (web ou GUI)

## Structure du projet
```
TransProject/
├── dataset/            # Données d'entraînement/test
├── models/             # Modèles IA sauvegardés
├── scripts/
│   ├── train_model.py  # Script d'entraînement
│   ├── car_control.py  # Contrôle IA
│   └── Client/         # Client réseau
└── car.png             # Illustration du projet
```

## Contribution
Les contributions sont les bienvenues.

### Processus
1. Fork du dépôt
2. Création d'une branche (`feature/x`)
3. Commit + Pull request clair
4. Revue par les mainteneurs

### Bonnes pratiques
- Tests dans `scripts/tests/`
- Style Python conforme à `flake8` ou `black`

## Auteurs et remerciements
**Alec Waumans** — Étudiant en informatique industrielle. Projet réalisé dans le cadre d’un projet transversal 2025. Merci aux enseignants des modules IA, systèmes embarqués et vision par ordinateur pour leur support pédagogique.

## Licence
Projet sous licence [MIT](https://opensource.org/licenses/MIT).

## Statut du projet
Projet terminé — merci à toutes les personnes ayant contribué ou soutenu son développement.