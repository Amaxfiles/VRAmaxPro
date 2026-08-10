# VRAmax PRO - Headset Performance Software
# Copyright (C) 2026 Amax

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
    "Automobilista 2": {"exe": "AMS2AVX.exe", "dll": "openvr_api.dll", "root": ""},
    "Assetto Corsa": {"exe": "acs.exe", "dll": "openvr_api.dll", "root": ""},
    "iRacing": {"exe": "iRacingSim64DX11.exe", "dll": "openvr_api.dll", "root": ""},
}

def ressource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_oxrtk_installed():
    return os.path.exists(r"C:\Program Files\OpenXR-Toolkit")

def check_opencomposite_installed():
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
    try:
        if sys.platform.startswith("win"):
            os.startfile(url)
        else:
            webbrowser.open_new_tab(url)
    except Exception:
        pass

# --- DICTIONNAIRE DES TRADUCTIONS ---
LANGUAGES = {
    "en": {
        "title": "VRAmax PRO - Headset Performance Software",
        "dir_label": "Meta Horizon CLI Location: ",
        "dir_sub": "Oculus Debug Tool",
        "browse": "Browse",
        "folder": "Folder",
        "loaded": "Loaded",
        "prof_title": "1. Hardware Performance Profiles",
        "prof_ext": "Extreme Profile (RTX 5080 / 5090 / 4090)",
        "prof_high": "High Profile (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Medium Profile (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Custom Setup",
        "var_title": "2. Variable Tweaking\nin Oculus Debug Tool",
        "game_title": "3. OpenXR Tool Kit Settings",
        "game_btn": "INJECT in openXR",
        "lbl_over": "Pixels Per Display Override :",
        "lbl_fov": "FOV Tangent Multiplier - Edge Masking :",
        "lbl_codec": "Video Codec :",
        "lbl_bit": "Constant Video Bitrate - Mbps :",
        "sharpness": "Sharpness :",
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
        "oxrtk_missing": "[OXRTK: Missing]",
        "err_cli": "Error: OculusDebugToolCLI.exe path is incorrect!",
        "err_dll": "Error: openvr_api_opencomposite.dll not found!",
        "err_game_folder": "Please select a game folder first.",
        "err_openvr_missing": "Error: openvr_api.dll not found in this game tree!",
        "err_game_exe_missing": "Warning: game exe not found. LibOVRRT64_1.dll was copied to the selected root folder.",
        "succ_inject": "Oculus Debug Tool variables injected successfully!",
        "succ_game": "Injection OK !",
        "tuto_title": "Setup Guide & Prerequisites",
        "tuto_prereq_title": "Prerequisites & Recommendations",
        "tuto_prereq_text": "Make sure Meta Link is properly installed and your headset is connected via cable. For optimal simracing performance with high bitrates, ensure your graphics drivers are up to date.",
        "tuto_step1_title": "Step 1: Meta Link Settings",
        "tuto_step1_text": "In the Meta Horizon application, go to Devices -> Quest 3 -> Graphics Preferences. Set the refresh rate to 90 Hz and push the render resolution slider to match the maximum native resolution as shown in the reference image above.",
        "tuto_step2_title": "Step 2: OpenXR Toolkit Integration",
        "tuto_step2_text": "OpenXR Toolkit enhances sharpness and scaling (FSR/NIS/CAS). Use the companion app to verify your runtime is correctly set to active.",
        "tuto_step3_title": "Step 3: OpenComposite Runtime Switch",
        "tuto_step3_text": "OpenComposite bypasses SteamVR entirely to run games directly through OpenXR, drastically reducing CPU overhead and micro-stutters in Automobilista 2 and iRacing.",
        "tuto_tip_title": "Pro Tip for Simracers",
        "tuto_tip_text": "Always launch VRAmax PRO and apply your configurations before starting your racing simulation for the best results.",
    },
    "fr": {
        "title": "VRAmax PRO - Logiciel de Performance Casque",
        "dir_label": "Emplacement du CLI Meta Horizon : ",
        "dir_sub": "Oculus Debug Tool",
        "browse": "Parcourir",
        "folder": "Dossier",
        "loaded": "Chargé",
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
        "lbl_codec": "Codec Vidéo :",
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
        "succ_inject": "Injection des variables dans Oculus Debug Tool succès !",
        "succ_game": "Injection OK !",
        "tuto_title": "Guide d'installation & prérequis",
        "tuto_prereq_title": "Prérequis & Recommandations",
        "tuto_prereq_text": "Assurez-vous que Meta Link est correctement installé et que votre casque est connecté en lien filaire. Pour des performances optimales en simracing avec un débit élevé, vérifiez que vos pilotes graphiques sont à jour.",
        "tuto_step1_title": "Étape 1 : Paramètres Meta Link",
        "tuto_step1_text": "Dans l'application Meta Horizon, allez dans Appareils -> Quest 3 -> Préférences graphiques. Fixez le taux de rafraîchissement à 90 Hz et poussez le curseur de résolution de rendu au maximum natif comme indiqué sur l'image de référence ci-dessus.",
        "tuto_step2_title": "Étape 2 : Intégration OpenXR Toolkit",
        "tuto_step2_text": "OpenXR Toolkit améliore la netteté et gère la mise à l'échelle (FSR/NIS/CAS). Utilisez l'application compagnon pour vérifier que votre runtime principal est bien défini.",
        "tuto_step3_title": "Étape 3 : Bascule Runtime OpenComposite",
        "tuto_step3_text": "OpenComposite contourne entièrement SteamVR pour exécuter les jeux directement via OpenXR, réduisant drastiquement la charge CPU et les micro-saccades sur Automobilista 2 et iRacing.",
        "tuto_tip_title": "Astuce Simracing",
        "tuto_tip_text": "Lancez toujours VRAmax PRO et appliquez vos configurations avant de démarrer votre simulation de course pour un résultat optimal.",
    },
    "de": {
        "title": "VRAmax PRO - Headset-Leistungssoftware",
        "dir_label": "Meta Horizon CLI Speicherort: ",
        "dir_sub": "Oculus Debug Tool",
        "browse": "Durchsuchen",
        "folder": "Ordner",
        "loaded": "Geladen",
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
        "lbl_codec": "Video-Codec:",
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
        "succ_inject": "Variablen erfolgreich injiziert!",
        "succ_game": "Injektion OK!",
        "tuto_title": "Installationsanleitung & Voraussetzungen",
        "tuto_prereq_title": "Voraussetzungen",
        "tuto_prereq_text": "Stellen Sie sicher, dass Meta Link installiert ist.",
        "tuto_step1_title": "Schritt 1: Meta Link Einstellungen",
        "tuto_step1_text": "Stellen Sie die Auflösung und Bildwiederholrate ein.",
        "tuto_step2_title": "Schritt 2: OpenXR Toolkit",
        "tuto_step2_text": "Verwenden Sie OpenXR Toolkit für Skalierung.",
        "tuto_step3_title": "Schritt 3: OpenComposite",
        "tuto_step3_text": "OpenComposite umgeht SteamVR.",
        "tuto_tip_title": "Tipp",
        "tuto_tip_text": "Starten Sie VRAmax vor dem Spiel.",
    },
    "es": {
        "title": "VRAmax PRO - Rendimiento del visor",
        "dir_label": "Ubicación de Meta Horizon CLI: ",
        "dir_sub": "Oculus Debug Tool",
        "browse": "Examinar",
        "folder": "Carpeta",
        "loaded": "Cargado",
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
        "lbl_codec": "Códec de vídeo:",
        "lbl_bit": "Bitrate de vídeo - Mbps:",
        "sharpness": "Nitidez:",
        "status_ready": "Listo.",
        "btn_inject": "INYECTAR CONFIGURACIÓN VR",
        "btn_odt": "Abrir Oculus Debug Tool",
        "btn_tuto": "Guía y requisitos",
        "btn_paypal": "Apoyar VRAmax",
        "btn_add_game": "Añadir juego",
        "new_game_name": "Nombre:",
        "new_game_exe": "Exe du jeu:",
        "select_game_exe": "Seleccionar exe",
        "game_added": "Añadido:",
        "oxrtk_ok": "",
        "oxrtk_missing": "[OXRTK: No detectado]",
        "err_cli": "Error: ¡Ruta de CLI incorrecta!",
        "err_dll": "Error: ¡openvr_api_opencomposite.dll no encontrada!",
        "err_game_folder": "Selecciona una carpeta primero.",
        "err_openvr_missing": "Error: ¡openvr_api.dll no encontrada en el juego!",
        "err_game_exe_missing": "Aviso: Exe no encontrado. LibOVRRT64_1 copiada.",
        "succ_inject": "¡Variables inyectadas correctamente!",
        "succ_game": "¡Inyección OK!",
        "tuto_title": "Guía y requisitos",
        "tuto_prereq_title": "Requisitos previos",
        "tuto_prereq_text": "Asegúrate de que Meta Link esté instalado.",
        "tuto_step1_title": "Paso 1: Ajustes de Meta Link",
        "tuto_step1_text": "Configura la resolución y tasa de refresco.",
        "tuto_step2_title": "Paso 2: OpenXR Toolkit",
        "tuto_step2_text": "Mejora la nitidez con OpenXR Toolkit.",
        "tuto_step3_title": "Paso 3: OpenComposite",
        "tuto_step3_text": "OpenComposite omite SteamVR.",
        "tuto_tip_title": "Consejo",
        "tuto_tip_text": "Inicia VRAmax antes de jugar.",
    },
}

ctk.set_appearance_mode("Dark")

class VRAMaxApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # On réduit légèrement la hauteur par défaut pour qu'elle s'adapte mieux aux écrans
        self.geometry("600x900")
        self.resizable(True, True)  # Permet à l'utilisateur de redimensionner la fenêtre si besoin
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

        # --- CONTENEUR PRINCIPAL DÉFILANT (SCROLLABLE FRAME) ---
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG_DARK, corner_radius=0)
        self.main_scroll.pack(fill="both", expand=True)

        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.header_frame.pack(pady=(15, 5), fill="x", padx=30)

        self.logo_path = ressource_path("logo_visuel.png")
        try:
            pil_logo = Image.open(self.logo_path)
            self.img_data_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(200, 200))
            self.logo_label = ctk.CTkLabel(self.header_frame, text="", image=self.img_data_logo)
            self.logo_label.pack(side="left")
        except Exception:
            self.logo_label = ctk.CTkLabel(self.header_frame, text="VRAmax PRO", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_CYAN)
            self.logo_label.pack(side="left")

        self.right_header = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.right_header.pack(side="right", fill="y", expand=True)

        self.lang_frame = ctk.CTkFrame(self.right_header, fg_color="transparent")
        self.lang_frame.pack(anchor="ne", pady=(0, 10))

        for lang in ["en", "fr", "de", "es"]:
            btn = ctk.CTkButton(self.lang_frame, text=lang.upper(), width=30, height=24, fg_color=COLOR_FRAME, hover_color=COLOR_BLUE_TECH, command=lambda l=lang: self.change_language(l))
            btn.pack(side="left", padx=2)

        self.btn_donate = ctk.CTkButton(self.right_header, text="Soutenir VRAmax", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#0079C1", height=32, command=lambda: open_url("https://paypal.me/PCVRAmax"))
        self.btn_donate.pack(anchor="ne", pady=(5, 5))

        self.btn_tuto = ctk.CTkButton(self.right_header, text="Guide d'installation & prérequis", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#2A9D8F", hover_color="#1E6B62", text_color="#FFFFFF", height=32, command=self.open_tutorial_window)
        self.btn_tuto.pack(anchor="ne", pady=(5, 5))

        self.lbl_version = ctk.CTkLabel(self.right_header, text="VRAmax PRO V3.0", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_CYAN)
        self.lbl_version.pack(anchor="ne", pady=(5, 0))

        # --- DIR FRAME ---
        self.dir_frame = ctk.CTkFrame(self.main_scroll, fg_color=COLOR_FRAME, border_color=COLOR_BLUE_TECH, border_width=1)
        self.dir_frame.pack(pady=5, fill="x", padx=30)

        self.dir_title_frame = ctk.CTkFrame(self.dir_frame, fg_color="transparent")
        self.dir_title_frame.pack(anchor="w", padx=15, pady=(5, 0))
        self.dir_title = ctk.CTkLabel(self.dir_title_frame, text="Emplacement du CLI Meta Horizon : ", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_CYAN)
        self.dir_title.pack(side="left")
        self.dir_subtitle = ctk.CTkLabel(self.dir_title_frame, text="Oculus Debug Tool", font=ctk.CTkFont(size=12), text_color="gray")
        self.dir_subtitle.pack(side="left")

        self.dir_sub_frame = ctk.CTkFrame(self.dir_frame, fg_color="transparent")
        self.dir_sub_frame.pack(fill="x", padx=15, pady=(2, 8))

        self.entry_dir = ctk.CTkEntry(self.dir_sub_frame, fg_color=COLOR_BG_DARK, border_color=COLOR_BLUE_TECH)
        self.entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_dir.insert(0, self.cli_path)
        self.entry_dir.bind("<KeyRelease>", lambda e: self.save_user_config())

        self.btn_browse = ctk.CTkButton(self.dir_sub_frame, text="Parcourir", width=80, fg_color=COLOR_BLUE_TECH, command=self.browse_directory)
        self.btn_browse.pack(side="right")

        # --- SECTION 1: PROFILES ---
        self.profile_frame = ctk.CTkFrame(self.main_scroll, fg_color=COLOR_FRAME, border_color=COLOR_BLUE_TECH, border_width=1)
        self.profile_frame.pack(pady=5, fill="x", padx=30)

        self.profile_title = ctk.CTkLabel(self.profile_frame, text="1. Profils de Performance Matérielle", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_CYAN)
        self.profile_title.pack(pady=5)

        self.profile_var = ctk.StringVar(value="extreme")

        for val in ["extreme", "high", "mid", "custom"]:
            rad = ctk.CTkRadioButton(self.profile_frame, text="", variable=self.profile_var, value=val, fg_color=COLOR_CYAN, command=self.update_inputs_by_profile)
            rad.pack(anchor="w", padx=25, pady=2)
            setattr(self, f"radio_{val}", rad)

        # --- SECTION 2: VARIABLES (ODT) ---
        self.param_frame = ctk.CTkFrame(self.main_scroll, fg_color=COLOR_FRAME, border_color=COLOR_BLUE_TECH, border_width=1)
        self.param_frame.pack(pady=5, fill="x", padx=30)

        self.param_title_frame = ctk.CTkFrame(self.param_frame, fg_color="transparent")
        self.param_title_frame.pack(pady=(5, 10))
        
        self.param_title = ctk.CTkLabel(self.param_title_frame, text="2. Ajustement des Variables\ndans Oculus Debug Tool", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_CYAN, justify="center")
        self.param_title.pack(side="left", padx=(0, 10))
        
        oculus_path = ressource_path("oculus.png")
        if os.path.exists(oculus_path):
            try:
                img_oc = ctk.CTkImage(Image.open(oculus_path), size=(50, 50))
                ctk.CTkLabel(self.param_title_frame, text="", image=img_oc).pack(side="left")
            except Exception:
                pass

        self.label_override = ctk.CTkLabel(self.param_frame, text="Pixels Per Display Override :", text_color="#FFFFFF")
        self.label_override.pack(anchor="w", padx=25)
        self.entry_override = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK)
        self.entry_override.pack(fill="x", padx=25, pady=2)
        self.entry_override.bind("<KeyRelease>", self.detect_manual_modification)

        self.label_fov = ctk.CTkLabel(self.param_frame, text="FOV Tangent Multiplier - Masquage :", text_color="#FFFFFF")
        self.label_fov.pack(anchor="w", padx=25)
        self.entry_fov = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK)
        self.entry_fov.pack(fill="x", padx=25, pady=2)
        self.entry_fov.bind("<KeyRelease>", self.detect_manual_modification)

        self.label_codec = ctk.CTkLabel(self.param_frame, text="Codec Vidéo :", text_color="#FFFFFF")
        self.label_codec.pack(anchor="w", padx=25)
        self.codec_var = ctk.StringVar(value="H.264")
        self.codec_dropdown = ctk.CTkOptionMenu(
            self.param_frame, variable=self.codec_var, values=["H.264", "H.265"],
            fg_color=COLOR_BG_DARK, button_color=COLOR_BLUE_TECH, command=lambda e: self.save_user_config()
        )
        self.codec_dropdown.pack(fill="x", padx=25, pady=2)

        self.label_bitrate = ctk.CTkLabel(self.param_frame, text="Débit Vidéo Constant - Mbps :", text_color="#FFFFFF")
        self.label_bitrate.pack(anchor="w", padx=25)
        self.entry_bitrate = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK)
        self.entry_bitrate.pack(fill="x", padx=25, pady=2)
        self.entry_bitrate.bind("<KeyRelease>", self.detect_manual_modification)

        self.status_label_odt = ctk.CTkLabel(self.param_frame, text="", text_color="#00FF00", font=ctk.CTkFont(weight="bold"))
        self.status_label_odt.pack(pady=(10, 5))

        self.btn_row_frame = ctk.CTkFrame(self.param_frame, fg_color="transparent")
        self.btn_row_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.btn_apply = ctk.CTkButton(self.btn_row_frame, text="INJECTER LA CONFIGURATION VR", fg_color=COLOR_BLUE_TECH, height=35, command=self.apply_settings)
        self.btn_apply.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_odt = ctk.CTkButton(self.btn_row_frame, text="Ouvrir Oculus Debug Tool", fg_color="#4E5D6C", width=160, height=35, command=self.open_oculus_debug_tool)
        self.btn_odt.pack(side="right")

        # --- SECTION 3: OPENCOMPOSITE & OXRTK ---
        self.game_frame = ctk.CTkFrame(self.main_scroll, fg_color=COLOR_FRAME, border_color=COLOR_AMBER, border_width=1)
        self.game_frame.pack(pady=(5, 20), fill="x", padx=30)

        self.game_title_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.game_title_frame.pack(pady=5)
        
        self.game_title = ctk.CTkLabel(self.game_title_frame, text="3. Paramètres OpenXR Tool Kit", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_AMBER)
        self.game_title.pack(side="left", padx=10)
        
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
            self.game_sub_frame, variable=self.game_var, values=list(self.games.keys()),
            fg_color=COLOR_BG_DARK, button_color=COLOR_AMBER, command=lambda e: self.on_game_changed()
        )
        self.game_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_browse_game = ctk.CTkButton(self.game_sub_frame, text="Chargé", width=80, fg_color=COLOR_BLUE_TECH, command=self.browse_game_dir)
        self.btn_browse_game.pack(side="right")

        self.btn_add_game = ctk.CTkButton(self.game_frame, text="Ajouter un jeu", width=140, fg_color=COLOR_BLUE_TECH, command=self.open_add_game_window)
        self.btn_add_game.pack(pady=(0, 8))

        self.oxr_config_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.oxr_config_frame.pack(fill="x", padx=15, pady=(5, 5))

        self.oxr_mode_var = ctk.StringVar(value="cas")
        self.oxr_mode_dropdown = ctk.CTkOptionMenu(
            self.oxr_config_frame, variable=self.oxr_mode_var, values=["cas", "fsr", "nis"],
            width=70, fg_color=COLOR_BG_DARK, command=lambda e: self.save_user_config()
        )
        self.oxr_mode_dropdown.pack(side="left", padx=(0, 10))

        self.lbl_sharpness = ctk.CTkLabel(self.oxr_config_frame, text="Netteté :", text_color="#FFFFFF")
        self.lbl_sharpness.pack(side="left", padx=(0, 5))

        self.oxr_sharpness_var = ctk.IntVar(value=73)
        self.oxr_sharpness_slider = ctk.CTkSlider(
            self.oxr_config_frame, variable=self.oxr_sharpness_var, from_=0, to=100,
            number_of_steps=100, width=100, command=lambda e: self.save_user_config()
        )
        self.oxr_sharpness_slider.pack(side="left", padx=(0, 5))

        self.lbl_sharpness_val = ctk.CTkLabel(self.oxr_config_frame, textvariable=self.oxr_sharpness_var, text_color=COLOR_CYAN, width=30)
        self.lbl_sharpness_val.pack(side="left")

        self.btn_inject_game = ctk.CTkButton(self.oxr_config_frame, text="INJECTER dans openXR", fg_color="#E07A5F", hover_color="#C06048", width=140, command=self.inject_game_mods)
        self.btn_inject_game.pack(side="right")
        
        self.status_label_oxr = ctk.CTkLabel(self.game_frame, text="", text_color="#00FF00", font=ctk.CTkFont(weight="bold"))
        self.status_label_oxr.pack(anchor="e", padx=20, pady=(0, 5))

        self.load_user_config()
        self.change_language(self.current_lang, save=False)

    def find_oculus_cli(self):
        default_path = r"C:\Program Files\Meta Horizon\Support\oculus-diagnostics\OculusDebugToolCLI.exe"
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Oculus VR, LLC\Oculus", 0, winreg.KEY_READ)
            base_folder, _ = winreg.QueryValueEx(reg_key, "BaseFolder")
            winreg.CloseKey(reg_key)
            dynamic_path = os.path.join(base_folder, "Support", "oculus-diagnostics", "OculusDebugToolCLI.exe")
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
        self.dir_subtitle.configure(text=t["dir_sub"])
        self.btn_browse.configure(text=t["browse"])

        self.profile_title.configure(text=t["prof_title"])
        self.radio_extreme.configure(text=t["prof_ext"])
        self.radio_high.configure(text=t["prof_high"])
        self.radio_mid.configure(text=t["prof_mid"])
        self.radio_custom.configure(text=t["prof_cust"])

        self.param_title.configure(text=t["var_title"])
        self.label_override.configure(text=t["lbl_over"])
        self.label_fov.configure(text=t["lbl_fov"])
        self.label_codec.configure(text=t["lbl_codec"])
        self.label_bitrate.configure(text=t["lbl_bit"])

        self.game_title.configure(text=t["game_title"])

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
            self.status_label_oxr.configure(text=f'{t["folder_status"]}: {os.path.basename(directory)}', text_color=COLOR_CYAN)
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
            self.codec_var.set("H.264")
            self.entry_bitrate.insert(0, "800")
        elif profile == "high":
            self.entry_override.insert(0, "1.1")
            self.entry_fov.insert(0, "0.75")
            self.codec_var.set("H.264")
            self.entry_bitrate.insert(0, "600")
        elif profile == "mid":
            self.entry_override.insert(0, "0.0")
            self.entry_fov.insert(0, "0.75")
            self.codec_var.set("H.265")
            self.entry_bitrate.insert(0, "500")
        self.save_user_config()

    def detect_manual_modification(self, event):
        if self.profile_var.get() != "custom":
            self.profile_var.set("custom")
        self.save_user_config()

    def save_user_config(self):
        try:
            custom_games = {name: data for name, data in self.games.items() if name not in DEFAULT_GAMES}
            default_game_roots = {name: data.get("root", "") for name, data in self.games.items() if name in DEFAULT_GAMES}
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(f"language={self.current_lang}\n")
                f.write(f"profile={self.profile_var.get()}\n")
                f.write(f"override={self.entry_override.get()}\n")
                f.write(f"fov={self.entry_fov.get()}\n")
                f.write(f"codec={self.codec_var.get()}\n")
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
                self.codec_var.set(config.get("codec", "H.264"))
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

        ctk.CTkLabel(win, text=t["new_game_name"], text_color=COLOR_CYAN, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        entry_name = ctk.CTkEntry(win, textvariable=name_var, fg_color=COLOR_FRAME)
        entry_name.pack(fill="x", padx=20)

        ctk.CTkLabel(win, text=t["new_game_exe"], text_color=COLOR_CYAN, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        exe_frame = ctk.CTkFrame(win, fg_color="transparent")
        exe_frame.pack(fill="x", padx=20)
        entry_exe = ctk.CTkEntry(exe_frame, textvariable=exe_var, fg_color=COLOR_FRAME)
        entry_exe.pack(side="left", fill="x", expand=True, padx=(0, 5))

        def browse_exe():
            file = filedialog.askopenfilename(title=t["select_game_exe"], filetypes=[("Executable", "*.exe"), ("All files", "*.*")])
            if file:
                exe_var.set(os.path.normpath(file))
                if not name_var.get().strip():
                    name_var.set(os.path.splitext(os.path.basename(file))[0])

        ctk.CTkButton(exe_frame, text=t["browse"], width=100, fg_color=COLOR_BLUE_TECH, command=browse_exe).pack(side="right")

        def add_game():
            name = name_var.get().strip()
            exe_path = exe_var.get().strip()
            if not name or not os.path.exists(exe_path):
                return
            game_root = os.path.dirname(exe_path)
            self.games[name] = {"exe": os.path.basename(exe_path), "root": game_root, "dll": "openvr_api.dll"}
            self.refresh_game_dropdown()
            self.game_var.set(name)
            self.selected_game_dir = game_root
            self.btn_browse_game.configure(text=t["loaded"])
            self.status_label_oxr.configure(text=f'{t["game_added"]} {name}', text_color=COLOR_CYAN)
            self.save_user_config()
            win.destroy()

        ctk.CTkButton(win, text=t["btn_add_game"], fg_color=COLOR_AMBER, hover_color="#C06048", command=add_game).pack(pady=25)

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

        process_name = os.path.splitext(exe_name)[0]
        reg_path = rf"Software\OpenXR_Toolkit\OpenComposite_{process_name}"
        mode_map = {"nis": 1, "fsr": 2, "cas": 3}
        mode_val = mode_map.get(self.oxr_mode_var.get(), 3)
        sharpness_val = self.oxr_sharpness_var.get()

        try:
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
            winreg.SetValueEx(reg_key, "scaling_type", 0, winreg.REG_DWORD, mode_val)
            winreg.SetValueEx(reg_key, "sharpness", 0, winreg.REG_DWORD, sharpness_val)
            winreg.SetValueEx(reg_key, "enabled", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(reg_key)

            if exe_path:
                self.status_label_oxr.configure(text=t["succ_game"], text_color="#00FF00")
            else:
                self.status_label_oxr.configure(text=t["succ_game"], text_color="#00FF00")
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

        os.system("taskkill /f /im OculusDebugTool.exe >nul 2>&1")

        cli_commands = f"service set-pixels-per-display-pixel-override {self.entry_override.get()}\n"
        cli_commands += f"service set-client-fov-tan-angle-multiplier {self.entry_fov.get()} {self.entry_fov.get()}\n"
        cli_commands += "server:asw.Off\n"
        cli_commands += "service set-use-fov-stencil Off\n"
        cli_commands += "service set-force-mip-gen-on-all-layers Off\n"
        cli_commands += "service enable-adaptive-gpu-perf-scale Off\n"
        cli_commands += "exit\n"

        try:
            process = subprocess.Popen(
                [self.entry_dir.get().strip()],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            process.communicate(input=cli_commands)
            
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Oculus\RemoteHeadset")
            
            codec_val = 1 if self.codec_var.get() == "H.265" else 0
            winreg.SetValueEx(reg_key, "HEVC", 0, winreg.REG_DWORD, codec_val)
            winreg.SetValueEx(reg_key, "DistortionCurve", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "DistortionCurvature", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "SlicedEncoding", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "EncodeWidth", 0, winreg.REG_DWORD, 4128)
            winreg.SetValueEx(reg_key, "ResolutionWidth", 0, winreg.REG_DWORD, 4128)
            winreg.SetValueEx(reg_key, "DBR", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "BitrateMax", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "BitrateMbps", 0, winreg.REG_DWORD, bitrate)
            winreg.SetValueEx(reg_key, "DBROffset", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "LinkSharpening", 0, winreg.REG_DWORD, 3)
            winreg.SetValueEx(reg_key, "LinkSharpeningEnabled", 0, winreg.REG_DWORD, 3)
            winreg.SetValueEx(reg_key, "LocalDimming", 0, winreg.REG_DWORD, 1)
            
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

        scroll_frame = ctk.CTkScrollableFrame(self.tuto_win, fg_color=COLOR_FRAME, border_color=COLOR_BLUE_TECH, border_width=1)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        components_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        components_frame.pack(fill="x", pady=10, padx=10)

        img_size = (35, 35)
        ctk_img1, ctk_img2, ctk_img3 = None, None, None
        try:
            if os.path.exists(ressource_path("1_2.jpg")): ctk_img1 = ctk.CTkImage(Image.open(ressource_path("1_2.jpg")), size=img_size)
            if os.path.exists(ressource_path("2_2.jpg")): ctk_img2 = ctk.CTkImage(Image.open(ressource_path("2_2.jpg")), size=img_size)
            if os.path.exists(ressource_path("3_2.jpg")): ctk_img3 = ctk.CTkImage(Image.open(ressource_path("3_2.jpg")), size=img_size)
        except Exception:
            pass

        row1 = ctk.CTkFrame(components_frame, fg_color="transparent")
        row1.pack(fill="x", pady=8)
        if ctk_img1: ctk.CTkLabel(row1, text="", image=ctk_img1).pack(side="left", padx=(0, 10))
        link_installed = os.path.exists(self.entry_dir.get().strip())
        ctk.CTkLabel(row1, text="Configuration Meta Link :", font=ctk.CTkFont(weight="bold"), text_color="#FFFFFF").pack(side="left", padx=5)
        ctk.CTkLabel(row1, text="OK" if link_installed else "Non détecté", font=ctk.CTkFont(weight="bold"), text_color="green" if link_installed else "red").pack(side="left", padx=10)

        row2 = ctk.CTkFrame(components_frame, fg_color="transparent")
        row2.pack(fill="x", pady=8)
        if ctk_img2: ctk.CTkLabel(row2, text="", image=ctk_img2).pack(side="left", padx=(0, 10))
        ctk.CTkButton(row2, text="Télécharger OpenXR Toolkit", fg_color="#E07A5F", hover_color="#C06048", command=lambda: open_url("https://github.com/mbucchia/OpenXR-Toolkit")).pack(side="left", padx=5)
        def open_oxrtk():
            path = r"C:\Program Files\OpenXR-Toolkit\companion.exe"
            if os.path.exists(path): subprocess.Popen([path])
            elif os.path.exists(r"C:\Program Files\OpenXR-Toolkit"): os.startfile(r"C:\Program Files\OpenXR-Toolkit")
            else:
                exe = filedialog.askopenfilename(title="Sélectionner OpenXR Toolkit Companion", filetypes=[("Executable", "*.exe")])
                if exe: subprocess.Popen([exe])
        ctk.CTkButton(row2, text="Ouvrir OpenXR Toolkit", fg_color=COLOR_BLUE_TECH, command=open_oxrtk).pack(side="left", padx=5)
        ctk.CTkLabel(row2, text="OK" if self.oxrtk_installed else "Non détecté", font=ctk.CTkFont(weight="bold"), text_color="green" if self.oxrtk_installed else "red").pack(side="left", padx=10)

        # BOUTON PATCH v1.3.8
        row_patch = ctk.CTkFrame(components_frame, fg_color="transparent")
        row_patch.pack(fill="x", pady=5)
        lbl_patch_status = ctk.CTkLabel(row_patch, text="", font=ctk.CTkFont(weight="bold"))
        
        def patch_oxr_138():
            target_dir = r"C:\Program Files\OpenXR-Toolkit"
            src_dll = ressource_path("XR_APILAYER_MBUCCHIA_toolkit.dll")
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            if os.path.exists(src_dll):
                try:
                    shutil.copyfile(src_dll, os.path.join(target_dir, "XR_APILAYER_MBUCCHIA_toolkit.dll"))
                    lbl_patch_status.configure(text="Patch v1.3.8 Appliqué avec Succès !", text_color="green")
                except Exception as e:
                    lbl_patch_status.configure(text=f"Erreur de patch : {str(e)}", text_color="red")
            else:
                lbl_patch_status.configure(text="Fichier source .dll introuvable !", text_color="red")

        btn_patch = ctk.CTkButton(row_patch, text="⚡ Patch OpenXR Toolkit vers v1.3.8", fg_color=COLOR_AMBER, hover_color="#C06048", command=patch_oxr_138)
        btn_patch.pack(side="left", padx=(45, 10))
        lbl_patch_status.pack(side="left", padx=10)

        row3 = ctk.CTkFrame(components_frame, fg_color="transparent")
        row3.pack(fill="x", pady=8)
        if ctk_img3: ctk.CTkLabel(row3, text="", image=ctk_img3).pack(side="left", padx=(0, 10))
        ctk.CTkButton(row3, text="Télécharger OpenComposite", fg_color="#E07A5F", hover_color="#C06048", command=lambda: open_url("https://znix.xyz/OpenComposite/runtimeswitcher.php?branch=openxr")).pack(side="left", padx=5)
        def open_opencomp():
            default_exe = r"C:\Program Files\OpenComposite\OpenComposite.exe"
            if self.manual_opencomposite_path and os.path.exists(self.manual_opencomposite_path):
                subprocess.Popen([self.manual_opencomposite_path])
                return
            if os.path.exists(default_exe):
                subprocess.Popen([default_exe])
            else:
                file_selected = filedialog.askopenfilename(title="Où se trouve l'exécutable OpenComposite.exe ?", filetypes=[("OpenComposite Executable", "*.exe")])
                if file_selected:
                    self.manual_opencomposite_path = os.path.normpath(file_selected)
                    self.save_user_config()
                    subprocess.Popen([self.manual_opencomposite_path])
                    lbl_oc_status.configure(text="OK", text_color="green")
        ctk.CTkButton(row3, text="Ouvrir OpenComposite", fg_color=COLOR_BLUE_TECH, command=open_opencomp).pack(side="left", padx=5)
        oc_installed = check_opencomposite_installed()
        lbl_oc_status = ctk.CTkLabel(row3, text="OK" if oc_installed else "Non détecté", font=ctk.CTkFont(weight="bold"), text_color="green" if oc_installed else "red")
        lbl_oc_status.pack(side="left", padx=10)

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

        sections = [
            (t["tuto_prereq_title"], t["tuto_prereq_text"], COLOR_CYAN),
            (t["tuto_step1_title"], t["tuto_step1_text"], COLOR_AMBER),
            (t["tuto_step2_title"], t["tuto_step2_text"], COLOR_AMBER),
            (t["tuto_step3_title"], t["tuto_step3_text"], COLOR_AMBER),
            (t["tuto_tip_title"], t["tuto_tip_text"], COLOR_CYAN),
        ]
        for title, text, color in sections:
            ctk.CTkLabel(scroll_frame, text=title, font=ctk.CTkFont(size=15, weight="bold"), text_color=color).pack(anchor="w", pady=(15, 5), padx=10)
            ctk.CTkLabel(scroll_frame, text=text, justify="left", text_color="#FFFFFF", wraplength=750).pack(anchor="w", padx=20)


if __name__ == "__main__":
    app = VRAMaxApp()
    app.mainloop()
