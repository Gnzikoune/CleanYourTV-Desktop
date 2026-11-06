"""
Security Rules & Package Catalog Module
"""

# Critical packages that must NEVER be disabled to prevent bootloops / bricking
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
}

# Human-friendly labels for common Android TV packages
FRIENDLY_NAMES = {
    # Google Bloatware & Telemetry
    "com.google.android.katniss": "Google Assistant / Recherche vocale",
    "com.google.android.apps.mediashell": "Chromecast intégré (Google Cast)",
    "com.google.android.play.games": "Google Play Jeux",
    "com.google.android.tvlauncher": "Launcher Android TV d'origine (Stock)",
    "com.google.android.feedback": "Google Feedback (Rapports plantage)",
    "com.google.android.partnersetup": "Google Partner Setup",
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
    "com.smartdevice.firewall": "Pare-feu & Télémétrie OEM",
    "com.smartdevice.epopplayer": "Lecteur démo magasin e-POP",
    "fusion.android.tv.demo": "Service démonstration magasin",
    "com.Smartdevice.emanual": "Manuel interactif à l'écran",
    "com.mstar.android.tv.disclaimercustomization": "Écran premier démarrage Mstar",
    "android.autoinstalls.config.SW": "Play Auto-Installs OEM",
    "com.smartdevice.tvworkwithalexa": "Liaison Alexa OEM",
    "com.sky.market": "Boutique d'applications OEM",
    "com.community.oneroom": "Module push arrière-plan Transsion",

    # Xiaomi / Mi Box / PatchWall
    "com.xiaomi.mitv.upgrade": "Mises à jour MiTV",
    "com.mitv.gallery": "Galerie Xiaomi MiTV",
    "com.xiaomi.mitv.advert": "Service publicitaire MiTV",
    "com.xiaomi.mitv.payment": "Paiement MiTV",
    "com.mitv.tvhome": "PatchWall Launcher Xiaomi",

    # TCL Bloatware
    "com.tcl.partnercustomizer": "Personnalisation partenaire TCL",
    "com.tcl.videoplayer": "Lecteur vidéo TCL",
    "com.tcl.waterfall.overseas": "TCL Channel / Recommandations",

    # Common System Services
    "com.android.printspooler": "Spooler d'impression",
    "com.android.htmlviewer": "Visualiseur HTML",
    "com.android.backupconfirm": "Confirmation sauvegarde système",
    "com.android.sharedstoragebackup": "Sauvegarde stockage partagé",
    "com.android.wallpaperbackup": "Sauvegarde fond d'écran",
}


def is_safe_to_disable(package_name: str) -> bool:
    """Check if a package can be safely disabled without bricking the device."""
    return package_name.strip() not in PROTECTED_PACKAGES


def get_friendly_name(package_name: str) -> str:
    """Return human readable label or package name fallback."""
    return FRIENDLY_NAMES.get(package_name.strip(), package_name.strip())
