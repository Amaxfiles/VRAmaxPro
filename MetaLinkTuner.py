import os
import sys
import subprocess
import winreg
import webbrowser
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# --- VRAmax BRANDING COLOR PALETTE ---
COLOR_BG_DARK = "#0B132B"       
COLOR_CYAN = "#00FBEC"          
COLOR_BLUE_TECH = "#1F509E"     
COLOR_AMBER = "#FF9F29"         
COLOR_FRAME = "#1C2541"         

CONFIG_FILE = "vramax_config.txt"

def ressource_path(relative_path):
    """ Gère les chemins d'accès pour l'intégration des fichiers physiques dans l'EXE """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- DICTIONNAIRE DES TRADUCTIONS ---
LANGUAGES = {
    "en": {
        "title": "VRAmax PRO - Headset Performance Software",
        "dir_label": "Meta Horizon CLI Location :",
        "browse": "Browse",
        "prof_title": "1. Hardware Performance Profiles",
        "prof_ext": "Extreme Profile (RTX 5080 / 5090 / 4090)",
        "prof_high": "High Profile (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Medium Profile (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Custom Setup (User Saved Values)",
        "var_title": "2. Variable Tweaking",
        "lbl_over": "Pixels Per Display Override :",
        "lbl_fov": "FOV Tangent Multiplier (Edge Masking) :",
        "lbl_bit": "Constant Video Bitrate (Mbps) :",
        "status_ready": "VRAmax system ready for optimization.",
        "btn_inject": "INJECT VR CONFIGURATION",
        "btn_odt": "Open Oculus Debug Tool",
        "btn_help": "💡 VRAmax Knowledge Base & Optimization Guide",
        "btn_paypal": " Support VRAmax",
        "err_cli": "Error: OculusDebugToolCLI.exe path is incorrect!",
        "err_odt": "Failed to open ODT:",
        "err_odt_notfound": "Error: OculusDebugTool.exe not found!",
        "succ_inject": "✓ Hardware alignment successful. VRAmax configuration injected!",
        "help_title": "VRAmax Knowledge Base & Optimization Manual",
        "help_h1": "⚙️ THE QUEST LINK OPTIMIZATION ENCYCLOPEDIA",
        "help_s1": "1. TECHNICAL PARAMETERS EXPLAINED",
        "help_p1": ("• Pixels Per Display Override (Supersampling):\nDetermines the forced scale of rendering resolution. 1.0 represents native headset resolution. Setting this to 1.1 or 1.3 forces the system to calculate sub-pixels, dramatically sharpening dial textures, cockpit instruments, and distant track apex indicators.\n\n"
                    "• FOV Tangent Multiplier (Edge Masking):\nRestricts the field of view rendering calculations slightly before it reaches the outer physical edges of your visor. By dropping this value to 0.75 or 0.78, you cut out rendering elements in your extreme peripheral vision, freeing up substantial GPU compute performance without affecting immersion.\n\n"
                    "• Constant Video Bitrate (Mbps):\nForces Meta's streaming server pipeline to deliver a fixed data bandwidth. A high bitrate (600 to 800 Mbps) eradicates compressed artifact pixelation blocks and fast motion blur during intense track cornering."),
        "help_s2": "2. DEFAULT REGISTRY MODIFICATIONS",
        "help_p2": ("When clicking 'INJECT', VRAmax PRO automatically writes the following deep-level overrides directly into your Windows Registry and Meta runtime:\n\n"
                    "- ASW (Asynchronous SpaceWarp): OFF (Removes vehicle ghosting)\n"
                    "- HEVC Compression: Forced ON (0)\n"
                    "- Dynamic Bitrate (DBR): OFF (0)\n"
                    "- Encode Resolution Width: 4128\n"
                    "- Link Sharpening: Quality Mode (2)\n\n"
                    "These base settings ensure a pure 1:1 hardware performance pipeline."),
        "help_s3": "3. PREMIUM SUPPORT & QUESTIONS",
        "help_p3": ("Do you have a specific question about your hardware, simracing setup, or VR tuning?\n\n"
                    "For personalized support, please consider making a 2€ donation via the PayPal button on the main interface. Simply write your question directly inside the PayPal payment comment section, and you will receive expert guidance.")
    },
    "fr": {
        "title": "VRAmax PRO - Logiciel de Performance Casque",
        "dir_label": "Emplacement du CLI Meta Horizon :",
        "browse": "Parcourir",
        "prof_title": "1. Profils de Performance Matérielle",
        "prof_ext": "Profil Extrême (RTX 5080 / 5090 / 4090)",
        "prof_high": "Profil Haut (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Profil Moyen (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Configuration Personnalisée (Sauvegardée)",
        "var_title": "2. Ajustement des Variables",
        "lbl_over": "Pixels Per Display Override :",
        "lbl_fov": "FOV Tangent Multiplier (Masquage des bords) :",
        "lbl_bit": "Débit Vidéo Constant (Mbps) :",
        "status_ready": "Système VRAmax prêt pour l'optimisation.",
        "btn_inject": "INJECTER LA CONFIGURATION VR",
        "btn_odt": "Ouvrir Oculus Debug Tool",
        "btn_help": "💡 Base de Connaissances & Guide VRAmax",
        "btn_paypal": " Soutenir VRAmax",
        "err_cli": "Erreur : Chemin OculusDebugToolCLI.exe incorrect !",
        "err_odt": "Échec de l'ouverture de l'ODT :",
        "err_odt_notfound": "Erreur : OculusDebugTool.exe introuvable !",
        "succ_inject": "✓ Alignement matériel réussi. Configuration VRAmax injectée !",
        "help_title": "Base de Connaissances VRAmax & Manuel",
        "help_h1": "⚙️ L'ENCYCLOPÉDIE D'OPTIMISATION QUEST LINK",
        "help_s1": "1. EXPLICATION DES PARAMÈTRES TECHNIQUES",
        "help_p1": ("• Pixels Per Display Override (Supersampling) :\nDétermine l'échelle forcée de la résolution de rendu. 1.0 représente la résolution native du casque. Passer à 1.1 ou 1.3 force le système à calculer des sous-pixels, rendant les textures des cadrans, les instruments du cockpit et les points de corde lointains incroyablement nets.\n\n"
                    "• FOV Tangent Multiplier (Masquage des bords) :\nRestreint légèrement le calcul du rendu du champ de vision avant qu'il n'atteigne les bords physiques de vos lentilles. En abaissant cette valeur à 0.75 ou 0.78, vous coupez le rendu dans votre vision périphérique extrême, libérant énormément de puissance GPU sans affecter l'immersion.\n\n"
                    "• Constant Video Bitrate (Mbps) :\nForce le serveur de streaming Meta à fournir une bande passante de données fixe. Un débit élevé (600 à 800 Mbps) élimine la pixellisation et le flou de mouvement lors des virages rapides."),
        "help_s2": "2. MODIFICATIONS CACHÉES PAR DÉFAUT",
        "help_p2": ("En cliquant sur 'INJECTER', VRAmax PRO inscrit automatiquement les valeurs de pointe suivantes directement dans votre Registre Windows et dans le moteur Meta :\n\n"
                    "- ASW (Asynchronous SpaceWarp) : DÉSACTIVÉ (Supprime le ghosting)\n"
                    "- Compression HEVC : Forcée (0)\n"
                    "- Bitrate Dynamique (DBR) : DÉSACTIVÉ (0)\n"
                    "- Résolution d'encodage (Encode Resolution Width) : 4128\n"
                    "- Link Sharpening : Mode Qualité (2)\n\n"
                    "Ces paramètres garantissent un rendu 1:1 pur des performances matérielles de votre machine."),
        "help_s3": "3. SUPPORT PREMIUM & QUESTIONS",
        "help_p3": ("Vous avez une question spécifique sur votre configuration matérielle, votre setup simracing ou vos réglages VR ?\n\n"
                    "Pour obtenir un support personnalisé, merci de faire un don de 2€ via le bouton PayPal sur l'interface principale. Il vous suffit d'écrire votre question directement dans la zone de commentaire du paiement PayPal, et vous recevrez une réponse experte.")
    },
    "de": {
        "title": "VRAmax PRO - Headset Leistungssoftware",
        "dir_label": "Meta Horizon CLI Standort :",
        "browse": "Durchsuchen",
        "prof_title": "1. Hardware Leistungsprofile",
        "prof_ext": "Extremes Profil (RTX 5080 / 5090 / 4090)",
        "prof_high": "Hohes Profil (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Mittleres Profil (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Benutzerdefiniertes Setup (Gespeichert)",
        "var_title": "2. Variablenanpassung",
        "lbl_over": "Pixels Per Display Override :",
        "lbl_fov": "FOV Tangent Multiplier (Randmaskierung) :",
        "lbl_bit": "Konstante Videobitrate (Mbps) :",
        "status_ready": "VRAmax-System bereit zur Optimierung.",
        "btn_inject": "VR-KONFIGURATION INJIZIEREN",
        "btn_odt": "Oculus Debug Tool Öffnen",
        "btn_help": "💡 VRAmax Wissensdatenbank & Anleitung",
        "btn_paypal": " VRAmax Unterstützen",
        "err_cli": "Fehler: OculusDebugToolCLI.exe Pfad falsch!",
        "err_odt": "ODT konnte nicht geöffnet werden:",
        "err_odt_notfound": "Fehler: OculusDebugTool.exe nicht gefunden!",
        "succ_inject": "✓ Hardware-Ausrichtung erfolgreich. VRAmax injiziert!",
        "help_title": "VRAmax Wissensdatenbank & Handbuch",
        "help_h1": "⚙️ DIE QUEST LINK OPTIMIERUNGS-ENZYKLOPÄDIE",
        "help_s1": "1. TECHNISCHE PARAMETER ERKLÄRT",
        "help_p1": ("• Pixels Per Display Override (Supersampling):\nBestimmt den erzwungenen Maßstab der Renderauflösung. 1.0 ist die native Headset-Auflösung. Ein Wert von 1.1 oder 1.3 zwingt das System zur Berechnung von Subpixeln, was Cockpit-Instrumente und Kurvenscheitelpunkte extrem scharf macht.\n\n"
                    "• FOV Tangent Multiplier (Randmaskierung):\nBeschränkt das Sichtfeld minimal an den äußersten Rändern. Durch eine Reduzierung auf 0.75 oder 0.78 sparen Sie massiv GPU-Leistung ein, ohne die Immersion beim Fahren zu beeinträchtigen.\n\n"
                    "• Constant Video Bitrate (Mbps):\nErzwingt eine feste Datenbandbreite. Eine hohe Bitrate (600 bis 800 Mbps) verhindert Kompressionsartefakte und Bewegungsunschärfe bei schnellen Kurvenfahrten."),
        "help_s2": "2. STANDARD-REGISTRIERUNGSÄNDERUNGEN",
        "help_p2": ("Wenn Sie auf 'INJIZIEREN' klicken, schreibt VRAmax PRO automatisch die folgenden Optimierungen in die Windows-Registrierung:\n\n"
                    "- ASW (Asynchronous SpaceWarp): AUS (Entfernt Fahrzeug-Ghosting)\n"
                    "- HEVC-Kompression: Erzwungen (0)\n"
                    "- Dynamische Bitrate (DBR): AUS (0)\n"
                    "- Codierungsauflösung: 4128\n"
                    "- Link Sharpening: Qualitätsmodus (2)\n\n"
                    "Diese Einstellungen sorgen für eine unverfälschte 1:1 Hardware-Leistung."),
        "help_s3": "3. PREMIUM SUPPORT & FRAGEN",
        "help_p3": ("Haben Sie eine spezifische Frage zu Ihrer Hardware, Ihrem Simracing-Setup oder den VR-Einstellungen?\n\n"
                    "Für persönliche Unterstützung spenden Sie bitte 2€ über den PayPal-Button auf der Hauptseite. Schreiben Sie Ihre Frage einfach direkt in das Kommentarfeld der PayPal-Zahlung, und Sie erhalten fachkundige Beratung.")
    },
    "es": {
        "title": "VRAmax PRO - Software de Rendimiento",
        "dir_label": "Ubicación de Meta Horizon CLI :",
        "browse": "Examinar",
        "prof_title": "1. Perfiles de Rendimiento de Hardware",
        "prof_ext": "Perfil Extremo (RTX 5080 / 5090 / 4090)",
        "prof_high": "Perfil Alto (RTX 4080 / 4070 / 3080)",
        "prof_mid": "Perfil Medio (RTX 4060 / 3070 / 3060)",
        "prof_cust": "Configuración Personalizada",
        "var_title": "2. Ajuste de Variables",
        "lbl_over": "Pixels Per Display Override :",
        "lbl_fov": "FOV Tangent Multiplier (Enmascaramiento) :",
        "lbl_bit": "Tasa de Bits de Video Constante (Mbps) :",
        "status_ready": "Sistema VRAmax listo para optimizar.",
        "btn_inject": "INYECTAR CONFIGURACIÓN VR",
        "btn_odt": "Abrir Oculus Debug Tool",
        "btn_help": "💡 Base de Conocimientos y Guía VRAmax",
        "btn_paypal": " Apoyar a VRAmax",
        "err_cli": "Error: ¡La ruta de OculusDebugToolCLI.exe es incorrecta!",
        "err_odt": "Error al abrir ODT:",
        "err_odt_notfound": "Error: ¡OculusDebugTool.exe no encontrado!",
        "succ_inject": "✓ Alineación de hardware exitosa. ¡VRAmax inyectado!",
        "help_title": "Base de Conocimientos y Manual VRAmax",
        "help_h1": "⚙️ LA ENCICLOPEDIA DE OPTIMIZACIÓN QUEST LINK",
        "help_s1": "1. PARÁMETROS TÉCNICOS EXPLICADOS",
        "help_p1": ("• Pixels Per Display Override (Supersampling):\nDetermina la escala de la resolución de renderizado. 1.0 es la resolución nativa. Subir a 1.1 o 1.3 fuerza el cálculo de subpíxeles, enfocando dramáticamente los instrumentos del tablero y las curvas distantes.\n\n"
                    "• FOV Tangent Multiplier (Enmascaramiento):\nRestringe los cálculos de renderizado del campo de visión en los bordes físicos. Bajar este valor a 0.75 libera gran cantidad de rendimiento de la GPU sin afectar la inmersión.\n\n"
                    "• Constant Video Bitrate (Mbps):\nFuerza un ancho de banda de datos fijo. Una tasa de bits alta (600 a 800 Mbps) elimina los bloques de píxeles y el desenfoque de movimiento en las curvas rápidas."),
        "help_s2": "2. MODIFICACIONES OCULTAS POR DEFECTO",
        "help_p2": ("Al hacer clic en 'INYECTAR', VRAmax PRO escribe automáticamente los siguientes ajustes directamente en su Registro de Windows:\n\n"
                    "- ASW (Asynchronous SpaceWarp): OFF (Elimina el ghosting)\n"
                    "- Compresión HEVC: Forzada (0)\n"
                    "- Tasa de bits dinámica (DBR): OFF (0)\n"
                    "- Ancho de resolución de codificación: 4128\n"
                    "- Link Sharpening: Modo Calidad (2)\n\n"
                    "Estos ajustes garantizan un rendimiento puro de hardware 1:1."),
        "help_s3": "3. SOPORTE PREMIUM Y PREGUNTAS",
        "help_p3": ("¿Tiene alguna pregunta específica sobre su hardware, configuración de simracing o ajustes de VR?\n\n"
                    "Para obtener soporte personalizado, considere hacer una donación de 2€ a través del botón de PayPal. Simplemente escriba su pregunta directamente en la sección de comentarios de pago de PayPal, y recibirá orientación experta.")
    }
}

ctk.set_appearance_mode("Dark")

class VRAMaxApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x850")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_DARK)

        self.current_lang = "en"
        self.is_loading_config = False
        self.help_win = None

        self.cli_path = self.find_oculus_cli()

        # --- HEADER : LOGO À GAUCHE, LANGUES & PAYPAL À DROITE ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(15, 5), fill="x", padx=30)

        # Extraction du LOGO PRINCIPAL PHYSIQUE
        self.logo_path = ressource_path("logo_visuel.png")
        try:
            pil_logo = Image.open(self.logo_path)
            # /!\ MODIFIER LA TAILLE CI-DESSOUS SI LE LOGO EST COUPÉ /!\ 
            self.img_data_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(250, 250))
            self.logo_label = ctk.CTkLabel(self.header_frame, text="", image=self.img_data_logo)
            self.logo_label.pack(side="left")
        except Exception:
            self.logo_label = ctk.CTkLabel(self.header_frame, text="VRAmax PRO", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_CYAN)
            self.logo_label.pack(side="left")

        self.right_header = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.right_header.pack(side="right", fill="y", expand=True)

        # Sélection des Langues
        self.lang_frame = ctk.CTkFrame(self.right_header, fg_color="transparent")
        self.lang_frame.pack(anchor="ne", pady=(0, 15))

        btn_en = ctk.CTkButton(self.lang_frame, text="EN", width=30, height=24, fg_color=COLOR_FRAME, hover_color=COLOR_BLUE_TECH, command=lambda: self.change_language("en"))
        btn_en.pack(side="left", padx=2)
        btn_fr = ctk.CTkButton(self.lang_frame, text="FR", width=30, height=24, fg_color=COLOR_FRAME, hover_color=COLOR_BLUE_TECH, command=lambda: self.change_language("fr"))
        btn_fr.pack(side="left", padx=2)
        btn_de = ctk.CTkButton(self.lang_frame, text="DE", width=30, height=24, fg_color=COLOR_FRAME, hover_color=COLOR_BLUE_TECH, command=lambda: self.change_language("de"))
        btn_de.pack(side="left", padx=2)
        btn_es = ctk.CTkButton(self.lang_frame, text="ES", width=30, height=24, fg_color=COLOR_FRAME, hover_color=COLOR_BLUE_TECH, command=lambda: self.change_language("es"))
        btn_es.pack(side="left", padx=2)

        # Bouton PayPal avec LOGO PAYPAL PHYSIQUE
        self.btn_donate = ctk.CTkButton(self.right_header, text=" Support VRAmax", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#0079C1", hover_color="#00457C", text_color="#FFFFFF", height=32, command=self.ouvrir_paypal)
        
        self.paypal_icon_path = ressource_path("paypal_logo.png")
        try:
            pil_pay = Image.open(self.paypal_icon_path)
            # /!\ MODIFIER LA TAILLE CI-DESSOUS SI LE LOGO PAYPAL EST COUPÉ /!\ 
            self.img_data_pay = ctk.CTkImage(light_image=pil_pay, dark_image=pil_pay, size=(20, 20))
            self.btn_donate.configure(image=self.img_data_pay, compound="left")
        except Exception:
            pass
            
        self.btn_donate.pack(anchor="se")

        # --- SECTION : DIRECTORY META HORIZON ---
        self.dir_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, border_color=COLOR_BLUE_TECH, border_width=1)
        self.dir_frame.pack(pady=5, fill="x", padx=30)
        
        self.dir_title = ctk.CTkLabel(self.dir_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_CYAN)
        self.dir_title.pack(anchor="w", padx=15, pady=(5, 0))

        self.dir_sub_frame = ctk.CTkFrame(self.dir_frame, fg_color="transparent")
        self.dir_sub_frame.pack(fill="x", padx=15, pady=(2, 8))

        self.entry_dir = ctk.CTkEntry(self.dir_sub_frame, fg_color=COLOR_BG_DARK, border_color=COLOR_BLUE_TECH, font=ctk.CTkFont(size=11))
        self.entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_dir.insert(0, self.cli_path)

        self.btn_browse = ctk.CTkButton(self.dir_sub_frame, text="", width=70, fg_color=COLOR_BLUE_TECH, hover_color="#14366B", command=self.browse_directory)
        self.btn_browse.pack(side="right")

        # --- SECTION 1: HARDWARE PROFILES ---
        self.profile_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, border_color=COLOR_BLUE_TECH, border_width=1)
        self.profile_frame.pack(pady=5, fill="x", padx=30)

        self.profile_title = ctk.CTkLabel(self.profile_frame, text="", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_CYAN)
        self.profile_title.pack(pady=5)

        self.profile_var = ctk.StringVar(value="extreme")
        
        self.radio_extreme = ctk.CTkRadioButton(self.profile_frame, text="", variable=self.profile_var, value="extreme", command=self.update_inputs_by_profile, fg_color=COLOR_CYAN, hover_color=COLOR_BLUE_TECH)
        self.radio_extreme.pack(anchor="w", padx=25, pady=4)

        self.radio_high = ctk.CTkRadioButton(self.profile_frame, text="", variable=self.profile_var, value="high", command=self.update_inputs_by_profile, fg_color=COLOR_CYAN, hover_color=COLOR_BLUE_TECH)
        self.radio_high.pack(anchor="w", padx=25, pady=4)

        self.radio_mid = ctk.CTkRadioButton(self.profile_frame, text="", variable=self.profile_var, value="mid", command=self.update_inputs_by_profile, fg_color=COLOR_CYAN, hover_color=COLOR_BLUE_TECH)
        self.radio_mid.pack(anchor="w", padx=25, pady=4)

        self.radio_custom = ctk.CTkRadioButton(self.profile_frame, text="", variable=self.profile_var, value="custom", command=self.update_inputs_by_profile, fg_color=COLOR_CYAN, hover_color=COLOR_BLUE_TECH)
        self.radio_custom.pack(anchor="w", padx=25, pady=4)

        # --- SECTION 2: CUSTOM VARIABLES ---
        self.param_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, border_color=COLOR_BLUE_TECH, border_width=1)
        self.param_frame.pack(pady=5, fill="x", padx=30)

        self.param_title = ctk.CTkLabel(self.param_frame, text="", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_CYAN)
        self.param_title.pack(pady=5)

        self.label_override = ctk.CTkLabel(self.param_frame, text="", text_color="#FFFFFF", font=ctk.CTkFont(size=12))
        self.label_override.pack(anchor="w", padx=25)
        self.entry_override = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK, border_color=COLOR_BLUE_TECH)
        self.entry_override.pack(fill="x", padx=25, pady=2)
        self.entry_override.bind("<KeyRelease>", self.detect_manual_modification)

        self.label_fov = ctk.CTkLabel(self.param_frame, text="", text_color="#FFFFFF", font=ctk.CTkFont(size=12))
        self.label_fov.pack(anchor="w", padx=25)
        self.entry_fov = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK, border_color=COLOR_BLUE_TECH)
        self.entry_fov.pack(fill="x", padx=25, pady=2)
        self.entry_fov.bind("<KeyRelease>", self.detect_manual_modification)

        self.label_bitrate = ctk.CTkLabel(self.param_frame, text="", text_color="#FFFFFF", font=ctk.CTkFont(size=12))
        self.label_bitrate.pack(anchor="w", padx=25)
        self.entry_bitrate = ctk.CTkEntry(self.param_frame, fg_color=COLOR_BG_DARK, border_color=COLOR_BLUE_TECH)
        self.entry_bitrate.pack(fill="x", padx=25, pady=2)
        self.entry_bitrate.bind("<KeyRelease>", self.detect_manual_modification)

        # --- CONSOLE STATUS ---
        self.status_label = ctk.CTkLabel(self, text="", text_color=COLOR_AMBER, font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(pady=5)

        # --- SECTION BOUTONS D'ACTIONS ---
        self.btn_row_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_row_frame.pack(fill="x", padx=30, pady=2)

        self.btn_apply = ctk.CTkButton(self.btn_row_frame, text="", font=ctk.CTkFont(size=13, weight="bold"), fg_color=COLOR_BLUE_TECH, hover_color="#14366B", text_color="#FFFFFF", height=40, command=self.apply_settings)
        self.btn_apply.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_odt = ctk.CTkButton(self.btn_row_frame, text="", font=ctk.CTkFont(size=11, weight="bold"), fg_color="#4E5D6C", hover_color="#3A4652", text_color="#FFFFFF", width=160, height=40, command=self.open_oculus_debug_tool)
        self.btn_odt.pack(side="right")

        # --- BOUTON ENCYCLOPÉDIE ---
        self.btn_help_center = ctk.CTkButton(self, text="", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#2A9D8F", hover_color="#1E6B62", text_color="#FFFFFF", height=38, command=self.open_help_window)
        self.btn_help_center.pack(pady=(15, 5), fill="x", padx=30)

        self.load_user_config()
        self.change_language(self.current_lang)

    def change_language(self, lang):
        self.current_lang = lang
        t = LANGUAGES[lang]
        
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
        
        if "ready" in self.status_label.cget("text") or "prêt" in self.status_label.cget("text") or "bereit" in self.status_label.cget("text") or "listo" in self.status_label.cget("text") or self.status_label.cget("text") == "":
            self.status_label.configure(text=t["status_ready"], text_color=COLOR_AMBER)
            
        self.btn_apply.configure(text=t["btn_inject"])
        self.btn_odt.configure(text=t["btn_odt"])
        self.btn_help_center.configure(text=t["btn_help"])
        self.btn_donate.configure(text=t["btn_paypal"])

        if self.help_win is not None and self.help_win.winfo_exists():
            self.help_win.destroy()
            self.open_help_window()
            
        self.save_user_config()

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

    def browse_directory(self):
        file_selected = filedialog.askopenfilename(title="Select OculusDebugToolCLI.exe", filetypes=[("Executable Files", "OculusDebugToolCLI.exe")])
        if file_selected:
            self.cli_path = os.path.normpath(file_selected)
            self.entry_dir.delete(0, ctk.END)
            self.entry_dir.insert(0, self.cli_path)
            self.save_user_config()

    def open_oculus_debug_tool(self):
        t = LANGUAGES[self.current_lang]
        current_cli = self.entry_dir.get().strip()
        odt_folder = os.path.dirname(current_cli)
        odt_path = os.path.join(odt_folder, "OculusDebugTool.exe")
        
        if os.path.exists(odt_path):
            try:
                subprocess.Popen([odt_path])
            except Exception as e:
                self.status_label.configure(text=f'{t["err_odt"]} {str(e)}', text_color="red")
        else:
            self.status_label.configure(text=t["err_odt_notfound"], text_color="red")

    def update_inputs_by_profile(self):
        if self.is_loading_config:
            return
            
        profile = self.profile_var.get()
        if profile == "custom":
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
            with open(CONFIG_FILE, "w") as f:
                f.write(f"language={self.current_lang}\n")
                f.write(f"profile={self.profile_var.get()}\n")
                f.write(f"override={self.entry_override.get()}\n")
                f.write(f"fov={self.entry_fov.get()}\n")
                f.write(f"bitrate={self.entry_bitrate.get()}\n")
                f.write(f"path={self.entry_dir.get()}\n")
        except Exception:
            pass

    def load_user_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                self.is_loading_config = True
                config = {}
                with open(CONFIG_FILE, "r") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            config[k] = v
                
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
                
                self.is_loading_config = False
                return
            except Exception:
                self.is_loading_config = False

        self.update_inputs_by_profile()

    def ouvrir_paypal(self):
        webbrowser.open("https://paypal.me/PCVRAmax")

    def apply_settings(self):
        self.save_user_config()
        t = LANGUAGES[self.current_lang]
        override = self.entry_override.get()
        fov = self.entry_fov.get()
        bitrate = int(self.entry_bitrate.get())
        current_cli = self.entry_dir.get().strip()

        if not os.path.exists(current_cli):
            self.status_label.configure(text=t["err_cli"], text_color="red")
            return

        cli_commands = f"service set-pixels-per-display-pixel-override {override}\n"
        if fov != "0.0" and fov != "0":
            cli_commands += f"service set-client-fov-tan-angle-multiplier {fov} {fov}\n"
        cli_commands += "server:asw.Off\n"

        try:
            process = subprocess.Popen([current_cli], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.communicate(input=cli_commands)
        except Exception as e:
            self.status_label.configure(text=f"CLI Error: {str(e)}", text_color="red")
            return

        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Oculus\RemoteHeadset", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(reg_key, "HEVC", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "BitrateMbps", 0, winreg.REG_DWORD, bitrate)
            winreg.SetValueEx(reg_key, "DBR", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "ResolutionWidth", 0, winreg.REG_DWORD, 4128)
            winreg.SetValueEx(reg_key, "LinkSharpening", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(reg_key)
        except Exception as e:
            self.status_label.configure(text=f"Registry Error: {str(e)}", text_color="red")
            return

        self.status_label.configure(text=t["succ_inject"], text_color=COLOR_CYAN)

    def open_help_window(self):
        t = LANGUAGES[self.current_lang]
        
        self.help_win = ctk.CTkToplevel(self)
        self.help_win.title(t["help_title"])
        self.help_win.geometry("750x700")
        self.help_win.resizable(True, True)
        self.help_win.configure(fg_color=COLOR_BG_DARK)
        self.help_win.attributes("-topmost", True)

        scroll_frame = ctk.CTkScrollableFrame(self.help_win, fg_color=COLOR_FRAME, border_color=COLOR_BLUE_TECH, border_width=1)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(scroll_frame, text=t["help_h1"], font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_CYAN)
        title.pack(pady=(10, 15))

        sec1_title = ctk.CTkLabel(scroll_frame, text=t["help_s1"], font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_AMBER)
        sec1_title.pack(anchor="w", pady=(10, 5))

        lbl_p1 = ctk.CTkLabel(scroll_frame, text=t["help_p1"], justify="left", font=ctk.CTkFont(size=12), text_color="#FFFFFF", wraplength=660)
        lbl_p1.pack(anchor="w", padx=10, pady=5)

        sec2_title = ctk.CTkLabel(scroll_frame, text=t["help_s2"], font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_AMBER)
        sec2_title.pack(anchor="w", pady=(20, 5))

        lbl_p2 = ctk.CTkLabel(scroll_frame, text=t["help_p2"], justify="left", font=ctk.CTkFont(size=12), text_color="#FFFFFF", wraplength=660)
        lbl_p2.pack(anchor="w", padx=10, pady=5)

        sec3_title = ctk.CTkLabel(scroll_frame, text=t["help_s3"], font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_AMBER)
        sec3_title.pack(anchor="w", pady=(20, 5))

        lbl_p3 = ctk.CTkLabel(scroll_frame, text=t["help_p3"], justify="left", font=ctk.CTkFont(size=12), text_color="#FFFFFF", wraplength=660)
        lbl_p3.pack(anchor="w", padx=10, pady=5)

if __name__ == "__main__":
    app = VRAMaxApp()
    app.mainloop()
