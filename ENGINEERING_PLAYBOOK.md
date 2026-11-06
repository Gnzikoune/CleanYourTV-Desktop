# Engineering Playbook — Standards "Elite" pour le Guardian Engineering Framework (GEF)

> **IMPORTANT :** En tant qu'IA, je m'engage à lire, comprendre et respecter scrupuleusement ces règles tout au long du développement du projet. Ce document est la référence absolue de notre façon de travailler ensemble, sur **tous les projets**, quels que soient le langage, la stack ou le domaine (SaaS, IA, jeu vidéo, mobile, backend...).
>
> Les spécificités techniques d'un projet donné (services cloud utilisés, base de données, etc.) ne figurent **jamais** ici : elles vivent dans un fichier `PROJECT_CONFIG.md` à la racine de chaque dépôt. Ce Playbook reste universel.

> **Méthodologie :** Ce Playbook orchestre la boucle **AI SDD** (*AI Spec-Driven Development*). Dans ce cycle, l'humain **Définit** les spécifications et **Vérifie** les livrables. L'IA **Analyse/Conçoit** (§2 à §4) puis **Implémente/Teste** (§8) — toujours sous les contraintes mécaniques ci-dessous.

---

## 0. Cycle de Vie du Projet & Clause d'Antériorité

L'IA doit toujours identifier la phase du projet avant d'agir (Idée → R&D → Dev Contractuel → Release → Maintenance).

> **Clause d'Antériorité (Fix Forward) :** L'IA applique les règles du Playbook sur tout le **nouveau** code produit. Elle ne doit **jamais** refactoriser proactivement du code existant uniquement pour le rendre conforme à une nouvelle règle, sauf demande explicite. Si un fichier est modifié pour un bugfix/feature, l'IA applique la **Boy Scout Rule** : nettoyer le code environnant sans casser les tests.

---

## 1. Clean Code : Métriques, Tailles et Refactoring

L'écriture du code doit suivre les **Google Engineering Practices** : la clarté prime sur la complexité (KISS). 

### 1.1. Tailles Maximales (Hard Limits)
- **Fonctions / Méthodes :** `50 lignes max`.
- **Paramètres :** `4 arguments max` (au-delà, utiliser un objet de configuration).
- **Composants UI :** `150 à 200 lignes max`. (La logique > 50 lignes doit être extraite en *Custom Hook* ou Service).
- **Fichiers :** `300 à 400 lignes max` (code source uniquement).
  - **Note :** Les artefacts générés automatiquement (package-lock.json, yarn.lock, etc.) sont exclus de cette limite selon ADR-002.

### 1.2. Complexité et Nesting
- **Profondeur (Nesting) :** `3 niveaux max`.
- **Guard Clauses (Early Return) :** Obligatoire. Éviter les `if/else` imbriqués.
- **Complexité Cyclomatique :** Maximum `10` chemins logiques par fonction.

### 1.3. Règles de Refactoring (The Rule of Three)
- **1ère fois :** Écrire pour résoudre.
- **2ème fois :** Tolérer la duplication.
- **3ème fois :** Refactorisation obligatoire en abstraction réutilisable.

### 1.4. Conventions de Nommage
- **Fichiers / Dossiers :** `kebab-case` ou `snake_case` (ex: `adb_client.py`).
- **Classes / Composants :** `PascalCase` (ex: `AdbClient`).
- **Variables / Fonctions :** `snake_case` ou `camelCase` (ex: `get_device_info`).
- **Constantes Globales :** `UPPER_SNAKE_CASE` (ex: `DEFAULT_PORT`).

---

## 2. Architecture & Design (Clean Architecture & SOLID)

Le code doit séparer le "métier" (règles de l'application) de "l'infrastructure" (frameworks, DB, UI).
- **Principe de Responsabilité Unique (SRP) :** Une classe/fonction ne fait qu'une seule chose.
- **Dependency Inversion (DIP) :** Le domaine dépend d'interfaces, pas d'implémentations.
- **Architecture par Fonctionnalité (Feature-Sliced Design) :** L'organisation des dossiers reflète le métier, pas la technique. 

---

## 3. Gestion Avancée des Erreurs (Resilience)

- **Information Hiding :** Ne **JAMAIS** exposer de stack traces ou de détails techniques au client final. Renvoyer une erreur générique ("Erreur interne") avec un ID de log.
- **Typage des Erreurs :** Créer des classes d'exceptions (ex: `DomainError`, `InfraError`, `ValidationError`).
- **Result Pattern :** Remplacer les blocs `try/catch` massifs par des retours prévisibles de type `Result<Success, Failure>` pour obliger la gestion explicite de l'échec.

---

## 4. Sécurité : OWASP Secure-by-Design & Hard Limits

*"La complexité est l'ennemie de la sécurité."*

- **Defense in Depth & Sanitisation :** Ne jamais faire confiance aux entrées. Validation stricte et échappement sécurisé de tout paramètre shell.
- **Fail-Safe Defaults :** Tout accès est refusé par défaut.
- **Gestion des secrets :** Toujours via variables d'environnement (`.env`). Jamais hardcodés.

---

## 5. Stratégie Git : Git Flow / GitHub Flow / GitLab Flow

La stabilité de la branche principale est primordiale. Nous utilisons un flux basé sur les Pull Requests/Merge Requests (PR/MR) :
- **Branche `main` verrouillée :** Les pushes directs sur `main` sont **strictement interdits**.
- **Branches Courtes :** Créez des branches par fonctionnalité (`feat/xxx`, `fix/xxx`, `docs/xxx`).
- **Pull/Merge Requests Obligatoires :** Tout code doit passer par une PR/MR.
- **Conventional Commits :** `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`. Tout commit doit inclure l'ID du ticket Kanban (`#XYZ`).

---

## 6. Documentation : Diátaxis & Docs-as-Code

La documentation technique (dossier `docs/`) doit suivre le framework cognitif **Diátaxis** :
1. **Tutoriels** (Prise en main)
2. **How-to Guides** (Tâches spécifiques)
3. **Référence** (API, DB)
4. **Explication** (Architecture, ADR)

- **Docs-as-Code & Modèle C4 :** L'architecture doit être visuelle et versionnée. Utiliser le format **Modèle C4** (Contexte, Conteneurs, Composants) généré via code (ex: `Mermaid.js`).

---

## 7. Assurance Qualité (QA) : Shift-Left & Test Pyramid

- **Shift-Left Testing :** La réflexion sur les tests commence dès l'écriture des spécifications.
- **La Pyramide des Tests :** Tests unitaires, tests d'intégration, tests end-to-end.

---

## 8. Pilotage Kanban et Autonomie de l'IA

- **Le "Pourquoi" avant tout :** Chaque Issue, PR ou tâche doit obligatoirement expliciter l'intention métier.
- **Découpage en Issues :** Utiliser GitHub CLI (`gh issue create`).
- **Création de Pull Requests :** Utiliser GitHub CLI (`gh pr create`).
- **Conventional Commits stricts :** format `type(scope): description (#ID)`.
