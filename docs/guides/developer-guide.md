# Guide du Développeur & Contribution

Ce document décrit comment configurer l'environnement de développement, tester et contribuer à **CleanYourTV Desktop Manager**.

---

## 1. Environnement Local

### Prérequis
- Windows 10 ou 11 (x64)
- Python 3.10 ou supérieur
- PowerShell 7 ou Windows PowerShell 5.1

### Installation
```powershell
# Cloner le dépôt
git clone https://github.com/Gnzikoune/CleanYourTV-Desktop.git
cd CleanYourTV-Desktop

# Créer l'environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

---

## 2. Structure du Code & Standards

Le projet respecte les limites strictes du **Engineering Playbook** :
- **Fichiers source :** < 300 lignes
- **Composants UI :** < 180 lignes
- **Fonctions :** < 50 lignes
- **Conventions de nommage :** `snake_case` pour fonctions/variables, `PascalCase` pour classes, `UPPER_SNAKE_CASE` pour constantes.

### Exécuter l'application en mode développement
```powershell
python main.py
```

---

## 3. Compiler l'Exécutable Portable (.exe)

La génération du binaire autonome repose sur PyInstaller :

```powershell
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed `
  --icon="assets/icon.ico" `
  --add-data "assets;assets" `
  --name="CleanYourTV-Manager" `
  main.py
```

Le résultat se trouvera dans `dist/CleanYourTV-Manager/CleanYourTV-Manager.exe`.

---

## 4. Règles de Contribution (Git Flow)

1. Toujours créer une branche courte depuis `main` à jour : `git checkout -b feat/nom-fonctionnalite` ou `fix/nom-bug`.
2. Format de commit conventionnel obligatoire :
   ```
   type(scope): description succincte (#ID_TICKET)
   ```
3. Pousser la branche et ouvrir une Pull Request vers `main`.
