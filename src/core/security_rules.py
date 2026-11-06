"""
Security Rules & Package Catalog Module
"""

# Critical packages that must NEVER be disabled to prevent bootloops / broken auth
PROTECTED_PACKAGES = {
    "android",
    "com.android.systemui",
    "com.android.settings",
    "com.android.tv.settings",
    "com.android.shell",
    "com.android.phone",
    "com.google.android.packageinstaller",
    "com.android.packageinstaller",
    "com.google.android.permissioncontroller",
    "com.android.permissioncontroller",
    "com.google.android.ext.services",
    "android.ext.services",
    "com.google.android.ext.shared",
    "android.ext.shared",
    "com.google.android.modulemetadata",
    "com.android.providers.settings",
    "com.android.inputmethod.latin",
    "com.google.android.inputmethod.latin",
    "com.liskovsoft.leankeyboard",
    "com.google.android.setupwraith",
    # Google Ecosystem / Store / Auth Protection
    "com.google.android.partnersetup",
    "com.android.vending",
    "com.google.android.gms",
    "com.google.android.gsf",
    "com.google.android.youtube.tv",
}

# Human-friendly labels for common Android TV packages
FRIENDLY_NAMES = {
    # Google Bloatware & Telemetry
    "com.google.android.katniss": "Google Assistant / Recherche vocale",
    "com.google.android.apps.mediashell": "Chromecast intégré (Google Cast)",
    "com.google.android.play.games": "Google Play Jeux",
    "com.google.android.tvlauncher": "Launcher Android TV d'origine (Stock)",
    "com.google.android.feedback": "Google Feedback (Rapports plantage)",
    "com.google.android.partnersetup": "Google Partner Setup (Requis pour Play Store)",
    "com.google.android.onetimeinitializer": "Google One-Time Initializer",
    "com.google.android.tvrecommendations": "Recommandations sponsorisées Google",
    "com.google.android.backdrop": "Écran de veille Google Backdrop",
    "com.google.android.youtube.tvmusic": "YouTube Music TV",
    "com.google.android.videos": "Google TV / Play Films",
    "com.google.android.syncadapters.calendar": "Synchronisation Agenda Google",

    # Skyworth / Coocaa / Panasonic OEM
    "com.smartdevice.dtv.icast": "CastPlay (Recopie d'écran Skyworth)",
    "com.tianci.localmedia": "Lecteur multimédia USB d'origine",
    "com.smartdevice.recommendation": "Bandeau publicitaire Daily Play",
    "com.smartdevice.acr.recommendation": "ACR (Reconnaissance de contenu à l'écran)",
    "com.smartdevice.leanbacklauncher.customizer": "Shop Customizer OEM",
    "fusion.android.tv.demo": "Mode Démo Magasin (Fusion Demo)",
    "com.sky.market": "App Store alternatif Skyworth",
    "com.community.oneroom": "Bandeau promo OneRoom",
    "com.smartdevice.epopplayer": "Lecteur Pop-up Pub Epop",
    "com.smartdevice.tvworkwithalexa": "Service vocal Amazon Alexa",
    "com.mstar.android.tv.disclaimercustomization": "MStar Disclaimer Telemetry",
    "com.Smartdevice.emanual": "Manuel utilisateur interactif",
    "com.smartdevice.firewall": "Firewall télémétrie constructeur",

    # Safe System Tools
    "com.android.printspooler": "Service d'impression papier",
    "com.android.htmlviewer": "Afficheur de pages HTML",
    "com.android.wallpaperbackup": "Sauvegarde fond d'écran",
    "com.android.backupconfirm": "Confirmation sauvegarde Cloud",
    "com.android.sharedstoragebackup": "Sauvegarde stockage partagé",
    "com.android.providers.calendar": "Fournisseur de calendrier",
}


def is_safe_to_disable(package_name: str) -> bool:
    """Check if package is safe to freeze (not in critical protected list)."""
    if package_name in PROTECTED_PACKAGES:
        return False
    return not (
        package_name.startswith("com.android.providers.")
        and "calendar" not in package_name
    )


def get_friendly_name(package_name: str) -> str:
    """Return friendly label or fallback to formatted package identifier."""
    if package_name in FRIENDLY_NAMES:
        return FRIENDLY_NAMES[package_name]
    parts = package_name.split(".")
    return parts[-1].capitalize() if parts else package_name
