# Epic eventt

## Description

Ce projet est une application en ligne de commande (CLI) développée en Python, utilisant le framework [Click](https://click.palletsprojects.com/) pour gérer les commandes et les arguments. L'application interagit avec une base de données SQLite pour stocker et manipuler des données de manière efficace.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

## Installation

1. Clonez ce dépôt sur votre machine locale :

   ```bash
   git clone https://github.com/lethyxnekuia/epic_events
   ```

2. Accédez au répertoire du projet :

   ```bash
   cd epic_events
   ```

3. Installez les dépendances l'environnement:

   ```bash
   poetry install
   ```

4. Definissez les variables d'environnement comme dans le fichier .env.exemple

Par défault un utilisateur gestion est disponible dans la base de donnée pour pouvoir créé votre premier utilisateur:
Email : admin@admin.com
mdp : admin


## Liste des commandes 

### Commandes utilisateurs 

1. Se connecter
    ```bash
    python main.py users login 
    ```

2. Se déconnecter
    ```bash
    python main.py users logout 
    ```

### Commandes générales 

1. Lister tous les utilisateurs
    ```bash
    python main.py events list-users 
    ```

2. Lister tous les clients
    ```bash
    python main.py events list-clients 
    ```

3. Lister tous les contrats
    ```bash
    python main.py events list-contracts 
    ```

4. Lister tous les événements
    ```bash
    python main.py events list-events 
    ```

### Commandes commerciales

1. Créer un nouveau client
    ```bash
    python main.py events commercial create-client
    ```

2. Modifier un clients
    ```bash
    python main.py events commercial update-client
    ```

3. Modifier un contrat
    ```bash
    python main.py events commercial update-contract
    ```

4. Créer un nouvel événement
    ```bash
    python main.py events commercial create-event
    ```

5. Lister des contrats non signés
    ```bash
    python main.py events commercial list-contracts-not-signed
    ```

6. Lister des contrats non payés
    ```bash
    python main.py events commercial list-contracts-not-payed
    ```

### Commandes gestions

1. Créer un nouvel utilisateur
    ```bash
    python main.py events gestion create-user
    ```

2. Modifier un utilisateur
    ```bash
    python main.py events gestion update-user
    ```

3. Supprimer un utilisateur
    ```bash
    python main.py events gestion delete-user
    ```

4. Créer un nouveau contrat
    ```bash
    python main.py events gestion create-contract
    ```

5. Modifier un contrat
    ```bash
    python main.py events gestion update-contract
    ```

6. Ajouter un utilisateur support à un événement
    ```bash
    python main.py events gestion add-user-to-event
    ```

7. Liste des événements sans support
    ```bash
    python main.py events gestion list-events-without-support
    ```

### Commandes supports

1. Modifier un événement
    ```bash
    python main.py events support update-event
    ```

2. Liste des événements attribués
    ```bash
    python main.py events support list-user-events
    ```

## Test et Coverage 

1. Lancer les tests
    ```bash
    coverage run -m pytest
    ```

2. générer rapport
    ```bash
    coverage report
    ```







