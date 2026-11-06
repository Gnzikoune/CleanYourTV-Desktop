# CleanYourTV Desktop Manager 📺✨

<p align="center">
  <strong>Un centre de contrôle Windows natif (design Microsoft Fluent 2) pour piloter, débloater, optimiser et personnaliser n'importe quel téléviseur ou box Android TV / Google TV en Wi-Fi / ADB.</strong>
</p>

<p align="center">
  <a href="README.fr.md">🇫🇷 <strong>Lire en Français</strong></a> ·
  <a href="README.md">🇬🇧 <strong>Read in English</strong></a>
</p>

<p align="center">
  <a href="https://github.com/Gnzikoune/CleanYourTV-Desktop/releases/latest"><img src="https://img.shields.io/github/v/release/Gnzikoune/CleanYourTV-Desktop?color=0078D4&label=Derni%C3%A8re%20Version&logo=windows" alt="Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licence-MIT-green.svg" alt="Licence: MIT"></a>
  <a href="#"><img src="https://img.shields.io/badge/Plateforme-Windows%2010%20%7C%2011%20(x64)-0078D4?logo=windows" alt="Plateforme"></a>
  <a href="#"><img src="https://img.shields.io/badge/Design-Microsoft%20Fluent%202-005FB8" alt="Fluent 2"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python"></a>
  <a href="https://github.com/Gathin23/cleanyourtv"><img src="https://img.shields.io/badge/Compagnon%20de-CleanYourTV-orange" alt="CleanYourTV"></a>
</p>

---

## 📑 Sommaire

- [Le Problème](#-le-problème)
- [Fonctionnalités Principales](#-fonctionnalités-principales)
  - [1. Connexion Universelle & Persistante](#1-connexion-universelle--persistante)
  - [2. Télécommande Virtuelle & Saisie Clavier Directe](#2-télécommande-virtuelle--saisie-clavier-directe)
  - [3. Recopie d'Écran en Direct (scrcpy)](#3-recopie-décran-en-direct-scrcpy)
  - [4. Gestionnaire de Débloat Intelligent & Sécurisé](#4-gestionnaire-de-débloat-intelligent--sécurisé)
  - [5. Accélération Système & Optimisations Matérielles](#5-accélération-système--optimisations-matérielles)
  - [6. Confidentialité, Sécurité & Verrouillage ADB](#6-confidentialité-sécurité--verrouillage-adb)
  - [7. Thèmes & Fonds d'Écran 4K](#7-thèmes--fonds-décran-4k)
- [Activer les Options Développeur sur votre TV](#-activer-les-options-développeur-sur-votre-tv)
- [Guide de Démarrage Rapide](#-guide-de-démarrage-rapide)
  - [Méthode A : Exécutable Portable (.exe autonome, aucune installation)](#méthode-a--exécutable-portable-exe-autonome-aucune-installation)
  - [Méthode B : Exécution depuis le Code Source](#méthode-b--exécution-depuis-le-code-source)
- [Compiler l'Exécutable (.exe) vous-même](#-compiler-lexécutable-exe-vous-même)
- [Philosophie Anti-Bricking & Sécurité Absolue](#-philosophie-anti-bricking--sécurité-absolue)
- [Matrice de Compatibilité](#-matrice-de-compatibilité)
- [Dépannage & FAQ](#-dépannage--faq)
- [Contribuer](#-contribuer)
- [Licence & Remerciements](#-licence--remerciements)

---

## 🧐 Le Problème

Les téléviseurs connectés récents (Android TV, Google TV et surcouches constructeurs) souffrent tous des mêmes maux :
- **Bannières publicitaires et vidéos sponsorisées imposées** en plein milieu de l'écran d'accueil.
- **Télémétrie et mouchards d'arrière-plan** qui saturent la mémoire vive (RAM), le processeur et la bande passante réseau.
- **Ralentissements et saccades permanents** causés par le manque de puissance des puces TV d'entrée/milieu de gamme (MediaTek, Realtek, Amlogic).
- **Saisie de texte pénible** à la télécommande pour entrer un mot de passe complexe ou une recherche.

**CleanYourTV Desktop Manager** résout l'ensemble de ces problèmes depuis votre PC sous Windows, de manière visuelle, sécurisée et accessible à tous, sans aucune ligne de commande complexe.

---

## 🌟 Fonctionnalités Principales

### 1. Connexion Universelle & Persistante
- **Zéro Configuration :** Saisissez simplement l'adresse IP locale de votre TV (ou IP distante Tailscale / VPN) et cliquez sur **Connecter**.
- **Moteur ADB Direct Pure-Python :** Échange directement en socket TCP sans dépendre de l'installation préalable d'ADB sur Windows.
- **Session Persistante Ultra-Rapide :** Maintient la socket réseau ouverte pour un temps de réponse d'environ **20 millisecondes**, éliminant le délai de 2 secondes de reconnexion des scripts classiques.
- **Détection Automatique du Matériel :** Affiche instantanément la marque, le modèle précis, la version d'Android et le niveau de SDK de votre téléviseur.

### 2. Télécommande Virtuelle & Saisie Clavier Directe
- **Pavé Directionnel (D-Pad) :** Haut, Bas, Gauche, Droite, OK/Centre, Accueil (Home), Retour, Menu, Réglage du Volume (+ / - / Muet).
- **Presse-Papier & Frappe Directe PC → TV :** Copiez n'importe quel texte ou mot de passe sur Windows et injectez-le instantanément dans le champ actif de la TV.
- **Notifications Toast sur l'Écran :** Affichez un bandeau informatif HUD directement sur le téléviseur (ex: *"Le dîner est prêt !"*).

### 3. Recopie d'Écran en Direct (scrcpy)
- **Flux Vidéo 60 FPS sans latence :** Détecte et lance automatiquement `scrcpy` pour afficher l'écran de la télévision dans une fenêtre Windows fluide et contrôlable à la souris.
- **Capture d'Écran Intégrée :** Récupère une capture d'écran HD via ADB et l'ouvre directement sur votre PC.

### 4. Gestionnaire de Débloat Intelligent & Sécurisé
- **Traduction des Noms de Packages :** Fini les identifiants obscurs comme `com.smartdevice.acr.recommendation` ou `com.google.android.katniss`, le gestionnaire affiche des libellés clairs en français.
- **Désactivation Réversible en 1 Clic :** Utilise rigoureusement `pm disable-user --user 0` sans rien désinstaller de définitif.
- **Protection Anti-Brick Stricte :** Empêche formellement de désactiver les composants indispensables au démarrage du système (SystemUI, Paramètres, Installateur de paquets, Clavier).
- **Restauration d'Urgence :** Réactive l'intégralité des applications d'origine en un seul clic avec confirmation.

### 5. Accélération Système & Optimisations Matérielles
- **Vitesse des Animations (0.5x) :** Divise par deux les temps de transition d'Android pour une sensation immédiate de fluidité et de rapidité.
- **Compilation Machine AOT (Ahead-Of-Time) :** Force la compilation native (`cmd package compile -m speed`) du launcher pour supprimer tout lag au lancement des applications.

### 6. Confidentialité, Sécurité & Verrouillage ADB
- **DNS Privé Chiffré AdGuard :** Configure en un clic le DNS-over-TLS (`dns.adguard-dns.com`) au niveau système pour bloquer les publicités et traqueurs sur toute la TV sans installer d'application supplémentaire.
- **Audit de Sécurité Réseau :** Analyse les ports ouverts sur la TV (port 5555, services tiers, modules de push non sollicités).
- **Verrouillage ADB Sécurisé :** Ferme le port 5555 et coupe le débogage réseau une fois votre nettoyage terminé, garantissant qu'aucun appareil distant ne puisse accéder à votre téléviseur.

### 7. Thèmes & Fonds d'Écran 4K
- Compatible avec le launcher de référence officiel [CleanYourTV Launcher](https://github.com/Gathin23/cleanyourtv) (`com.gathin.tvhome`).
- Injection directe de n'importe quelle photo de votre PC comme fond d'écran 4K sur la TV.
- Bascule en mode Sombre Épuré (OLED Minimal) sans distraction.

---

## 📺 Activer les Options Développeur sur votre TV

Avant d'utiliser le gestionnaire, activez le **Débogage USB / Réseau** une seule fois sur votre télévision :

1. Sur la TV, allez dans **Paramètres** (`⚙️`) → **Préférences relatives à l'appareil** (ou **Système**) → **À propos**.
2. Descendez jusqu'à la ligne **Build de l'OS Android TV** (ou **Numéro de build**).
3. Cliquez **7 fois** d'affilée sur le bouton **OK** de votre télécommande physique. Un message confirmera : *"Vous êtes désormais un développeur !"*.
4. Revenez en arrière dans **Paramètres** → **Préférences relatives à l'appareil** → **Options pour les développeurs**.
5. Activez **Débogage USB** et **Débogage réseau** (ou **Débogage sans fil**).
6. Notez l'adresse IP de la TV dans **Paramètres** → **Réseau & Internet** (ex: `192.168.1.50`).
7. Lors de la toute première connexion, cochez *"Toujours autoriser depuis cet ordinateur"* sur l'écran du téléviseur.

---

## 🚀 Guide de Démarrage Rapide

### Méthode A : Exécutable Portable (.exe autonome, aucune installation)

> Idéal pour tous les utilisateurs. Aucun outil technique, ni Python, ni terminal requis.

1. Rendez-vous sur la **[Page des Releases](https://github.com/Gnzikoune/CleanYourTV-Desktop/releases/latest)**.
2. Téléchargez l'archive **`CleanYourTV-Manager-v1.0.0-windows-x64.zip`**.
3. Décompressez l'archive dans le dossier de votre choix sur votre PC.
4. Double-cliquez sur **`CleanYourTV-Manager.exe`**.
5. Renseignez l'IP de votre téléviseur et cliquez sur **⚡ Connecter**.

---

### Méthode B : Exécution depuis le Code Source

```powershell
# 1. Cloner le dépôt
git clone https://github.com/Gnzikoune/CleanYourTV-Desktop.git
cd CleanYourTV-Desktop

# 2. Créer et activer un environnement virtuel Python
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Installer les dépendances requises
pip install -r requirements.txt

# 4. Lancer le gestionnaire
python app.py
```

---

## 🛠️ Compiler l'Exécutable (.exe) vous-même

Vous pouvez générer votre propre binaire autonome avec PyInstaller :

```powershell
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed `
  --icon="assets/icon.ico" `
  --add-data "assets;assets" `
  --name="CleanYourTV-Manager" `
  app.py
```

Le programme compilé sera généré dans `dist/CleanYourTV-Manager/`.

---

## 🛡️ Philosophie Anti-Bricking & Sécurité Absolue

CleanYourTV Desktop Manager respecte rigoureusement la charte de sécurité de la communauté [CleanYourTV](https://github.com/Gathin23/cleanyourtv) :

| Règle d'or | Mise en application technique |
|---|---|
| **Aucune Désinstallation** | Utilisation exclusive de `pm disable-user --user 0`. Les fichiers système restent intacts sur la partition d'origine. |
| **Liste Noire Matérielle** | Les composants critiques (`android`, `SystemUI`, `Paramètres`, installeurs de paquets, claviers) sont verrouillés et impossibles à désactiver. |
| **Zéro Root / Zéro Flash** | Fonctionne uniquement dans l'espace utilisateur standard autorisé par Android via ADB. |
| **Confidentialité Intégrale** | Fonctionne en local direct entre votre PC et votre TV. Aucun serveur distant, aucune télémétrie, aucun pistage. |

---

## 📱 Matrice de Compatibilité

Le gestionnaire est compatible avec **tous les appareils équipés d'Android TV 8.0 (API 26) jusqu'à Android 14+ / Google TV** :

| Marque | Système d'exploitation | État | Observations |
|---|---|:---:|---|
| **Sony Bravia** | Google TV / Android TV | ✅ Testé | Excellente réactivité, compilation AOT très performante. |
| **TCL** | Google TV / Android TV | ✅ Testé | Fonctionne sur toutes les cartes mères G-series (G03, G05, G08, G10). |
| **Xiaomi / Redmi** | PatchWall / Android TV | ✅ Testé | Neutralise parfaitement les services publicitaires et traceurs. |
| **Panasonic** | Android TV 10/11 | ✅ Testé | Validé sur châssis Skyworth SW4H OEM. |
| **Philips** | Android TV / Google TV | ✅ Testé | Neutralise les démos magasins et la télémétrie constructeur. |
| **Chromecast avec Google TV** | Google TV (HD & 4K) | ✅ Testé | Avertissement Setupwraith respecté. |
| **Nvidia Shield TV** | Android TV | ✅ Testé | Réactivité maximale et contrôle fluide. |
| **Hisense / Changhong / Coocaa** | Android TV OEM | ✅ Testé | Nettoie les boucles de démonstration et les modules push. |

---

## ❓ Dépannage & FAQ

<details>
<summary><b>1. L'application indique "Connexion refusée" ou mouline lors du clic sur Connecter.</b></summary>
Vérifiez que :
- Votre téléviseur et votre ordinateur sont bien connectés au même réseau Wi-Fi / Ethernet (ou joignables via Tailscale/VPN).
- Le **Débogage USB / Réseau** est bien resté activé dans les *Options pour les développeurs* sur la TV.
- L'adresse IP renseignée est exacte (vérifiez dans *Paramètres > Réseau* sur votre TV).
</details>

<details>
<summary><b>2. La télévision affiche une demande d'autorisation.</b></summary>
Lors de la toute première connexion, Android TV affiche un message d'avertissement : *"Autoriser le débogage USB ?"*. Cochez impérativement **"Toujours autoriser depuis cet ordinateur"** puis validez sur **OK** avec la télécommande.
</details>

<details>
<summary><b>3. scrcpy ne s'ouvre pas lorsque je clique sur "Miroir Écran en Direct".</b></summary>
scrcpy est un utilitaire optionnel pour la vidéo en direct. Vous pouvez l'installer facilement sur Windows via PowerShell :
```powershell
winget install Genymobile.scrcpy
```
CleanYourTV Desktop Manager le détectera ensuite automatiquement.
</details>

<details>
<summary><b>4. Comment couper complètement l'accès ADB une fois que j'ai fini ?</b></summary>
Ouvrez l'onglet **Boost & Sécurité Système** et cliquez sur **Verrouiller ADB**. Le programme fermera le port 5555 (`stop adbd`). Pour le réactiver plus tard, il suffira de le réactiver manuellement avec votre télécommande physique dans les options développeur.
</details>

---

## 🤝 Contribuer

Les contributions, suggestions d'améliorations et signalements de bugs sont les bienvenus !

1. Forkez le projet (`https://github.com/Gnzikoune/CleanYourTV-Desktop/fork`).
2. Créez votre branche de fonctionnalité (`git checkout -b feature/NouvelleFonctionnalite`).
3. Committez vos modifications (`git commit -m 'feat: Ajout de ma fonctionnalite'`).
4. Poussez sur votre branche (`git push origin feature/NouvelleFonctionnalite`).
5. Ouvrez une Pull Request.

---

## 📄 Licence & Remerciements

- **Licence :** Distribué sous licence open-source **[MIT](LICENSE)**.
- **Communauté :** Développé comme outil compagnon pour l'initiative mondiale **[CleanYourTV](https://github.com/Gathin23/cleanyourtv)**.
