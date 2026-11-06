# Project Configuration — CleanYourTV Desktop Manager

## 1. Métadonnées du Projet
- **Nom du Projet :** CleanYourTV Desktop Manager
- **Description :** Centre de contrôle Windows (Fluent 2) pour gérer, débloater et optimiser toute Android TV / Google TV.
- **Phase du Projet :** Release / Production v1.0.0
- **Dépôt GitHub :** `Gnzikoune/CleanYourTV-Desktop`
- **Licence :** MIT

## 2. Stack Technique
- **Langage :** Python 3.10+
- **Interface Utilisateur :** CustomTkinter 5.2+, Pillow 10+ (Thème Microsoft Fluent 2 Dark)
- **Protocole & Réseau :** `adb-shell` (pur socket TCP persistant), `rsa` (génération clés cryptographiques)
- **Packaging & Compilation :** PyInstaller 6.22+ (Binaire Windows x64 portable sans dépendances)
- **Miroir Vidéo Optionnel :** `scrcpy` (détection automatique)

## 3. Limites Physiques & Clean Code (Playbook §1)
- **Taille Max par Fichier Source :** 300 lignes (exception tolérée : 400 lignes pour les fenêtres UI composées)
- **Taille Max par Composant UI :** 180 lignes
- **Taille Max par Fonction :** 50 lignes
- **Arguments Max par Fonction :** 4 (utiliser des dictionnaires ou objets de config au-delà)
- **Profondeur Max (Nesting) :** 3 niveaux (Early Return obligatoire)

## 4. Architecture & Organisation (Clean Architecture)
```
src/
├── core/         # Configuration, constantes, règles de sécurité (anti-brick)
├── infra/        # Client TCP ADB, gestionnaire de clés RSA
├── services/     # Métier : débloat, optimisation système, streaming/capture
└── ui/           # Interface graphique CustomTkinter (Fluent 2) découpée en composants
```

## 5. Règles de Commit & Git Flow
- **Format Commit :** `<type>(<scope>): <message> (#<issue_id>)`
  - Types autorisés : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`
  - Exemple : `feat(infra): implement persistent socket adb client (#2)`
