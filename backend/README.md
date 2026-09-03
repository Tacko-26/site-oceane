# Backend — Site Océane

Backend Flask du site vitrine d'Océane, gérant le formulaire de contact et son stockage en base de données.

## À propos

Ce backend reçoit les messages envoyés depuis le formulaire de contact du site, les valide, les enregistre dans une base de données SQLite, et propose une page d'administration protégée pour les consulter.

- **Frontend** : https://tacko-26.github.io/site-oceane/
- **Backend en production** : https://site-oceane.onrender.com

## Stack technique

- **Python 3** / **Flask** — micro-framework backend
- **SQLite** — base de données légère (fichier `database.db`, généré automatiquement)
- **Gunicorn** — serveur de production (utilisé en déploiement)
- **Flask-CORS** — autorise les requêtes du frontend

## Installation en local

```bash
cd backend
pip install -r requirements.txt
```

## Lancer le serveur en local

```bash
python app.py
```

Le serveur démarre sur `http://127.0.0.1:5000`. La base de données (`database.db`) et sa table sont créées automatiquement au premier lancement si elles n'existent pas déjà.

### Variables d'environnement (optionnelles en local)

Par défaut, sans configuration, les identifiants admin sont :
- Identifiant : `oceane`
- Mot de passe : `0000`

Pour définir tes propres identifiants en local (recommandé) :

```bash
export ADMIN_USER=ton_identifiant
export ADMIN_PASSWORD=ton_mot_de_passe
python app.py
```

## Routes disponibles

| Route | Méthode | Description |
|---|---|---|
| `/api/contact` | POST | Reçoit les données du formulaire de contact (nom, email, message), les valide, et les enregistre en base. |
| `/admin` | GET | Affiche les messages reçus sous forme de tableau. Protégée par authentification (identifiant + mot de passe). |

## Déploiement (Render)

Le backend est déployé sur [Render](https://render.com), configuré ainsi :

- **Root Directory** : `backend`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn app:app`
- **Variables d'environnement** définies dans Render : `ADMIN_USER`, `ADMIN_PASSWORD`

Le fichier `database.db` n'est **pas suivi par Git** (voir `.gitignore`) — il est recréé automatiquement à chaque démarrage du serveur s'il n'existe pas.

Pour mettre à jour le backend en production, il suffit de pousser les modifications sur la branche principale du dépôt GitHub : Render redéploie automatiquement à chaque `push`.

## Limites connues et pistes d'amélioration

Ce projet a été réalisé dans le cadre d'un stage de découverte, avec un temps limité. Quelques limites assumées, à améliorer pour un usage en production plus poussé :

- **Mot de passe admin** : bien que géré via variable d'environnement (pas en clair dans le code), il n'est pas hashé. Une évolution possible serait d'utiliser un système de hashage (ex: `bcrypt`) et une vraie base d'utilisateurs.
- **Persistance de la base** : SQLite étant un simple fichier, sa persistance sur un hébergeur gratuit comme Render n'est pas garantie à 100 % dans tous les cas (redémarrages, changements d'infrastructure). Pour un usage à plus grande échelle, une base de données hébergée séparément (ex: PostgreSQL) serait préférable.
- **Pas de notification email** : les nouveaux messages ne déclenchent pas d'email automatique à Océane ; elle doit consulter la page `/admin` pour les voir.

## Contact / Suivi du projet

Pour toute question sur la reprise ou l'évolution de ce projet, le code reste documenté et commenté directement dans `app.py`.