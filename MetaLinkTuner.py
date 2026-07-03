"""
VRAmax PRO - Headset Performance Software
=========================================
A specialized tool for Meta Quest PCVR users to automate registry 
tweaks and CLI diagnostics for optimal simracing performance.

Author: Amaxfiles
License: GNU General Public License v3.0 (GPLv3)
Language: Python 3.x
"""


# VRAmax PRO - Headset Performance Software
# Copyright (C) 2026 Amax
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import os
import sys
import subprocess
import winreg
import webbrowser
import shutil
import json
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

# --- VRAmax BRANDING COLOR PALETTE ---
COLOR_BG_DARK = "#0B132B"
COLOR_CYAN = "#00FBEC"
COLOR_BLUE_TECH = "#1F509E"
COLOR_AMBER = "#FF9F29"
COLOR_FRAME = "#1C2541"

# --- CONFIG UTILISATEUR ---
APPDATA_BASE = os.getenv("APPDATA") or os.path.expanduser("~")
APPDATA_DIR = os.path.join(APPDATA_BASE, "VRAmax")
os.makedirs(APPDATA_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(APPDATA_DIR, "vramax_config.txt")

DEFAULT_GAMES = {
    "Automobilista 2": {
        "exe": "AMS2AVX.exe",
        "dll": "openvr_api.dll",
        "root": "",
    },
    "Assetto Corsa": {
        "exe": "acs.exe",
        "dll": "openvr_api.dll",
        "root": "",
    },
    "iRacing": {
        "exe": "iRacingSim64DX11.exe",
        "dll": "openvr_api.dll",
        "root": "",
    },
}


def ressource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def check_oxrtk_installed():
    """Vérifie si OpenXR Toolkit est installé sur le système."""
    return os.path.exists(r"C:\Program Files\OpenXR-Toolkit")


def open_url(url):
    """Ouvre une URL de manière fiable sous Windows et en exécutable PyInstaller."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(url)
        else:
            webbrowser.open_new_tab(url)
    except Exception:
        try:
            webbrowser.open_new_tab(url)
        except Exception:
            pass


# --- DICTIONNAIRE DES TRADUCTIONS ---
LANGUAGES = {
    "en": {
        "title": "VRAmax PRO - Headset Performance Software",
        "dir_label": "Meta Horizon CLI Location:",
        "browse": "Browse",
        "folder": "Folder",
        "loaded": "Loaded",
        "select_cli": "Select OculusDebugToolCLI.exe",
        "select_game_folder": "Select Game Folder",
        "folder_status": "Folder",
        "prof_title": "1. Hardware Performance Profiles",
        "prof_ext": "Extreme Profile (RTX 5080 / 5090 / 4090)",
        "prof_high": "High Profile (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Medium Profile (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Custom Setup",
        "var_title": "2. Variable Tweaking",
        "game_title": "3. OpenComposite & OXRTK Settings",
        "game_btn": "INJECT GAME MODS",
        "lbl_over": "Pixels Per Display Override:",
        "lbl_fov": "FOV Tangent Multiplier - Edge Masking:",
        "lbl_bit": "Constant Video Bitrate - Mbps:",
        "sharpness": "Sharpness:",
        "status_ready": "VRAmax system ready for optimization.",
        "btn_inject": "INJECT VR CONFIGURATION",
        "btn_odt": "Open Oculus Debug Tool",
        "btn_tuto": "Setup Guide & Prerequisites",
        "btn_paypal": "Support VRAmax",
        "btn_add_game": "Add game",
        "new_game_name": "Game name:",
        "new_game_exe": "Game exe:",
        "select_game_exe": "Select game exe",
        "game_added": "Game added:",
        "oxrtk_ok": "[OXRTK: OK]",
        "oxrtk_missing": "[OXRTK: Not detected]",
        "err_cli": "Error: OculusDebugToolCLI.exe path is incorrect!",
        "err_dll": "Error: openvr_api_opencomposite.dll not found!",
        "err_game_folder": "Please select a game folder first.",
        "err_openvr_missing": "Error: openvr_api.dll not found in this game tree!",
        "err_game_exe_missing": "Warning: game exe not found. LibOVRRT64_1.dll was copied to the selected root folder.",
        "err_files_injection": "Files injection error:",
        "err_oxrtk_config": "OXRTK config error:",
        "err_invalid_bitrate": "Error: invalid bitrate.",
        "err_generic": "Error:",
        "succ_inject": "Meta hardware alignment successful!",
        "succ_game": "OpenComposite & OXRTK injected successfully!",
        "tuto_title": "VRAmax PRO User Guide",
        "tuto_prereq_title": "Prerequisites - only once",
        "tuto_prereq_text": (
            "Before using VRAmax PRO, make sure of two things:\n\n"
            "1. Launch your game once: start your game, for example Automobilista 2, normally through Steam "
            "at least once until the main menu, then quit. This allows the game to create its configuration folders.\n\n"
            "2. Install OpenXR Toolkit: VRAmax PRO configures sharpness settings, but the main engine must be installed "
            "on your PC. Download and install OpenXR Toolkit normally on Windows.\n\n"
            "If OpenXR Toolkit is not installed, the sharpness part may not be applied correctly."
        ),
        "tuto_download_oxrtk": "Download OpenXR Toolkit",
        "tuto_step1_title": "Step 1: Headset startup and optimization - Sections 1 & 2",
        "tuto_step1_text": (
            "This step prepares your Meta Quest headset to receive a high-quality image by removing default limitations.\n\n"
            "- Right-click VRAmaxPro.exe and choose 'Run as administrator'. This is required to modify registry keys.\n"
            "- Check that the 'Meta Horizon CLI Location' path is filled correctly.\n"
            "- In section 1, select your graphics card performance profile: Extreme, High, or Medium.\n"
            "- The values in section 2 are filled automatically according to the selected profile.\n"
            "- Click the big blue button at the bottom: INJECT VR CONFIGURATION.\n\n"
            "Result: the status text turns cyan with 'Meta hardware alignment successful!'. Your headset is now optimized for Meta Link."
        ),
        "tuto_step2_title": "Step 2: Inject mods into the game - Section 3",
        "tuto_step2_text": (
            "This step bypasses SteamVR, which uses a lot of resources, and injects OpenComposite directly into the game.\n\n"
            "- Choose your game in the dropdown list, for example Automobilista 2.\n"
            "- If your game is not listed, click 'Add game', select the game exe, then validate.\n"
            "- Click the Folder button if you want to define or change the game root folder.\n"
            "- Select the main game folder, for example:\n"
            "  C:\\Program Files (x86)\\Steam\\steamapps\\common\\Automobilista 2\n\n"
            "- Set sharpness: select 'cas' and adjust the Sharpness slider. Around 70% is recommended.\n"
            "- Click the orange button: INJECT GAME MODS.\n\n"
            "Result: VRAmax PRO backs up the original DLL, replaces openvr_api.dll with the OpenComposite version, "
            "copies LibOVRRT64_1.dll into the game exe folder, then creates the matching OpenXR Toolkit configuration file."
        ),
        "tuto_step3_title": "Step 3: Launch and play",
        "tuto_step3_text": (
            "- Put your Meta Quest headset on.\n"
            "- Enable Quest Link with the cable.\n"
            "- Keep the Meta Horizon PC app open.\n"
            "- Launch your game from Steam.\n\n"
            "The game should launch directly in the headset without the heavy SteamVR environment, with a sharper image and better performance."
        ),
        "tuto_tip_title": "Developer tip:",
        "tuto_tip_text": (
            "If a game receives a major Steam update and VR no longer starts correctly, the original DLL may have been restored.\n\n"
            "In that case, simply reopen VRAmax PRO, select the game, then click INJECT GAME MODS again to instantly reapply the modification.\n\n"
            "If you add a game manually, make sure the selected exe is the main game exe. That folder is used to place LibOVRRT64_1.dll."
        ),
    },
    "fr": {
        "title": "VRAmax PRO - Logiciel de Performance Casque",
        "dir_label": "Emplacement du CLI Meta Horizon :",
        "browse": "Parcourir",
        "folder": "Dossier",
        "loaded": "Chargé",
        "select_cli": "Sélectionner OculusDebugToolCLI.exe",
        "select_game_folder": "Sélectionner le dossier du jeu",
        "folder_status": "Dossier",
        "prof_title": "1. Profils de Performance Matérielle",
        "prof_ext": "Profil Extrême (RTX 5080 / 5090 / 4090)",
        "prof_high": "Profil Haut (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Profil Moyen (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Configuration Personnalisée",
        "var_title": "2. Ajustement des Variables",
        "game_title": "3. Paramètres OpenComposite & OXRTK",
        "game_btn": "INJECTER MODS JEU",
        "lbl_over": "Pixels Per Display Override :",
        "lbl_fov": "FOV Tangent Multiplier - Masquage :",
        "lbl_bit": "Débit Vidéo Constant - Mbps :",
        "sharpness": "Netteté :",
        "status_ready": "Système VRAmax prêt pour l'optimisation.",
        "btn_inject": "INJECTER LA CONFIGURATION VR",
        "btn_odt": "Ouvrir Oculus Debug Tool",
        "btn_tuto": "Guide d'installation & prérequis",
        "btn_paypal": "Soutenir VRAmax",
        "btn_add_game": "Ajouter un jeu",
        "new_game_name": "Nom du jeu :",
        "new_game_exe": "Exe du jeu :",
        "select_game_exe": "Sélectionner l'exe du jeu",
        "game_added": "Jeu ajouté :",
        "oxrtk_ok": "[OXRTK : OK]",
        "oxrtk_missing": "[OXRTK : Non détecté]",
        "err_cli": "Erreur : chemin OculusDebugToolCLI.exe incorrect !",
        "err_dll": "Erreur : openvr_api_opencomposite.dll introuvable !",
        "err_game_folder": "Veuillez sélectionner le dossier du jeu.",
        "err_openvr_missing": "Erreur : openvr_api.dll introuvable dans ce dossier de jeu !",
        "err_game_exe_missing": "Attention : exe du jeu introuvable. LibOVRRT64_1.dll a été copiée dans la racine sélectionnée.",
        "err_files_injection": "Erreur d'injection des fichiers :",
        "err_oxrtk_config": "Erreur de configuration OXRTK :",
        "err_invalid_bitrate": "Erreur : débit vidéo invalide.",
        "err_generic": "Erreur :",
        "succ_inject": "Alignement matériel Meta réussi !",
        "succ_game": "OpenComposite & OXRTK injectés avec succès !",
        "tuto_title": "Guide d'utilisation VRAmax PRO",
        "tuto_prereq_title": "Prérequis - à faire une seule fois",
        "tuto_prereq_text": (
            "Avant d'utiliser VRAmax PRO, assure-toi de deux petites choses :\n\n"
            "1. Lancer ton jeu une première fois : démarre ton jeu, par exemple Automobilista 2, normalement via Steam "
            "au moins une fois jusqu'au menu principal, puis quitte-le. Cela permet au jeu de créer ses dossiers de configuration.\n\n"
            "2. Installer OpenXR Toolkit : VRAmax PRO configure les réglages de netteté, mais le moteur principal doit être installé "
            "sur ton PC. Télécharge et installe OpenXR Toolkit normalement sur Windows.\n\n"
            "Si OpenXR Toolkit n'est pas installé, la partie netteté peut ne pas être appliquée correctement."
        ),
        "tuto_download_oxrtk": "Télécharger OpenXR Toolkit",
        "tuto_step1_title": "Étape 1 : démarrage et optimisation du casque - Sections 1 & 2",
        "tuto_step1_text": (
            "Cette étape prépare ton casque Meta Quest à recevoir une image de haute qualité en supprimant les limitations par défaut.\n\n"
            "- Fais un clic droit sur VRAmaxPro.exe et choisis 'Exécuter en tant qu'administrateur'. C'est indispensable pour modifier les clés de registre.\n"
            "- Vérifie que le chemin 'Emplacement du CLI Meta Horizon' est bien rempli.\n"
            "- Dans la section 1, sélectionne la puissance de ta carte graphique : Profil Extrême, Profil Haut ou Profil Moyen.\n"
            "- Les valeurs de la section 2 sont remplies automatiquement selon le profil choisi.\n"
            "- Clique sur le gros bouton bleu en bas : INJECTER LA CONFIGURATION VR.\n\n"
            "Résultat : le texte en bas devient cyan avec 'Alignement matériel Meta réussi !'. Ton casque est maintenant optimisé côté Meta Link."
        ),
        "tuto_step2_title": "Étape 2 : injection des mods dans le jeu - Section 3",
        "tuto_step2_text": (
            "Cette étape permet de contourner SteamVR, qui consomme beaucoup de ressources, et d'injecter OpenComposite directement dans le jeu.\n\n"
            "- Choisis ton jeu dans la liste déroulante, par exemple Automobilista 2.\n"
            "- Si ton jeu n'est pas dans la liste, clique sur 'Ajouter un jeu', sélectionne l'exe du jeu, puis valide.\n"
            "- Clique sur le bouton Dossier si tu veux définir ou changer le dossier racine du jeu.\n"
            "- Sélectionne le dossier principal du jeu, par exemple :\n"
            "  C:\\Program Files (x86)\\Steam\\steamapps\\common\\Automobilista 2\n\n"
            "- Règle la netteté : sélectionne 'cas' et ajuste le curseur Netteté. Une valeur autour de 70% est recommandée.\n"
            "- Clique sur le bouton orange : INJECTER MODS JEU.\n\n"
            "Résultat : VRAmax PRO sauvegarde la DLL d'origine, remplace openvr_api.dll par la version OpenComposite, "
            "copie LibOVRRT64_1.dll dans le dossier de l'exe du jeu, puis crée le fichier de configuration OpenXR Toolkit correspondant."
        ),
        "tuto_step3_title": "Étape 3 : lancer et jouer",
        "tuto_step3_text": (
            "- Mets ton casque Meta Quest sur la tête.\n"
            "- Active Quest Link avec le câble.\n"
            "- Garde l'application Meta Horizon ouverte sur ton PC.\n"
            "- Lance ton jeu depuis Steam.\n\n"
            "Le jeu devrait se lancer directement dans le casque sans l'environnement lourd de SteamVR, avec une image plus nette et de meilleures performances."
        ),
        "tuto_tip_title": "Astuce du développeur :",
        "tuto_tip_text": (
            "Si un jeu reçoit une grosse mise à jour Steam et que la VR ne se lance plus correctement, il est possible que la DLL d'origine ait été restaurée.\n\n"
            "Dans ce cas, rouvre simplement VRAmax PRO, sélectionne le jeu, puis clique à nouveau sur INJECTER MODS JEU pour réappliquer instantanément la modification.\n\n"
            "Si tu ajoutes un jeu manuellement, vérifie que l'exe sélectionné est bien l'exe principal du jeu. C'est ce dossier qui sera utilisé pour placer LibOVRRT64_1.dll."
        ),
    },
    "de": {
        "title": "VRAmax PRO - Headset-Leistungssoftware",
        "dir_label": "Meta Horizon CLI Speicherort:",
        "browse": "Durchsuchen",
        "folder": "Ordner",
        "loaded": "Geladen",
        "select_cli": "OculusDebugToolCLI.exe auswählen",
        "select_game_folder": "Spielordner auswählen",
        "folder_status": "Ordner",
        "prof_title": "1. Hardware-Leistungsprofile",
        "prof_ext": "Extrem-Profil (RTX 5080 / 5090 / 4090)",
        "prof_high": "Hohes Profil (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Mittleres Profil (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Benutzerdefinierte Einstellungen",
        "var_title": "2. Variablen-Anpassung",
        "game_title": "3. OpenComposite- & OXRTK-Einstellungen",
        "game_btn": "SPIEL-MODS INJIZIEREN",
        "lbl_over": "Pixels Per Display Override:",
        "lbl_fov": "FOV Tangent Multiplier - Randmaskierung:",
        "lbl_bit": "Konstante Videobitrate - Mbps:",
        "sharpness": "Schärfe:",
        "status_ready": "VRAmax-System bereit zur Optimierung.",
        "btn_inject": "VR-KONFIGURATION INJIZIEREN",
        "btn_odt": "Oculus Debug Tool öffnen",
        "btn_tuto": "Installationsanleitung & Voraussetzungen",
        "btn_paypal": "VRAmax unterstützen",
        "btn_add_game": "Spiel hinzufügen",
        "new_game_name": "Name des Spiels:",
        "new_game_exe": "Exe-Datei des Spiels:",
        "select_game_exe": "Exe-Datei des Spiels auswählen",
        "game_added": "Spiel hinzugefügt:",
        "oxrtk_ok": "[OXRTK: OK]",
        "oxrtk_missing": "[OXRTK: Nicht erkannt]",
        "err_cli": "Fehler: Pfad zu OculusDebugToolCLI.exe ist ungültig!",
        "err_dll": "Fehler: openvr_api_opencomposite.dll nicht gefunden!",
        "err_game_folder": "Bitte zuerst einen Spielordner auswählen.",
        "err_openvr_missing": "Fehler: openvr_api.dll wurde in diesem Spielordner nicht gefunden!",
        "err_game_exe_missing": "Warnung: Spiel-exe nicht gefunden. LibOVRRT64_1.dll wurde in den ausgewählten Stammordner kopiert.",
        "err_files_injection": "Fehler bei der Datei-Injektion:",
        "err_oxrtk_config": "OXRTK-Konfigurationsfehler:",
        "err_invalid_bitrate": "Fehler: ungültige Videobitrate.",
        "err_generic": "Fehler:",
        "succ_inject": "Meta-Hardware-Ausrichtung erfolgreich!",
        "succ_game": "OpenComposite & OXRTK erfolgreich injiziert!",
        "tuto_title": "VRAmax PRO Benutzerhandbuch",
        "tuto_prereq_title": "Voraussetzungen - nur einmal",
        "tuto_prereq_text": (
            "Bevor du VRAmax PRO verwendest, stelle zwei Dinge sicher:\n\n"
            "1. Starte dein Spiel einmal normal über Steam bis zum Hauptmenü und beende es dann. "
            "Dadurch kann das Spiel seine Konfigurationsordner erstellen.\n\n"
            "2. Installiere OpenXR Toolkit: VRAmax PRO konfiguriert die Schärfe-Einstellungen, aber die Hauptkomponente muss "
            "auf deinem PC installiert sein.\n\n"
            "Wenn OpenXR Toolkit nicht installiert ist, werden die Schärfe-Einstellungen möglicherweise nicht korrekt angewendet."
        ),
        "tuto_download_oxrtk": "OpenXR Toolkit herunterladen",
        "tuto_step1_title": "Schritt 1: Headset-Start und Optimierung - Abschnitte 1 & 2",
        "tuto_step1_text": (
            "Dieser Schritt bereitet dein Meta Quest Headset auf ein hochwertiges Bild vor und entfernt Standardbeschränkungen.\n\n"
            "- Klicke mit der rechten Maustaste auf VRAmaxPro.exe und wähle 'Als Administrator ausführen'. Dies ist notwendig, um Registry-Werte zu ändern.\n"
            "- Prüfe, ob der Pfad 'Meta Horizon CLI Speicherort' korrekt ausgefüllt ist.\n"
            "- Wähle in Abschnitt 1 das Leistungsprofil deiner Grafikkarte: Extrem, Hoch oder Mittel.\n"
            "- Die Werte in Abschnitt 2 werden automatisch passend zum Profil gesetzt.\n"
            "- Klicke unten auf den großen blauen Button: VR-KONFIGURATION INJIZIEREN.\n\n"
            "Ergebnis: Der Statustext wird cyan und zeigt 'Meta-Hardware-Ausrichtung erfolgreich!'. Dein Headset ist jetzt für Meta Link optimiert."
        ),
        "tuto_step2_title": "Schritt 2: Mods ins Spiel injizieren - Abschnitt 3",
        "tuto_step2_text": (
            "Dieser Schritt umgeht SteamVR, das viele Ressourcen verbraucht, und injiziert OpenComposite direkt ins Spiel.\n\n"
            "- Wähle dein Spiel in der Liste, zum Beispiel Automobilista 2.\n"
            "- Wenn dein Spiel nicht in der Liste steht, klicke auf 'Spiel hinzufügen', wähle die Spiel-exe und bestätige.\n"
            "- Klicke auf den Ordner-Button, wenn du den Stammordner des Spiels festlegen oder ändern möchtest.\n"
            "- Wähle den Hauptordner des Spiels, zum Beispiel:\n"
            "  C:\\Program Files (x86)\\Steam\\steamapps\\common\\Automobilista 2\n\n"
            "- Stelle die Schärfe ein: Wähle 'cas' und setze den Schärfe-Regler. Etwa 70% wird empfohlen.\n"
            "- Klicke auf den orangefarbenen Button: SPIEL-MODS INJIZIEREN.\n\n"
            "Ergebnis: VRAmax PRO sichert die originale DLL, ersetzt openvr_api.dll durch die OpenComposite-Version, "
            "kopiert LibOVRRT64_1.dll in den Ordner der Spiel-exe und erstellt die passende OpenXR Toolkit-Konfigurationsdatei."
        ),
        "tuto_step3_title": "Schritt 3: Starten und spielen",
        "tuto_step3_text": (
            "- Setze dein Meta Quest Headset auf.\n"
            "- Aktiviere Quest Link per Kabel.\n"
            "- Lasse die Meta Horizon PC-App geöffnet.\n"
            "- Starte dein Spiel über Steam.\n\n"
            "Das Spiel sollte direkt im Headset starten, ohne die schwere SteamVR-Umgebung, mit schärferem Bild und besserer Leistung."
        ),
        "tuto_tip_title": "Entwickler-Tipp:",
        "tuto_tip_text": (
            "Wenn ein Steam-Update die originale DLL wiederherstellt und VR nicht mehr korrekt startet, öffne einfach VRAmax PRO erneut, "
            "wähle das Spiel aus und klicke erneut auf SPIEL-MODS INJIZIEREN.\n\n"
            "Wenn du ein Spiel manuell hinzufügst, achte darauf, dass die ausgewählte exe die Haupt-exe des Spiels ist. "
            "In diesen Ordner wird LibOVRRT64_1.dll kopiert."
        ),
    },
    "es": {
        "title": "VRAmax PRO - Software de rendimiento para visor",
        "dir_label": "Ubicación del CLI de Meta Horizon:",
        "browse": "Examinar",
        "folder": "Carpeta",
        "loaded": "Cargado",
        "select_cli": "Seleccionar OculusDebugToolCLI.exe",
        "select_game_folder": "Seleccionar carpeta del juego",
        "folder_status": "Carpeta",
        "prof_title": "1. Perfiles de rendimiento de hardware",
        "prof_ext": "Perfil extremo (RTX 5080 / 5090 / 4090)",
        "prof_high": "Perfil alto (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Perfil medio (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Configuración personalizada",
        "var_title": "2. Ajuste de variables",
        "game_title": "3. Ajustes OpenComposite y OXRTK",
        "game_btn": "INYECTAR MODS DEL JUEGO",
        "lbl_over": "Pixels Per Display Override:",
        "lbl_fov": "FOV Tangent Multiplier - Máscara de bordes:",
        "lbl_bit": "Bitrate de vídeo constante - Mbps:",
        "sharpness": "Nitidez:",
        "status_ready": "Sistema VRAmax listo para la optimización.",
        "btn_inject": "INYECTAR CONFIGURACIÓN VR",
        "btn_odt": "Abrir Oculus Debug Tool",
        "btn_tuto": "Guía de instalación y requisitos",
        "btn_paypal": "Apoyar VRAmax",
        "btn_add_game": "Añadir juego",
        "new_game_name": "Nombre del juego:",
        "new_game_exe": "Exe del juego:",
        "select_game_exe": "Seleccionar exe del juego",
        "game_added": "Juego añadido:",
        "oxrtk_ok": "[OXRTK: OK]",
        "oxrtk_missing": "[OXRTK: No detectado]",
        "err_cli": "Error: la ruta de OculusDebugToolCLI.exe no es correcta.",
        "err_dll": "Error: openvr_api_opencomposite.dll no encontrado.",
        "err_game_folder": "Selecciona primero una carpeta de juego.",
        "err_openvr_missing": "Error: openvr_api.dll no se encontró en esta carpeta del juego.",
        "err_game_exe_missing": "Aviso: exe del juego no encontrado. LibOVRRT64_1.dll se copió en la raíz seleccionada.",
        "err_files_injection": "Error al inyectar archivos:",
        "err_oxrtk_config": "Error de configuración OXRTK:",
        "err_invalid_bitrate": "Error: bitrate de vídeo no válido.",
        "err_generic": "Error:",
        "succ_inject": "Alineación de hardware Meta realizada correctamente.",
        "succ_game": "OpenComposite y OXRTK inyectados correctamente.",
        "tuto_title": "Guía de usuario de VRAmax PRO",
        "tuto_prereq_title": "Requisitos - solo una vez",
        "tuto_prereq_text": (
            "Antes de usar VRAmax PRO, asegúrate de dos cosas:\n\n"
            "1. Inicia tu juego una vez normalmente desde Steam hasta el menú principal y luego ciérralo. "
            "Esto permite que el juego cree sus carpetas de configuración.\n\n"
            "2. Instala OpenXR Toolkit: VRAmax PRO configura los ajustes de nitidez, pero el componente principal debe estar instalado "
            "en tu PC.\n\n"
            "Si OpenXR Toolkit no está instalado, la parte de nitidez puede no aplicarse correctamente."
        ),
        "tuto_download_oxrtk": "Descargar OpenXR Toolkit",
        "tuto_step1_title": "Paso 1: Inicio y optimización del visor - Secciones 1 y 2",
        "tuto_step1_text": (
            "Este paso prepara tu visor Meta Quest para recibir una imagen de alta calidad eliminando las limitaciones por defecto.\n\n"
            "- Haz clic derecho en VRAmaxPro.exe y elige 'Ejecutar como administrador'. Es necesario para modificar valores del registro.\n"
            "- Comprueba que la ruta 'Ubicación del CLI de Meta Horizon' esté rellenada correctamente.\n"
            "- En la sección 1, selecciona el perfil de rendimiento de tu tarjeta gráfica: Extremo, Alto o Medio.\n"
            "- Los valores de la sección 2 se rellenan automáticamente según el perfil seleccionado.\n"
            "- Haz clic en el gran botón azul inferior: INYECTAR CONFIGURACIÓN VR.\n\n"
            "Resultado: el texto de estado se vuelve cian y muestra 'Alineación de hardware Meta realizada correctamente'. Tu visor ya está optimizado para Meta Link."
        ),
        "tuto_step2_title": "Paso 2: Inyectar mods en el juego - Sección 3",
        "tuto_step2_text": (
            "Este paso evita SteamVR, que consume muchos recursos, e inyecta OpenComposite directamente en el juego.\n\n"
            "- Elige tu juego en la lista, por ejemplo Automobilista 2.\n"
            "- Si tu juego no aparece, pulsa 'Añadir juego', selecciona el exe del juego y confirma.\n"
            "- Pulsa el botón Carpeta si quieres definir o cambiar la carpeta raíz del juego.\n"
            "- Selecciona la carpeta principal del juego, por ejemplo:\n"
            "  C:\\Program Files (x86)\\Steam\\steamapps\\common\\Automobilista 2\n\n"
            "- Ajusta la nitidez: selecciona 'cas' y ajusta el control deslizante Nitidez. Se recomienda alrededor del 70%.\n"
            "- Pulsa el botón naranja: INYECTAR MODS DEL JUEGO.\n\n"
            "Resultado: VRAmax PRO guarda una copia de la DLL original, reemplaza openvr_api.dll por la versión OpenComposite, "
            "copia LibOVRRT64_1.dll en la carpeta del exe del juego y crea el archivo de configuración correspondiente de OpenXR Toolkit."
        ),
        "tuto_step3_title": "Paso 3: Iniciar y jugar",
        "tuto_step3_text": (
            "- Ponte el visor Meta Quest.\n"
            "- Activa Quest Link con el cable.\n"
            "- Mantén abierta la aplicación Meta Horizon en el PC.\n"
            "- Inicia el juego desde Steam.\n\n"
            "El juego debería iniciarse directamente en el visor sin el entorno pesado de SteamVR, con una imagen más nítida y mejor rendimiento."
        ),
        "tuto_tip_title": "Consejo del desarrollador:",
        "tuto_tip_text": (
            "Si un juego recibe una actualización importante de Steam y la VR deja de iniciar correctamente, es posible que se haya restaurado la DLL original.\n\n"
            "En ese caso, abre VRAmax PRO de nuevo, selecciona el juego y pulsa otra vez INYECTAR MODS DEL JUEGO para reaplicar la modificación al instante.\n\n"
            "Si añades un juego manualmente, asegúrate de que el exe seleccionado sea el exe principal del juego. Esa carpeta se usará para colocar LibOVRRT64_1.dll."
        ),
    },
}


ctk.set_appearance_mode("Dark")


class VRAMaxApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x1020")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_DARK)

        self.current_lang = "fr"
        self.is_loading_config = False
        self.selected_game_dir = ""
        self.games = json.loads(json.dumps(DEFAULT_GAMES))
        self.oxrtk_installed = check_oxrtk_installed()
        self.cli_path = self.find_oculus_cli()
        self.tuto_win = None

        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(15, 5), fill="x", padx=30)

        self.logo_path = ressource_path("logo_visuel.png")
        try:
            pil_logo = Image.open(self.logo_path)
            self.img_data_logo = ctk.CTkImage(
                light_image=pil_logo,
                dark_image=pil_logo,
                size=(200, 200),
            )
            self.logo_label = ctk.CTkLabel(self.header_frame, text="", image=self.img_data_logo)
            self.logo_label.pack(side="left")
        except Exception:
            self.logo_label = ctk.CTkLabel(
                self.header_frame,
                text="VRAmax PRO",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=COLOR_CYAN,
            )
            self.logo_label.pack(side="left")

        self.right_header = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.right_header.pack(side="right", fill="y", expand=True)

        self.lang_frame = ctk.CTkFrame(self.right_header, fg_color="transparent")
        self.lang_frame.pack(anchor="ne", pady=(0, 15))

        for lang in ["en", "fr", "de", "es"]:
            btn = ctk.CTkButton(
                self.lang_frame,
                text=lang.upper(),
                width=30,
                height=24,
                fg_color=COLOR_FRAME,
                hover_color=COLOR_BLUE_TECH,
                command=lambda l=lang: self.change_language(l),
            )
            btn.pack(side="left", padx=2)

        self.btn_donate = ctk.CTkButton(
            self.right_header,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0079C1",
            height=32,
            command=lambda: open_url("https://paypal.me/PCVRAmax"),
        )
        self.btn_donate.pack(anchor="se")

        # --- DIR FRAME ---
        self.dir_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BLUE_TECH,
            border_width=1,
        )
        self.dir_frame.pack(pady=5, fill="x", padx=30)

        self.dir_title = ctk.CTkLabel(
            self.dir_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_CYAN,
        )
        self.dir_title.pack(anchor="w", padx=15, pady=(5, 0))

        self.dir_sub_frame = ctk.CTkFrame(self.dir_frame, fg_color="transparent")
        self.dir_sub_frame.pack(fill="x", padx=15, pady=(2, 8))

        self.entry_dir = ctk.CTkEntry(
            self.dir_sub_frame,
            fg_color=COLOR_BG_DARK,
            border_color=COLOR_BLUE_TECH,
        )
        self.entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_dir.insert(0, self.cli_path)
        self.entry_dir.bind("<KeyRelease>", lambda e: self.save_user_config())

        self.btn_browse = ctk.CTkButton(
            self.dir_sub_frame,
            text="",
            width=80,
            fg_color=COLOR_BLUE_TECH,
            command=self.browse_directory,
        )
        self.btn_browse.pack(side="right")

        # --- SECTION 1: PROFILES ---
        self.profile_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BLUE_TECH,
            border_width=1,
        )
        self.profile_frame.pack(pady=5, fill="x", padx=30)

        self.profile_title = ctk.CTkLabel(
            self.profile_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_CYAN,
        )
        self.profile_title.pack(pady=5)

        self.profile_var = ctk.StringVar(value="extreme")

        for val in ["extreme", "high", "mid", "custom"]:
            rad = ctk.CTkRadioButton(
                self.profile_frame,
                text="",
                variable=self.profile_var,
                value=val,
                fg_color=COLOR_CYAN,
                command=self.update_inputs_by_profile,
            )
            rad.pack(anchor="w", padx=25, pady=2)
            setattr(self, f"radio_{val}", rad)

        # --- SECTION 2: VARIABLES ---
        self.param_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BLUE_TECH,
            border_width=1,
        )
        self.param_frame.pack(pady=5, fill="x", padx=30)

        self.param_title = ctk.CTkLabel(
            self.param_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_CYAN,
        )
        self.param_title.pack(pady=5)

        self.label_override = ctk.CTkLabel(self.param_frame, text="", text_color="#FFFFFF")
        self.label_override.pack(anchor="w", padx=25)

        self.entry_override = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK)
        self.entry_override.pack(fill="x", padx=25, pady=2)
        self.entry_override.bind("<KeyRelease>", self.detect_manual_modification)

        self.label_fov = ctk.CTkLabel(self.param_frame, text="", text_color="#FFFFFF")
        self.label_fov.pack(anchor="w", padx=25)

        self.entry_fov = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK)
        self.entry_fov.pack(fill="x", padx=25, pady=2)
        self.entry_fov.bind("<KeyRelease>", self.detect_manual_modification)

        self.label_bitrate = ctk.CTkLabel(self.param_frame, text="", text_color="#FFFFFF")
        self.label_bitrate.pack(anchor="w", padx=25)

        self.entry_bitrate = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK)
        self.entry_bitrate.pack(fill="x", padx=25, pady=2)
        self.entry_bitrate.bind("<KeyRelease>", self.detect_manual_modification)

        # --- SECTION 3: OPENCOMPOSITE & OXRTK ---
        self.game_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_FRAME,
            border_color=COLOR_AMBER,
            border_width=1,
        )
        self.game_frame.pack(pady=5, fill="x", padx=30)

        self.game_title = ctk.CTkLabel(
            self.game_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_AMBER,
        )
        self.game_title.pack(pady=5)

        self.game_sub_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.game_sub_frame.pack(fill="x", padx=15, pady=(0, 5))

        self.game_var = ctk.StringVar(value="Automobilista 2")
        self.game_dropdown = ctk.CTkOptionMenu(
            self.game_sub_frame,
            variable=self.game_var,
            values=list(self.games.keys()),
            fg_color=COLOR_BG_DARK,
            button_color=COLOR_AMBER,
            command=lambda e: self.on_game_changed(),
        )
        self.game_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_browse_game = ctk.CTkButton(
            self.game_sub_frame,
            text="",
            width=80,
            fg_color=COLOR_BLUE_TECH,
            command=self.browse_game_dir,
        )
        self.btn_browse_game.pack(side="right")

        self.btn_add_game = ctk.CTkButton(
            self.game_frame,
            text="",
            width=140,
            fg_color=COLOR_BLUE_TECH,
            command=self.open_add_game_window,
        )
        self.btn_add_game.pack(pady=(0, 8))

        self.oxr_config_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.oxr_config_frame.pack(fill="x", padx=15, pady=(5, 10))

        self.oxr_mode_var = ctk.StringVar(value="cas")
        self.oxr_mode_dropdown = ctk.CTkOptionMenu(
            self.oxr_config_frame,
            variable=self.oxr_mode_var,
            values=["cas", "fsr", "nis"],
            width=70,
            fg_color=COLOR_BG_DARK,
            command=lambda e: self.save_user_config(),
        )
        self.oxr_mode_dropdown.pack(side="left", padx=(0, 10))

        self.lbl_sharpness = ctk.CTkLabel(self.oxr_config_frame, text="", text_color="#FFFFFF")
        self.lbl_sharpness.pack(side="left", padx=(0, 5))

        self.oxr_sharpness_var = ctk.IntVar(value=70)
        self.oxr_sharpness_slider = ctk.CTkSlider(
            self.oxr_config_frame,
            variable=self.oxr_sharpness_var,
            from_=0,
            to=100,
            number_of_steps=100,
            width=120,
            command=lambda e: self.save_user_config(),
        )
        self.oxr_sharpness_slider.pack(side="left", padx=(0, 5))

        self.lbl_sharpness_val = ctk.CTkLabel(
            self.oxr_config_frame,
            textvariable=self.oxr_sharpness_var,
            text_color=COLOR_CYAN,
            width=30,
        )
        self.lbl_sharpness_val.pack(side="left")

        self.btn_inject_game = ctk.CTkButton(
            self.oxr_config_frame,
            text="",
            fg_color="#E07A5F",
            hover_color="#C06048",
            width=100,
            command=self.inject_game_mods,
        )
        self.btn_inject_game.pack(side="right")

        # --- STATUS & ACTIONS ---
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            text_color=COLOR_AMBER,
            font=ctk.CTkFont(weight="bold"),
        )
        self.status_label.pack(pady=5)

        self.btn_row_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_row_frame.pack(fill="x", padx=30, pady=2)

        self.btn_apply = ctk.CTkButton(
            self.btn_row_frame,
            text="",
            fg_color=COLOR_BLUE_TECH,
            height=40,
            command=self.apply_settings,
        )
        self.btn_apply.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_odt = ctk.CTkButton(
            self.btn_row_frame,
            text="",
            fg_color="#4E5D6C",
            width=160,
            height=40,
            command=self.open_oculus_debug_tool,
        )
        self.btn_odt.pack(side="right")

        self.btn_tuto = ctk.CTkButton(
            self,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2A9D8F",
            hover_color="#1E6B62",
            text_color="#FFFFFF",
            height=38,
            command=self.open_tutorial_window,
        )
        self.btn_tuto.pack(pady=(15, 5), fill="x", padx=30)

        self.load_user_config()
        self.change_language(self.current_lang, save=False)

    def find_oculus_cli(self):
        default_path = r"C:\Program Files\Meta Horizon\Support\oculus-diagnostics\OculusDebugToolCLI.exe"

        try:
            reg_key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Wow6432Node\Oculus VR, LLC\Oculus",
                0,
                winreg.KEY_READ,
            )
            base_folder, _ = winreg.QueryValueEx(reg_key, "BaseFolder")
            winreg.CloseKey(reg_key)

            dynamic_path = os.path.join(
                base_folder,
                "Support",
                "oculus-diagnostics",
                "OculusDebugToolCLI.exe",
            )

            if os.path.exists(dynamic_path):
                return os.path.normpath(dynamic_path)
        except Exception:
            pass

        return default_path

    def get_translations(self):
        return LANGUAGES.get(self.current_lang, LANGUAGES["fr"])

    def refresh_game_dropdown(self):
        self.game_dropdown.configure(values=list(self.games.keys()))

    def change_language(self, lang, save=True):
        if lang not in LANGUAGES:
            lang = "fr"

        self.current_lang = lang
        t = self.get_translations()

        self.title(t["title"])
        self.dir_title.configure(text=t["dir_label"])
        self.btn_browse.configure(text=t["browse"])

        self.profile_title.configure(text=t["prof_title"])
        self.radio_extreme.configure(text=t["prof_ext"])
        self.radio_high.configure(text=t["prof_high"])
        self.radio_mid.configure(text=t["prof_mid"])
        self.radio_custom.configure(text=t["prof_cust"])

        self.param_title.configure(text=t["var_title"])
        self.label_override.configure(text=t["lbl_over"])
        self.label_fov.configure(text=t["lbl_fov"])
        self.label_bitrate.configure(text=t["lbl_bit"])

        oxrtk_status = t["oxrtk_ok"] if self.oxrtk_installed else t["oxrtk_missing"]
        self.game_title.configure(text=f'{t["game_title"]} {oxrtk_status}')

        self.btn_browse_game.configure(text=t["loaded"] if self.selected_game_dir else t["folder"])
        self.btn_add_game.configure(text=t["btn_add_game"])
        self.lbl_sharpness.configure(text=t["sharpness"])

        self.btn_apply.configure(text=t["btn_inject"])
        self.btn_inject_game.configure(text=t["game_btn"])
        self.btn_odt.configure(text=t["btn_odt"])
        self.btn_tuto.configure(text=t["btn_tuto"])
        self.btn_donate.configure(text=t["btn_paypal"])

        self.status_label.configure(text=t["status_ready"], text_color=COLOR_AMBER)

        if save and not self.is_loading_config:
            self.save_user_config()

    def browse_directory(self):
        t = self.get_translations()

        file = filedialog.askopenfilename(title=t["select_cli"])
        if file:
            self.entry_dir.delete(0, ctk.END)
            self.entry_dir.insert(0, os.path.normpath(file))
            self.save_user_config()

    def browse_game_dir(self):
        t = self.get_translations()

        directory = filedialog.askdirectory(title=t["select_game_folder"])
        if directory:
            self.selected_game_dir = os.path.normpath(directory)

            game_selected = self.game_var.get()
            if game_selected in self.games:
                self.games[game_selected]["root"] = self.selected_game_dir

            self.btn_browse_game.configure(text=t["loaded"])
            self.status_label.configure(
                text=f'{t["folder_status"]}: {os.path.basename(directory)}',
                text_color=COLOR_CYAN,
            )
            self.save_user_config()

    def update_inputs_by_profile(self):
        if self.is_loading_config:
            return

        profile = self.profile_var.get()
        if profile == "custom":
            self.save_user_config()
            return

        self.entry_override.delete(0, ctk.END)
        self.entry_fov.delete(0, ctk.END)
        self.entry_bitrate.delete(0, ctk.END)

        if profile == "extreme":
            self.entry_override.insert(0, "1.3")
            self.entry_fov.insert(0, "0.78")
            self.entry_bitrate.insert(0, "800")
        elif profile == "high":
            self.entry_override.insert(0, "1.1")
            self.entry_fov.insert(0, "0.75")
            self.entry_bitrate.insert(0, "600")
        elif profile == "mid":
            self.entry_override.insert(0, "0.0")
            self.entry_fov.insert(0, "0.75")
            self.entry_bitrate.insert(0, "500")

        self.save_user_config()

    def detect_manual_modification(self, event):
        if self.profile_var.get() != "custom":
            self.profile_var.set("custom")
        self.save_user_config()

    def save_user_config(self):
        try:
            custom_games = {
                name: data
                for name, data in self.games.items()
                if name not in DEFAULT_GAMES
            }

            default_game_roots = {
                name: data.get("root", "")
                for name, data in self.games.items()
                if name in DEFAULT_GAMES
            }

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(f"language={self.current_lang}\n")
                f.write(f"profile={self.profile_var.get()}\n")
                f.write(f"override={self.entry_override.get()}\n")
                f.write(f"fov={self.entry_fov.get()}\n")
                f.write(f"bitrate={self.entry_bitrate.get()}\n")
                f.write(f"path={self.entry_dir.get()}\n")
                f.write(f"game={self.game_var.get()}\n")
                f.write(f"oxr_mode={self.oxr_mode_var.get()}\n")
                f.write(f"oxr_sharpness={self.oxr_sharpness_var.get()}\n")
                f.write(f"game_dir={self.selected_game_dir}\n")
                f.write(f"default_game_roots={json.dumps(default_game_roots, ensure_ascii=False)}\n")
                f.write(f"custom_games={json.dumps(custom_games, ensure_ascii=False)}\n")
        except Exception:
            pass

    def load_user_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                self.is_loading_config = True
                config = {}

                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            config[k] = v

                if "default_game_roots" in config:
                    try:
                        roots = json.loads(config["default_game_roots"])
                        if isinstance(roots, dict):
                            for name, root in roots.items():
                                if name in self.games:
                                    self.games[name]["root"] = root
                    except Exception:
                        pass

                if "custom_games" in config:
                    try:
                        loaded_games = json.loads(config["custom_games"])
                        if isinstance(loaded_games, dict):
                            self.games.update(loaded_games)
                    except Exception:
                        pass

                self.refresh_game_dropdown()

                if "language" in config and config["language"] in LANGUAGES:
                    self.current_lang = config["language"]

                if "path" in config and os.path.exists(config["path"]):
                    self.cli_path = config["path"]
                    self.entry_dir.delete(0, ctk.END)
                    self.entry_dir.insert(0, self.cli_path)

                if "profile" in config:
                    self.profile_var.set(config["profile"])

                self.entry_override.delete(0, ctk.END)
                self.entry_fov.delete(0, ctk.END)
                self.entry_bitrate.delete(0, ctk.END)

                self.entry_override.insert(0, config.get("override", "1.3"))
                self.entry_fov.insert(0, config.get("fov", "0.78"))
                self.entry_bitrate.insert(0, config.get("bitrate", "800"))

                if "game" in config and config["game"] in self.games:
                    self.game_var.set(config["game"])

                if "oxr_mode" in config:
                    self.oxr_mode_var.set(config["oxr_mode"])

                if "oxr_sharpness" in config:
                    try:
                        self.oxr_sharpness_var.set(int(config["oxr_sharpness"]))
                    except ValueError:
                        self.oxr_sharpness_var.set(70)

                selected_game = self.game_var.get()
                selected_root = self.games.get(selected_game, {}).get("root", "")

                if selected_root and os.path.exists(selected_root):
                    self.selected_game_dir = selected_root
                elif "game_dir" in config and os.path.exists(config["game_dir"]):
                    self.selected_game_dir = config["game_dir"]

                self.is_loading_config = False
                return
            except Exception:
                self.is_loading_config = False

        self.update_inputs_by_profile()

    def on_game_changed(self):
        game_selected = self.game_var.get()
        game_root = self.games.get(game_selected, {}).get("root", "")

        if game_root and os.path.exists(game_root):
            self.selected_game_dir = game_root
        else:
            self.selected_game_dir = ""

        t = self.get_translations()
        self.btn_browse_game.configure(text=t["loaded"] if self.selected_game_dir else t["folder"])
        self.save_user_config()

    def open_add_game_window(self):
        t = self.get_translations()

        win = ctk.CTkToplevel(self)
        win.title(t["btn_add_game"])
        win.geometry("520x260")
        win.resizable(False, False)
        win.configure(fg_color=COLOR_BG_DARK)
        win.attributes("-topmost", True)

        name_var = ctk.StringVar(value="")
        exe_var = ctk.StringVar(value="")

        ctk.CTkLabel(
            win,
            text=t["new_game_name"],
            text_color=COLOR_CYAN,
            font=ctk.CTkFont(weight="bold"),
        ).pack(anchor="w", padx=20, pady=(20, 5))

        entry_name = ctk.CTkEntry(win, textvariable=name_var, fg_color=COLOR_FRAME)
        entry_name.pack(fill="x", padx=20)

        ctk.CTkLabel(
            win,
            text=t["new_game_exe"],
            text_color=COLOR_CYAN,
            font=ctk.CTkFont(weight="bold"),
        ).pack(anchor="w", padx=20, pady=(15, 5))

        exe_frame = ctk.CTkFrame(win, fg_color="transparent")
        exe_frame.pack(fill="x", padx=20)

        entry_exe = ctk.CTkEntry(exe_frame, textvariable=exe_var, fg_color=COLOR_FRAME)
        entry_exe.pack(side="left", fill="x", expand=True, padx=(0, 5))

        def browse_exe():
            file = filedialog.askopenfilename(
                title=t["select_game_exe"],
                filetypes=[("Executable", "*.exe"), ("All files", "*.*")],
            )
            if file:
                exe_var.set(os.path.normpath(file))
                if not name_var.get().strip():
                    name_var.set(os.path.splitext(os.path.basename(file))[0])

        ctk.CTkButton(
            exe_frame,
            text=t["browse"],
            width=100,
            fg_color=COLOR_BLUE_TECH,
            command=browse_exe,
        ).pack(side="right")

        def add_game():
            name = name_var.get().strip()
            exe_path = exe_var.get().strip()

            if not name or not os.path.exists(exe_path):
                return

            game_root = os.path.dirname(exe_path)

            self.games[name] = {
                "exe": os.path.basename(exe_path),
                "root": game_root,
                "dll": "openvr_api.dll",
            }

            self.refresh_game_dropdown()
            self.game_var.set(name)
            self.selected_game_dir = game_root
            self.btn_browse_game.configure(text=t["loaded"])
            self.status_label.configure(text=f'{t["game_added"]} {name}', text_color=COLOR_CYAN)
            self.save_user_config()
            win.destroy()

        ctk.CTkButton(
            win,
            text=t["btn_add_game"],
            fg_color=COLOR_AMBER,
            hover_color="#C06048",
            command=add_game,
        ).pack(pady=25)

    def inject_game_mods(self):
        t = self.get_translations()

        game_selected = self.game_var.get()
        game_info = self.games.get(game_selected, {})

        exe_name = game_info.get("exe", "AMS2AVX.exe")
        dll_name = game_info.get("dll", "openvr_api.dll")
        game_root = game_info.get("root", "") or self.selected_game_dir

        if not game_root or not os.path.exists(game_root):
            self.status_label.configure(text=t["err_game_folder"], text_color="red")
            return

        self.selected_game_dir = game_root

        exe_path = None
        target_dll_path = None

        for root, dirs, files in os.walk(game_root):
            if exe_name in files and exe_path is None:
                exe_path = os.path.join(root, exe_name)

            if dll_name in files and target_dll_path is None:
                target_dll_path = os.path.join(root, dll_name)

            if exe_path and target_dll_path:
                break

        if exe_path:
            exe_working_dir = os.path.dirname(exe_path)
        else:
            exe_working_dir = game_root

        if not target_dll_path:
            self.status_label.configure(text=t["err_openvr_missing"], text_color="red")
            return

        backup_dll = target_dll_path + ".bak"
        oc_dll_src = ressource_path("openvr_api_opencomposite.dll")

        if not os.path.exists(oc_dll_src):
            self.status_label.configure(text=t["err_dll"], text_color="red")
            return

        try:
            if not os.path.exists(backup_dll):
                os.rename(target_dll_path, backup_dll)

            shutil.copyfile(oc_dll_src, target_dll_path)

            libovr_src = ressource_path("LibOVRRT64_1.dll")
            if os.path.exists(libovr_src):
                shutil.copyfile(libovr_src, os.path.join(exe_working_dir, "LibOVRRT64_1.dll"))

        except Exception as e:
            self.status_label.configure(text=f'{t["err_files_injection"]} {str(e)}', text_color="red")
            return

        # --- INJECTION VARIABLES OPENXR TOOLKIT ---
        appdata_local = os.environ.get("LOCALAPPDATA") or APPDATA_BASE
        oxr_dir = os.path.join(appdata_local, "OpenXR-Toolkit")
        os.makedirs(oxr_dir, exist_ok=True)

        if self.oxr_mode_var.get() == "cas":
            mode_idx = 1
        elif self.oxr_mode_var.get() == "fsr":
            mode_idx = 2
        else:
            mode_idx = 3

        oxrtk_config = {
            "upscaling_mode": mode_idx,
            "upscaling_sharpness": self.oxr_sharpness_var.get(),
            "anisotropic_filtering": 0,
            "foveated_blur": 0,
        }

        try:
            with open(os.path.join(oxr_dir, f"{exe_name}.json"), "w", encoding="utf-8") as f:
                json.dump(oxrtk_config, f, indent=4)

            if exe_path:
                self.status_label.configure(text=t["succ_game"], text_color=COLOR_AMBER)
            else:
                self.status_label.configure(
                    text=f'{t["succ_game"]} {t["err_game_exe_missing"]}',
                    text_color=COLOR_AMBER,
                )

        except Exception as e:
            self.status_label.configure(text=f'{t["err_oxrtk_config"]} {str(e)}', text_color="red")

    def apply_settings(self):
        t = self.get_translations()

        if not os.path.exists(self.entry_dir.get().strip()):
            self.status_label.configure(text=t["err_cli"], text_color="red")
            return

        try:
            bitrate = int(self.entry_bitrate.get())
        except ValueError:
            self.status_label.configure(text=t["err_invalid_bitrate"], text_color="red")
            return

        cli_commands = f"service set-pixels-per-display-pixel-override {self.entry_override.get()}\n"
        cli_commands += f"service set-client-fov-tan-angle-multiplier {self.entry_fov.get()} {self.entry_fov.get()}\n"
        cli_commands += "server:asw.Off\n"

        try:
            process = subprocess.Popen(
                [self.entry_dir.get().strip()],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            process.communicate(input=cli_commands)

            reg_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Oculus\RemoteHeadset",
                0,
                winreg.KEY_SET_VALUE,
            )
            winreg.SetValueEx(reg_key, "HEVC", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "BitrateMbps", 0, winreg.REG_DWORD, bitrate)
            winreg.SetValueEx(reg_key, "DBR", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "ResolutionWidth", 0, winreg.REG_DWORD, 4128)
            winreg.SetValueEx(reg_key, "LinkSharpening", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(reg_key)

            self.status_label.configure(text=t["succ_inject"], text_color=COLOR_CYAN)
        except Exception as e:
            self.status_label.configure(text=f'{t["err_generic"]} {str(e)}', text_color="red")

    def open_oculus_debug_tool(self):
        odt_path = os.path.join(os.path.dirname(self.entry_dir.get().strip()), "OculusDebugTool.exe")
        if os.path.exists(odt_path):
            subprocess.Popen([odt_path])

    def open_tutorial_window(self):
        t = self.get_translations()

        if self.tuto_win is not None and self.tuto_win.winfo_exists():
            self.tuto_win.focus()
            return

        self.tuto_win = ctk.CTkToplevel(self)
        self.tuto_win.title(t["tuto_title"])
        self.tuto_win.geometry("850x750")
        self.tuto_win.resizable(True, True)
        self.tuto_win.configure(fg_color=COLOR_BG_DARK)
        self.tuto_win.attributes("-topmost", True)

        scroll_frame = ctk.CTkScrollableFrame(
            self.tuto_win,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BLUE_TECH,
            border_width=1,
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        sections = [
            (t["tuto_prereq_title"], t["tuto_prereq_text"], COLOR_CYAN),
            (t["tuto_step1_title"], t["tuto_step1_text"], COLOR_AMBER),
            (t["tuto_step2_title"], t["tuto_step2_text"], COLOR_AMBER),
            (t["tuto_step3_title"], t["tuto_step3_text"], COLOR_AMBER),
            (t["tuto_tip_title"], t["tuto_tip_text"], COLOR_CYAN),
        ]

        for title, text, color in sections:
            ctk.CTkLabel(
                scroll_frame,
                text=title,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=color,
            ).pack(anchor="w", pady=(15, 5), padx=10)

            ctk.CTkLabel(
                scroll_frame,
                text=text,
                justify="left",
                text_color="#FFFFFF",
                wraplength=750,
            ).pack(anchor="w", padx=20)

        ctk.CTkButton(
            scroll_frame,
            text=t["tuto_download_oxrtk"],
            fg_color="#E07A5F",
            hover_color="#C06048",
            command=lambda: open_url("https://github.com/mbucchia/OpenXR-Toolkit"),
        ).pack(anchor="w", padx=20, pady=20)


if __name__ == "__main__":
    app = VRAMaxApp()
    app.mainloop()
