# Architecture Technique & Modèle C4

Ce document détaille l'architecture logicielle de **CleanYourTV Desktop Manager** selon le standard C4 (Contexte, Conteneurs, Composants).

---

## 1. C4 Niveau 1 : Diagramme de Contexte Système

```mermaid
flowchart TD
    User["Utilisateur (Windows Desktop)"]
    DesktopApp["CleanYourTV Desktop Manager\n(Application Native Windows)"]
    AndroidTV["Téléviseur Android TV / Google TV\n(Sony, TCL, Xiaomi, Panasonic, etc.)"]
    ScrcpyEngine["Moteur scrcpy (Optionnel)\n(Flux vidéo 60 FPS)"]

    User -->|"Pilote, débloate et saisit du texte"| DesktopApp
    DesktopApp -->|"Socket TCP persistant (Port 5555 / ADB)"| AndroidTV
    DesktopApp -->|"Orchestre et lance la fenêtre"| ScrcpyEngine
    ScrcpyEngine -->|"Flux H.264 / H.265 vidéo direct"| AndroidTV
```

---

## 2. C4 Niveau 2 : Diagramme de Conteneurs

```mermaid
flowchart TD
    subgraph WindowsClient ["Environnement Windows (Client)"]
        UI["Interface Graphique (CustomTkinter)\nMicrosoft Fluent 2 Dark Theme"]
        Services["Couche Métier (Domain Services)\nDebloat, Système, Streaming"]
        Infra["Couche Infrastructure\nClient ADB TCP + Clés RSA"]
        Config["Gestionnaire de Configuration\n~/.cleanyourtv_desktop/"]
    end

    subgraph TVDevice ["Téléviseur Android TV (Serveur)"]
        AdbDaemon["Démon adbd\n(Port TCP 5555)"]
        PackageManager["Package Manager (pm)\nUser 0 Namespace"]
        WindowManager["Window Manager (Animations / ART)"]
        NetworkSettings["Settings Global (DNS Privé)"]
    end

    UI -->|"Invoque de manière asynchrone"| Services
    Services -->|"Exécute commandes shell"| Infra
    Services -->|"Persiste état & IP"| Config
    Infra -->|"Socket TCP chiffré RSA"| AdbDaemon

    AdbDaemon -->|"pm disable-user --user 0"| PackageManager
    AdbDaemon -->|"settings put / cmd package compile"| WindowManager
    AdbDaemon -->|"settings put global private_dns"| NetworkSettings
```

---

## 3. C4 Niveau 3 : Diagramme de Composants Internes

```mermaid
classDiagram
    class MainWindow {
        +adb: AdbClient
        +debloat_service: DebloatService
        +system_service: SystemService
        +screen_service: ScreenService
        +run_async(fn)
        +set_status(text)
    }

    class RemoteTab {
        +_send_key(keycode)
        +_on_send_text()
        +_on_launch_mirror()
    }

    class DebloatTab {
        +refresh_list()
        +_toggle_package()
        +_on_restore_all()
    }

    class SystemTab {
        +_on_boost_animations()
        +_on_compile_aot()
        +_on_setup_dns()
        +_on_lockdown()
    }

    class AdbClient {
        +connect(host, port)
        +disconnect()
        +shell(command)
        +get_device_props()
    }

    class DebloatService {
        +get_disabled_packages()
        +get_all_packages()
        +disable_package(pkg)
        +enable_package(pkg)
        +restore_all()
    }

    class SystemService {
        +set_animation_scale(scale)
        +compile_aot(target)
        +configure_adguard_dns()
        +audit_security()
        +lockdown_adb()
    }

    MainWindow *-- RemoteTab
    MainWindow *-- DebloatTab
    MainWindow *-- SystemTab
    MainWindow *-- AdbClient
    MainWindow *-- DebloatService
    MainWindow *-- SystemService
    DebloatService --> AdbClient
    SystemService --> AdbClient
```

---

## 4. Diagramme de Séquence : Connexion Persistante à Faible Latence (~20ms)

```mermaid
sequenceDiagram
    autonumber
    actor U as Utilisateur
    participant UI as MainWindow (UI Thread)
    participant S as Async Worker Thread
    participant A as AdbClient (Socket TCP)
    participant TV as Android TV (adbd:5555)

    U->>UI: Clic sur 'Connecter' (IP: 192.168.1.50)
    UI->>S: Déclenche worker asynchrone (non-bloquant)
    S->>A: connect(host, port=5555)
    A->>TV: Handshake TCP SYN + CNXN (Authentification RSA)
    TV-->>A: Handshake ACK + AUTH OK
    Note over A,TV: La socket TCP reste ouverte en permanence
    S->>A: get_device_props() via socket persistante
    A->>TV: shell "getprop ro.product.model ..."
    TV-->>A: "Panasonic 4K (Android 10)"
    S-->>UI: Mise à jour UI : Badge vert + chargement packages
    UI-->>U: Interface prête et réactive
```
