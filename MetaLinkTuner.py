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


def check_opencomposite_installed():
    """Vérifie si OpenComposite App est installé ou configuré."""
    default_path = r"C:\Program Files\OpenComposite\OpenComposite.exe"
    if os.path.exists(default_path):
        return True
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("opencomposite_exe="):
                        path = line.strip().split("=", 1)[1]
                        if os.path.exists(path):
                            return True
        except Exception:
            pass
    return False


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
        "var_title": "2. Variable Tweaking\nin Oculus Debug Tool",
        "game_title": "3. OpenXR Tool Kit Settings",
        "game_btn": "INJECT in openXR",
        "lbl_over": "Pixels Per Display Override:",
        "lbl_fov": "FOV Tangent Multiplier - Edge Masking:",
        "lbl_bit": "Constant Video Bitrate - Mbps:",
        "sharpness": "Sharpness:",
        "status_ready": "Ready.",
        "btn_inject": "INJECT VR CONFIGURATION",
        "btn_odt": "Open Oculus Debug Tool",
        "btn_tuto": "Setup Guide & Prerequisites",
        "btn_paypal": "Support VRAmax",
        "btn_add_game": "Add game",
        "new_game_name": "Game name:",
        "new_game_exe": "Game exe:",
        "select_game_exe": "Select game exe",
        "game_added": "Game added:",
        "oxrtk_ok": "",
        "oxrtk_missing": "[OXRTK: Not detected]",
        "err_cli": "Error: OculusDebugToolCLI.exe path is incorrect!",
        "err_dll": "Error: openvr_api_opencomposite.dll not found!",
        "err_game_folder": "Please select a game folder first.",
        "err_openvr_missing": "Error: openvr_api.dll not found in this game tree!",
        "err_game_exe_missing": "Warning: game exe not found. LibOVRRT64_1.dll was copied to the root folder.",
        "err_files_injection": "Files injection error:",
        "err_oxrtk_config": "OXRTK config error:",
        "err_invalid_bitrate": "Error: invalid bitrate.",
        "err_generic": "Error:",
        "succ_inject": "Variables injected successfully in Oculus Debug Tool!",
        "succ_game": "Injection OK!",
        "tuto_title": "VRAmax PRO User Guide",
        "tuto_prereq_title": "Prerequisites - only once",
        "tuto_prereq_text": (
            "Before using VRAmax PRO, make sure of two things:\n\n"
            "1. Launch your game once: start your game normally through Steam "
            "at least once until the main menu, then quit.\n\n"
            "2. Install OpenXR Toolkit: VRAmax PRO configures sharpness settings, but the main engine must be installed "
            "on your PC."
        ),
        "tuto_step1_title": "Step 1: Headset startup and optimization - Sections 1 & 2",
        "tuto_step1_text": (
            "- Right-click VRAmaxPro.exe and choose 'Run as administrator'.\n"
            "- In section 1, select your graphics card performance profile.\n"
            "- Click INJECT VR CONFIGURATION."
        ),
        "tuto_step2_title": "Step 2: Inject mods into the game - Section 3",
        "tuto_step2_text": (
            "- Choose your game in the dropdown list.\n"
            "- Set sharpness (CAS recommended around 70%).\n"
            "- Click INJECT in openXR."
        ),
        "tuto_step3_title": "Step 3: Launch and play",
        "tuto_step3_text": (
            "- Put your Meta Quest headset on and enable Quest Link.\n"
            "- Launch your game from Steam."
        ),
        "tuto_tip_title": "Developer tip:",
        "tuto_tip_text": (
            "If a game receives a major Steam update and VR no longer starts correctly, the original DLL may have been restored.\n"
            "Simply click INJECT in openXR again to reapply the modification."
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
        "var_title": "2. Ajustement des Variables\ndans Oculus Debug Tool",
        "game_title": "3. Paramètres OpenXR Tool Kit",
        "game_btn": "INJECTER dans openXR",
        "lbl_over": "Pixels Per Display Override :",
        "lbl_fov": "FOV Tangent Multiplier - Masquage :",
        "lbl_bit": "Débit Vidéo Constant - Mbps :",
        "sharpness": "Netteté :",
        "status_ready": "Prêt.",
        "btn_inject": "INJECTER LA CONFIGURATION VR",
        "btn_odt": "Ouvrir Oculus Debug Tool",
        "btn_tuto": "Guide d'installation & prérequis",
        "btn_paypal": "Soutenir VRAmax",
        "btn_add_game": "Ajouter un jeu",
        "new_game_name": "Nom du jeu :",
        "new_game_exe": "Exe du jeu :",
        "select_game_exe": "Sélectionner l'exe du jeu",
        "game_added": "Jeu ajouté :",
        "oxrtk_ok": "",
        "oxrtk_missing": "[OXRTK : Non détecté]",
        "err_cli": "Erreur : chemin OculusDebugToolCLI.exe incorrect !",
        "err_dll": "Erreur : openvr_api_opencomposite.dll introuvable !",
        "err_game_folder": "Veuillez sélectionner le dossier du jeu.",
        "err_openvr_missing": "Erreur : openvr_api.dll introuvable dans ce dossier de jeu !",
        "err_game_exe_missing": "Attention : exe du jeu introuvable. LibOVRRT64_1 a été copiée.",
        "err_files_injection": "Erreur d'injection des fichiers :",
        "err_oxrtk_config": "Erreur de configuration OXRTK :",
        "err_invalid_bitrate": "Erreur : débit vidéo invalide.",
        "err_generic": "Erreur :",
        "succ_inject": "Injection des variable dans Oculus Debug Tool succés!",
        "succ_game": "Injection OK !",
        "tuto_title": "Guide d'utilisation VRAmax PRO",
        "tuto_prereq_title": "Prérequis - à faire une seule fois",
        "tuto_prereq_text": (
            "Avant d'utiliser VRAmax PRO, assure-toi de deux petites choses :\n\n"
            "1. Lancer ton jeu une première fois : démarre ton jeu normalement via Steam "
            "au moins une fois jusqu'au menu principal, puis quitte-le.\n\n"
            "2. Installer OpenXR Toolkit : VRAmax PRO configure les réglages de netteté, mais le moteur principal doit être installé "
            "sur ton PC."
        ),
        "tuto_step1_title": "Étape 1 : démarrage et optimisation du casque - Sections 1 & 2",
        "tuto_step1_text": (
            "- Fais un clic droit sur VRAmaxPro.exe et choisis 'Exécuter en tant qu'administrateur'.\n"
            "- Dans la section 1, sélectionne la puissance de ta carte graphique.\n"
            "- Clique sur INJECTER LA CONFIGURATION VR."
        ),
        "tuto_step2_title": "Étape 2 : injection des mods dans le jeu - Section 3",
        "tuto_step2_text": (
            "- Choisis ton jeu dans la liste déroulante.\n"
            "- Règle la netteté (CAS recommandé autour de 70%).\n"
            "- Clique sur INJECTER dans openXR."
        ),
        "tuto_step3_title": "Étape 3 : lancer et jouer",
        "tuto_step3_text": (
            "- Mets ton casque Meta Quest sur la tête et active Quest Link.\n"
            "- Lance ton jeu depuis Steam."
        ),
        "tuto_tip_title": "Astuce du développeur :",
        "tuto_tip_text": (
            "Si un jeu reçoit une grosse mise à jour Steam et que la VR ne se lance plus correctement, il est possible que la DLL d'origine ait été restaurée.\n"
            "Clique à nouveau sur INJECTER dans openXR pour réappliquer instantanément la modification."
        ),
    },
    "de": {
        "title": "VRAmax PRO - Headset-Leistungssoftware",
        "dir_label": "Meta Horizon CLI Speicherort:",
        "browse": "Durchsuchen",
        "folder": "Ordner",
        "loaded": "Geladen",
        "select_cli": "OculusDebugToolCLI auswählen",
        "select_game_folder": "Spielordner auswählen",
        "folder_status": "Ordner",
        "prof_title": "1. Hardware-Leistungsprofile",
        "prof_ext": "Extrem-Profil (RTX 5080/4090)",
        "prof_high": "Hohes Profil (RTX 4080/3080)",
        "prof_mid": "Mittleres Profil (RTX 4060/3060)",
        "prof_cust": "Benutzerdefiniert",
        "var_title": "2. Variablen in Oculus\nDebug Tool anpassen",
        "game_title": "3. OpenXR Tool Kit-Einstellungen",
        "game_btn": "IN OPENXR INJIZIEREN",
        "lbl_over": "Pixels Per Display Override:",
        "lbl_fov": "FOV Tangent Multiplier:",
        "lbl_bit": "Konstante Videobitrate - Mbps:",
        "sharpness": "Schärfe:",
        "status_ready": "Bereit.",
        "btn_inject": "VR-KONFIGURATION INJIZIEREN",
        "btn_odt": "Oculus Debug Tool öffnen",
        "btn_tuto": "Installationsanleitung & Voraussetzungen",
        "btn_paypal": "VRAmax unterstützen",
        "btn_add_game": "Spiel hinzufügen",
        "new_game_name": "Name des Spiels:",
        "new_game_exe": "Exe des Spiels:",
        "select_game_exe": "Exe auswählen",
        "game_added": "Spiel hinzugefügt:",
        "oxrtk_ok": "",
        "oxrtk_missing": "[OXRTK: Fehlt]",
        "err_cli": "Fehler: CLI-Pfad falsch!",
        "err_dll": "Fehler: openvr_api_opencomposite.dll fehlt!",
        "err_game_folder": "Bitte Spielordner wählen.",
        "err_openvr_missing": "Fehler: openvr_api.dll fehlt im Ordner!",
        "err_game_exe_missing": "Warnung: Exe fehlt. LibOVRRT64_1 kopiert.",
        "err_files_injection": "Fehler bei Datei-Injektion:",
        "err_oxrtk_config": "OXRTK-Fehler:",
        "err_invalid_bitrate": "Fehler: Bitrate ungültig.",
        "err_generic": "Fehler:",
        "succ_inject": "Variablen erfolgreich in Oculus Debug Tool injiziert!",
        "succ_game": "Injektion OK!",
        "tuto_title": "Benutzerhandbuch",
        "tuto_prereq_title": "Voraussetzungen",
        "tuto_prereq_text": "Bitte OpenXR Toolkit installieren und Spiel einmal starten.",
        "tuto_step1_title": "Schritt 1: Headset-Optimierung",
        "tuto_step1_text": "Als Administrator ausführen, Profil wählen, dann Konfiguration injizieren klicken.",
        "tuto_step2_title": "Schritt 2: Mods injizieren",
        "tuto_step2_text": "Spiel wählen, Schärfe anpassen, In OpenXR injizieren klicken.",
        "tuto_step3_title": "Schritt 3: Spielen",
        "tuto_step3_text": "Headset aufsetzen, Quest Link aktivieren und Spiel starten.",
        "tuto_tip_title": "Tipp:",
        "tuto_tip_text": "Nach Steam-Updates Injektion in OpenXR einfach wiederholen.",
    },
    "es": {
        "title": "VRAmax PRO - Rendimiento del visor",
        "dir_label": "Ubicación de Meta Horizon CLI:",
        "browse": "Examinar",
        "folder": "Carpeta",
        "loaded": "Cargado",
        "select_cli": "Seleccionar OculusDebugToolCLI",
        "select_game_folder": "Seleccionar carpeta",
        "folder_status": "Carpeta",
        "prof_title": "1. Perfiles de hardware",
        "prof_ext": "Perfil Extremo (RTX 5080/4090)",
        "prof_high": "Perfil Alto (RTX 4080/3080)",
        "prof_mid": "Perfil Medio (RTX 4060/3060)",
        "prof_cust": "Personalizado",
        "var_title": "2. Ajuste de variables\nen Oculus Debug Tool",
        "game_title": "3. Ajustes de OpenXR Tool Kit",
        "game_btn": "INYECTAR EN OPENXR",
        "lbl_over": "Pixels Per Display Override:",
        "lbl_fov": "FOV Tangent Multiplier:",
        "lbl_bit": "Bitrate de vídeo - Mbps:",
        "sharpness": "Nitidez:",
        "status_ready": "Listo.",
        "btn_inject": "INYECTAR CONFIGURACIÓN VR",
        "btn_odt": "Abrir Oculus Debug Tool",
        "btn_tuto": "Guía y requisitos",
        "btn_paypal": "Apoyar VRAmax",
        "btn_add_game": "Añadir juego",
        "new_game_name": "Nombre:",
        "new_game_exe": "Exe del juego:",
        "select_game_exe": "Seleccionar exe",
        "game_added": "Añadido:",
        "oxrtk_ok": "",
        "oxrtk_missing": "[OXRTK: No detectado]",
        "err_cli": "Error: ¡Ruta de CLI incorrecta!",
        "err_dll": "Error: ¡openvr_api_opencomposite.dll no encontrada!",
        "err_game_folder": "Selecciona una carpeta primero.",
        "err_openvr_missing": "Error: ¡openvr_api.dll no encontrada en el juego!",
        "err_game_exe_missing": "Aviso: Exe no encontrado. LibOVRRT64_1 copiada.",
        "err_files_injection": "Error al inyectar archivos:",
        "err_oxrtk_config": "Error de configuración OXRTK:",
        "err_invalid_bitrate": "Error: bitrate no válido.",
        "err_generic": "Error:",
        "succ_inject": "¡Variables inyectadas en Oculus Debug Tool correctamente!",
        "succ_game": "¡Inyección OK!",
        "tuto_title": "Guía de usuario",
        "tuto_prereq_title": "Requisitos",
        "tuto_prereq_text": "Instala OpenXR Toolkit e inicia el juego una vez.",
        "tuto_step1_title": "Paso 1: Optimización",
        "tuto_step1_text": "Ejecuta como administrador, elige tu perfil y haz clic en Inyectar Configuración VR.",
        "tuto_step2_title": "Paso 2: Inyectar mods",
        "tuto_step2_text": "Elige tu juego, ajusta la nitidez y haz clic en Inyectar en OpenXR.",
        "tuto_step3_title": "Paso 3: Jugar",
        "tuto_step3_text": "Ponte el visor, activa Quest Link e inicia el juego.",
        "tuto_tip_title": "Consejo:",
        "tuto_tip_text": "Si hay una actualización de Steam, vuelve a hacer clic en Inyectar en OpenXR.",
    },
}


ctk.set_appearance_mode("Dark")


class VRAMaxApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x1020")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_DARK)
        
        try:
            self.iconbitmap(ressource_path("logo.ico"))
        except Exception:
            pass

        self.current_lang = "fr"
        self.is_loading_config = False
        self.selected_game_dir = ""
        self.manual_opencomposite_path = ""
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
        self.btn_donate.pack(anchor="ne", pady=(5, 5))

        self.btn_tuto = ctk.CTkButton(
            self.right_header,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2A9D8F",
            hover_color="#1E6B62",
            text_color="#FFFFFF",
            height=32,
            command=self.open_tutorial_window,
        )
        self.btn_tuto.pack(anchor="ne", pady=(0, 5))


        # --- DIR FRAME ---
        self.dir_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BLUE_TECH,
            border_width=1,
        )
        self.dir_frame.pack(pady=5, fill="x", padx=30)

        self.dir_title_frame = ctk.CTkFrame(self.dir_frame, fg_color="transparent")
        self.dir_title_frame.pack(anchor="w", padx=15, pady=(5, 0))

        self.dir_title = ctk.CTkLabel(
            self.dir_title_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_CYAN,
        )
        self.dir_title.pack(side="left")
        
        ctk.CTkLabel(
            self.dir_title_frame,
            text=" Oculus Debug Tool",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        ).pack(side="left", padx=(5, 0))

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


        # --- SECTION 2: VARIABLES (ODT) ---
        self.param_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BLUE_TECH,
            border_width=1,
        )
        self.param_frame.pack(pady=5, fill="x", padx=30)

        self.param_title_frame = ctk.CTkFrame(self.param_frame, fg_color="transparent")
        self.param_title_frame.pack(pady=5)

        self.param_title = ctk.CTkLabel(
            self.param_title_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_CYAN,
            justify="right"
        )
        self.param_title.pack(side="left", padx=(0, 10))

        # Ocululs Icon integration
        oculus_path = ressource_path("oculus.png")
        try:
            if os.path.exists(oculus_path):
                oc_img = Image.open(oculus_path)
                self.oculus_logo = ctk.CTkImage(light_image=oc_img, dark_image=oc_img, size=(45, 45))
                ctk.CTkLabel(self.param_title_frame, text="", image=self.oculus_logo).pack(side="left")
        except Exception:
            pass

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

        self.status_label_odt = ctk.CTkLabel(
            self.param_frame,
            text="",
            text_color=COLOR_AMBER,
            font=ctk.CTkFont(weight="bold"),
        )
        self.status_label_odt.pack(pady=(5, 0))

        self.btn_row_frame = ctk.CTkFrame(self.param_frame, fg_color="transparent")
        self.btn_row_frame.pack(fill="x", padx=15, pady=(5, 15))

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


        # --- SECTION 3: OPENCOMPOSITE & OXRTK ---
        self.game_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_FRAME,
            border_color=COLOR_AMBER,
            border_width=1,
        )
        self.game_frame.pack(pady=5, fill="x", padx=30)

        self.game_title_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.game_title_frame.pack(pady=5)

        self.game_title = ctk.CTkLabel(
            self.game_title_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_AMBER,
        )
        self.game_title.pack(side="left", padx=(0, 10))

        # OpenXR Icon integration
        openxr_path = ressource_path("openxr.png")
        try:
            if os.path.exists(openxr_path):
                oxr_img = Image.open(openxr_path)
                self.openxr_logo = ctk.CTkImage(light_image=oxr_img, dark_image=oxr_img, size=(60, 20))
                ctk.CTkLabel(self.game_title_frame, text="", image=self.openxr_logo).pack(side="left")
        except Exception:
            pass

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
        self.oxr_config_frame.pack(fill="x", padx=15, pady=(5, 0))

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

        self.oxr_sharpness_var = ctk.IntVar(value=73)
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
            width=150,
            command=self.inject_game_mods,
        )
        self.btn_inject_game.pack(side="right")

        self.status_label_oxr = ctk.CTkLabel(
            self.game_frame,
            text="",
            text_color=COLOR_AMBER,
            font=ctk.CTkFont(weight="bold"),
        )
        self.status_label_oxr.pack(anchor="e", padx=25, pady=(5, 10))

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

        self.status_label_odt.configure(text=t["status_ready"], text_color=COLOR_AMBER)
        self.status_label_oxr.configure(text=t["status_ready"], text_color=COLOR_AMBER)

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
            self.status_label_oxr.configure(
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
                f.write(f"opencomposite_exe={self.manual_opencomposite_path}\n")
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

                if "opencomposite_exe" in config and os.path.exists(config["opencomposite_exe"]):
                    self.manual_opencomposite_path = config["opencomposite_exe"]

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
            self.status_label_oxr.configure(text=f'{t["game_added"]} {name}', text_color=COLOR_CYAN)
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
            self.status_label_oxr.configure(text=t["err_game_folder"], text_color="red")
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
            self.status_label_oxr.configure(text=t["err_openvr_missing"], text_color="red")
            return

        backup_dll = target_dll_path + ".bak"
        oc_dll_src = ressource_path("openvr_api_opencomposite.dll")

        if not os.path.exists(oc_dll_src):
            self.status_label_oxr.configure(text=t["err_dll"], text_color="red")
            return

        try:
            if not os.path.exists(backup_dll):
                os.rename(target_dll_path, backup_dll)

            shutil.copyfile(oc_dll_src, target_dll_path)

            libovr_src = ressource_path("LibOVRRT64_1.dll")
            if os.path.exists(libovr_src):
                shutil.copyfile(libovr_src, os.path.join(exe_working_dir, "LibOVRRT64_1.dll"))

        except Exception as e:
            self.status_label_oxr.configure(text=f'{t["err_files_injection"]} {str(e)}', text_color="red")
            return

        # --- INJECTION VARIABLES OPENXR TOOLKIT VIA REGISTRE ---
        process_name = os.path.splitext(exe_name)[0]
        reg_path = rf"Software\OpenXR_Toolkit\OpenComposite_{process_name}"
        
        # Mapping: cas=3, fsr=2, nis=1
        mode_map = {"nis": 1, "fsr": 2, "cas": 3}
        mode_val = mode_map.get(self.oxr_mode_var.get(), 3)
        sharpness_val = self.oxr_sharpness_var.get()

        try:
            # Ouverture/Création de la clé registre pour ce jeu
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
            
            # Injection des paramètres (valeurs DWORD)
            winreg.SetValueEx(reg_key, "scaling_type", 0, winreg.REG_DWORD, mode_val)
            winreg.SetValueEx(reg_key, "sharpness", 0, winreg.REG_DWORD, sharpness_val)
            winreg.SetValueEx(reg_key, "enabled", 0, winreg.REG_DWORD, 1)
            
            winreg.CloseKey(reg_key)

            if exe_path:
                self.status_label_oxr.configure(text=t["succ_game"], text_color="#00FF00")
            else:
                self.status_label_oxr.configure(
                    text=f'{t["succ_game"]} {t["err_game_exe_missing"]}',
                    text_color="#00FF00",
                )

        except Exception as e:
            self.status_label_oxr.configure(text=f"Registry Error: {str(e)}", text_color="red")

    def apply_settings(self):
        t = self.get_translations()

        if not os.path.exists(self.entry_dir.get().strip()):
            self.status_label_odt.configure(text=t["err_cli"], text_color="red")
            return

        try:
            bitrate = int(self.entry_bitrate.get())
        except ValueError:
            self.status_label_odt.configure(text=t["err_invalid_bitrate"], text_color="red")
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

            self.status_label_odt.configure(text=t["succ_inject"], text_color="#00FF00")
        except Exception as e:
            self.status_label_odt.configure(text=f'{t["err_generic"]} {str(e)}', text_color="red")

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
        self.tuto_win.geometry("950x900")
        self.tuto_win.configure(fg_color=COLOR_BG_DARK)
        self.tuto_win.attributes("-topmost", True)

        scroll_frame = ctk.CTkScrollableFrame(
            self.tuto_win,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BLUE_TECH,
            border_width=1,
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- BLOC DE COMPOSANTS ALIGNÉS AVEC LES IMAGES 1, 2, 3 ---
        components_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        components_frame.pack(fill="x", pady=10, padx=10)

        # Chargement et redimensionnement des icônes numérotées (compatibilité PyInstaller)
        img1_path = ressource_path("1_2.jpg")
        img2_path = ressource_path("2_2.jpg")
        img3_path = ressource_path("3_2.jpg")
        
        img_size = (35, 35)
        ctk_img1, ctk_img2, ctk_img3 = None, None, None
        
        try:
            if os.path.exists(img1_path):
                ctk_img1 = ctk.CTkImage(Image.open(img1_path), size=img_size)
            if os.path.exists(img2_path):
                ctk_img2 = ctk.CTkImage(Image.open(img2_path), size=img_size)
            if os.path.exists(img3_path):
                ctk_img3 = ctk.CTkImage(Image.open(img3_path), size=img_size)
        except Exception:
            pass

        # --- LIGNE 1 : LINK CONFIGURATION ---
        row1 = ctk.CTkFrame(components_frame, fg_color="transparent")
        row1.pack(fill="x", pady=8)
        if ctk_img1:
            ctk.CTkLabel(row1, text="", image=ctk_img1).pack(side="left", padx=(0, 10))
        
        # Statut Link CLI
        link_installed = os.path.exists(self.entry_dir.get().strip())
        link_status_txt = "OK" if link_installed else "Non détecté - Renseigner l'emplacement CLI"
        link_status_color = "green" if link_installed else "red"
        
        ctk.CTkLabel(row1, text="Configuration Meta Link :", font=ctk.CTkFont(weight="bold"), text_color="#FFFFFF").pack(side="left", padx=5)
        ctk.CTkLabel(row1, text=link_status_txt, font=ctk.CTkFont(weight="bold"), text_color=link_status_color).pack(side="left", padx=10)

        # --- LIGNE 2 : OPENXR TOOLKIT ---
        row2 = ctk.CTkFrame(components_frame, fg_color="transparent")
        row2.pack(fill="x", pady=8)
        if ctk_img2:
            ctk.CTkLabel(row2, text="", image=ctk_img2).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            row2,
            text="Télécharger OpenXR Toolkit",
            fg_color="#E07A5F",
            hover_color="#C06048",
            command=lambda: open_url("https://github.com/mbucchia/OpenXR-Toolkit"),
        ).pack(side="left", padx=5)

        def open_oxrtk():
            path = r"C:\Program Files\OpenXR-Toolkit\companion.exe"
            if os.path.exists(path):
                subprocess.Popen([path])
            elif os.path.exists(r"C:\Program Files\OpenXR-Toolkit"):
                os.startfile(r"C:\Program Files\OpenXR-Toolkit")
            else:
                exe = filedialog.askopenfilename(title="Sélectionner OpenXR Toolkit Companion", filetypes=[("Executable", "*.exe")])
                if exe:
                    subprocess.Popen([exe])

        ctk.CTkButton(
            row2,
            text="Ouvrir OpenXR Toolkit",
            fg_color=COLOR_BLUE_TECH,
            command=open_oxrtk,
        ).pack(side="left", padx=5)

        # Statut Dynamique OpenXR Toolkit
        oxr_status_txt = "OK" if self.oxrtk_installed else "Non détecté - Suivre les prérequis d'installation"
        oxr_status_color = "green" if self.oxrtk_installed else "red"
        ctk.CTkLabel(row2, text=oxr_status_txt, font=ctk.CTkFont(weight="bold"), text_color=oxr_status_color).pack(side="left", padx=10)

        # --- LIGNE 3 : OPENCOMPOSITE ---
        row3 = ctk.CTkFrame(components_frame, fg_color="transparent")
        row3.pack(fill="x", pady=8)
        if ctk_img3:
            ctk.CTkLabel(row3, text="", image=ctk_img3).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            row3,
            text="Télécharger OpenComposite",
            fg_color="#E07A5F",
            hover_color="#C06048",
            command=lambda: open_url("https://znix.xyz/OpenComposite/runtimeswitcher.php?branch=openxr"),
        ).pack(side="left", padx=5)

        def open_opencomp():
            # Essai 1: Chemin par défaut de la version globale
            default_exe = r"C:\Program Files\OpenComposite\OpenComposite.exe"
            # Essai 2: Utilisation de la sélection manuelle précédente stockée
            if self.manual_opencomposite_path and os.path.exists(self.manual_opencomposite_path):
                subprocess.Popen([self.manual_opencomposite_path])
                return
            
            if os.path.exists(default_exe):
                subprocess.Popen([default_exe])
            else:
                # Si l'application ne sait pas où opencomposite se trouve, on propose de chercher l'EXE manuel
                file_selected = filedialog.askopenfilename(
                    title="Où se trouve l'exécutable OpenComposite.exe ?", 
                    filetypes=[("OpenComposite Executable", "*.exe")]
                )
                if file_selected:
                    self.manual_opencomposite_path = os.path.normpath(file_selected)
                    self.save_user_config()
                    subprocess.Popen([self.manual_opencomposite_path])
                    # Forcer le rafraîchissement visuel du label
                    lbl_oc_status.configure(text="OK", text_color="green")

        ctk.CTkButton(
            row3,
            text="Ouvrir OpenComposite",
            fg_color=COLOR_BLUE_TECH,
            command=open_opencomp,
        ).pack(side="left", padx=5)

        # Statut Dynamique OpenComposite
        oc_installed = check_opencomposite_installed()
        oc_status_txt = "OK" if oc_installed else "Non détecté - Suivre les prérequis d'installation"
        oc_status_color = "green" if oc_installed else "red"
        lbl_oc_status = ctk.CTkLabel(row3, text=oc_status_txt, font=ctk.CTkFont(weight="bold"), text_color=oc_status_color)
        lbl_oc_status.pack(side="left", padx=10)


        # --- 2. IMAGE DES PRÉFÉRENCES ---
        img_path = ressource_path("reglage preference graphique casque.png")
        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                w, h = pil_img.size
                ratio = 500 / float(w)
                new_size = (500, int(float(h) * ratio))
                img_data = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=new_size)
                ctk.CTkLabel(scroll_frame, text="", image=img_data).pack(pady=(10, 20))
            except Exception:
                pass


        # --- 3. TEXTE DU TUTORIEL ---
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


if __name__ == "__main__":
    app = VRAMaxApp()
    app.mainloop()
