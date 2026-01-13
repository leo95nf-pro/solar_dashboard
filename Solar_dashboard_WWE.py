import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog, messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
import requests
from io import BytesIO
import math
import datetime
import threading
import sys
import os

# Fix per alta risoluzione su Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# --- FUNZIONE PER RISORSE EXE ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CONFIGURAZIONE ---
EARTH_SIZE = 620 
RAD = math.pi / 180

# --- DATABASE CITTÀ ---
# Puoi aggiungere tutte le città che vuoi qui!
DB_CITTA = {
    # --- Dati Originali ---
    "Roma (Italia)": (41.90, 12.49),
    "Napoli (Italia)": (40.85, 14.26),
    "Milano (Italia)": (45.46, 9.19),
    "New York (USA)": (40.71, -74.00),
    "Londra (UK)": (51.50, -0.12),
    "Parigi (Francia)": (48.85, 2.35),
    "Tokyo (Giappone)": (35.67, 139.65),
    "Sydney (Australia)": (-33.86, 151.20),
    "Quito (Ecuador)": (-0.18, -78.46),
    "Città del Capo (Sudafrica)": (-33.92, 18.42),
    "Mosca (Russia)": (55.75, 37.61),
    "Reykjavik (Islanda)": (64.14, -21.90),
    "Rio de Janeiro (Brasile)": (-22.90, -43.17),
    "Singapore": (1.35, 103.81),
    "Taipei (Taiwan)": (25.03, 121.56),
    "Los Angeles (USA)": (34.05, -118.24),

    # --- Europa ---
    "Tirana (Albania)": (41.32, 19.81),
    "Andorra la Vella (Andorra)": (42.50, 1.52),
    "Vienna (Austria)": (48.20, 16.37),
    "Bruxelles (Belgio)": (50.85, 4.35),
    "Minsk (Bielorussia)": (53.90, 27.56),
    "Sarajevo (Bosnia ed Erzegovina)": (43.85, 18.41),
    "Sofia (Bulgaria)": (42.69, 23.32),
    "Zagabria (Croazia)": (45.81, 15.98),
    "Nicosia (Cipro)": (35.18, 33.38),
    "Praga (Repubblica Ceca)": (50.07, 14.43),
    "Copenaghen (Danimarca)": (55.67, 12.56),
    "Tallinn (Estonia)": (59.43, 24.75),
    "Helsinki (Finlandia)": (60.16, 24.93),
    "Berlino (Germania)": (52.52, 13.40),
    "Atene (Grecia)": (37.98, 23.72),
    "Dublino (Irlanda)": (53.34, -6.26),
    "Pristina (Kosovo)": (42.66, 21.16),
    "Riga (Lettonia)": (56.94, 24.10),
    "Vaduz (Liechtenstein)": (47.14, 9.52),
    "Vilnius (Lituania)": (54.68, 25.27),
    "Lussemburgo (Lussemburgo)": (49.61, 6.13),
    "Skopje (Macedonia del Nord)": (41.99, 21.42),
    "La Valletta (Malta)": (35.89, 14.51),
    "Chisinau (Moldavia)": (47.01, 28.86),
    "Monaco (Monaco)": (43.73, 7.42),
    "Podgorica (Montenegro)": (42.43, 19.26),
    "Amsterdam (Paesi Bassi)": (52.36, 4.90),
    "Oslo (Norvegia)": (59.91, 10.75),
    "Varsavia (Polonia)": (52.22, 21.01),
    "Lisbona (Portogallo)": (38.72, -9.13),
    "Bucarest (Romania)": (44.42, 26.10),
    "San Marino (San Marino)": (43.93, 12.45),
    "Belgrado (Serbia)": (44.78, 20.44),
    "Bratislava (Slovacchia)": (48.14, 17.10),
    "Lubiana (Slovenia)": (46.05, 14.50),
    "Madrid (Spagna)": (40.41, -3.70),
    "Stoccolma (Svezia)": (59.32, 18.06),
    "Berna (Svizzera)": (46.94, 7.44),
    "Kiev (Ucraina)": (50.45, 30.52),
    "Budapest (Ungheria)": (47.49, 19.04),
    "Città del Vaticano (Vaticano)": (41.90, 12.45),

    # --- Asia ---
    "Kabul (Afghanistan)": (34.55, 69.20),
    "Riad (Arabia Saudita)": (24.71, 46.67),
    "Erevan (Armenia)": (40.18, 44.51),
    "Baku (Azerbaigian)": (40.40, 49.86),
    "Manama (Bahrein)": (26.22, 50.58),
    "Dacca (Bangladesh)": (23.81, 90.41),
    "Thimphu (Bhutan)": (27.47, 89.63),
    "Bandar Seri Begawan (Brunei)": (4.90, 114.93),
    "Phnom Penh (Cambogia)": (11.55, 104.92),
    "Pechino (Cina)": (39.90, 116.40),
    "Pyongyang (Corea del Nord)": (39.03, 125.76),
    "Seul (Corea del Sud)": (37.56, 126.97),
    "Abu Dhabi (Emirati Arabi Uniti)": (24.45, 54.37),
    "Manila (Filippine)": (14.59, 120.98),
    "Tbilisi (Georgia)": (41.71, 44.82),
    "Amman (Giordania)": (31.94, 35.92),
    "Nuova Delhi (India)": (28.61, 77.20),
    "Giacarta (Indonesia)": (-6.20, 106.84), # Nota: Nusantara è in costruzione, Giacarta è ancora de facto
    "Teheran (Iran)": (35.68, 51.38),
    "Baghdad (Iraq)": (33.31, 44.36),
    "Gerusalemme (Israele)": (31.76, 35.21),
    "Astana (Kazakistan)": (51.16, 71.47),
    "Bishkek (Kirghizistan)": (42.87, 74.59),
    "Kuwait City (Kuwait)": (29.37, 47.97),
    "Vientiane (Laos)": (17.97, 102.63),
    "Beirut (Libano)": (33.89, 35.50),
    "Kuala Lumpur (Malesia)": (3.13, 101.68),
    "Malé (Maldive)": (4.17, 73.50),
    "Ulan Bator (Mongolia)": (47.91, 106.91),
    "Naypyidaw (Myanmar)": (19.76, 96.07),
    "Katmandu (Nepal)": (27.71, 85.32),
    "Mascate (Oman)": (23.58, 58.40),
    "Islamabad (Pakistan)": (33.68, 73.04),
    "Doha (Qatar)": (25.28, 51.53),
    "Damasco (Siria)": (33.51, 36.29),
    "Colombo (Sri Lanka)": (6.92, 79.86), # Sri Jayawardenepura Kotte è legislativa
    "Dušanbe (Tagikistan)": (38.55, 68.77),
    "Bangkok (Thailandia)": (13.75, 100.50),
    "Dili (Timor Est)": (-8.55, 125.56),
    "Ankara (Turchia)": (39.93, 32.85),
    "Ashgabat (Turkmenistan)": (37.96, 58.32),
    "Tashkent (Uzbekistan)": (41.29, 69.24),
    "Hanoi (Vietnam)": (21.02, 105.83),
    "Sana'a (Yemen)": (15.36, 44.19),

    # --- Africa ---
    "Algeri (Algeria)": (36.75, 3.05),
    "Luanda (Angola)": (-8.83, 13.23),
    "Porto-Novo (Benin)": (6.49, 2.62),
    "Gaborone (Botswana)": (-24.62, 25.92),
    "Ouagadougou (Burkina Faso)": (12.37, -1.51),
    "Gitega (Burundi)": (-3.42, 29.92),
    "Yaoundé (Camerun)": (3.84, 11.50),
    "Praia (Capo Verde)": (14.93, -23.51),
    "N'Djamena (Ciad)": (12.13, 15.04),
    "Moroni (Comore)": (-11.71, 43.25),
    "Brazzaville (Congo)": (-4.26, 15.28),
    "Kinshasa (RD del Congo)": (-4.44, 15.26),
    "Yamoussoukro (Costa d'Avorio)": (6.82, -5.27),
    "Il Cairo (Egitto)": (30.04, 31.23),
    "Asmara (Eritrea)": (15.32, 38.92),
    "Mbabane (Eswatini)": (-26.30, 31.13),
    "Addis Abeba (Etiopia)": (9.00, 38.75),
    "Libreville (Gabon)": (0.41, 9.46),
    "Banjul (Gambia)": (13.45, -16.57),
    "Accra (Ghana)": (5.60, -0.18),
    "Gibuti (Gibuti)": (11.57, 43.14),
    "Conakry (Guinea)": (9.50, -13.69),
    "Bissau (Guinea-Bissau)": (11.86, -15.59),
    "Malabo (Guinea Equatoriale)": (3.75, 8.78),
    "Nairobi (Kenya)": (-1.29, 36.82),
    "Maseru (Lesotho)": (-29.31, 27.48),
    "Monrovia (Liberia)": (6.30, -10.79),
    "Tripoli (Libia)": (32.88, 13.19),
    "Antananarivo (Madagascar)": (-18.87, 47.50),
    "Lilongwe (Malawi)": (-13.96, 33.78),
    "Bamako (Mali)": (12.63, -8.00),
    "Rabat (Marocco)": (34.02, -6.83),
    "Nouakchott (Mauritania)": (18.07, -15.95),
    "Port Louis (Mauritius)": (-20.16, 57.50),
    "Maputo (Mozambico)": (-25.96, 32.58),
    "Windhoek (Namibia)": (-22.56, 17.06),
    "Niamey (Niger)": (13.51, 2.10),
    "Abuja (Nigeria)": (9.07, 7.39),
    "Bangui (Rep. Centrafricana)": (4.39, 18.55),
    "Kigali (Ruanda)": (-1.97, 30.10),
    "São Tomé (São Tomé e Príncipe)": (0.34, 6.73),
    "Dakar (Senegal)": (14.71, -17.46),
    "Victoria (Seychelles)": (-4.61, 55.45),
    "Freetown (Sierra Leone)": (8.46, -13.23),
    "Mogadiscio (Somalia)": (2.04, 45.31),
    "Pretoria (Sudafrica)": (-25.74, 28.22), # Amministrativa
    "Giuba (Sud Sudan)": (4.85, 31.57),
    "Khartoum (Sudan)": (15.50, 32.55),
    "Dodoma (Tanzania)": (-6.16, 35.74),
    "Lomé (Togo)": (6.13, 1.21),
    "Tunisi (Tunisia)": (36.80, 10.18),
    "Kampala (Uganda)": (0.34, 32.58),
    "Lusaka (Zambia)": (-15.38, 28.32),
    "Harare (Zimbabwe)": (-17.82, 31.05),

    # --- Nord e Centro America ---
    "Saint John's (Antigua e Barbuda)": (17.12, -61.84),
    "Nassau (Bahamas)": (25.04, -77.35),
    "Bridgetown (Barbados)": (13.11, -59.59),
    "Belmopan (Belize)": (17.25, -88.77),
    "Ottawa (Canada)": (45.42, -75.69),
    "San José (Costa Rica)": (9.92, -84.09),
    "L'Avana (Cuba)": (23.11, -82.36),
    "Roseau (Dominica)": (15.30, -61.38),
    "San Salvador (El Salvador)": (13.69, -89.19),
    "Kingston (Giamaica)": (17.97, -76.79),
    "Saint George's (Grenada)": (12.05, -61.75),
    "Città del Guatemala (Guatemala)": (14.63, -90.50),
    "Port-au-Prince (Haiti)": (18.59, -72.30),
    "Tegucigalpa (Honduras)": (14.07, -87.20),
    "Città del Messico (Messico)": (19.43, -99.13),
    "Managua (Nicaragua)": (12.11, -86.23),
    "Panama (Panama)": (8.98, -79.51),
    "Santo Domingo (Rep. Dominicana)": (18.48, -69.93),
    "Basseterre (Saint Kitts e Nevis)": (17.30, -62.71),
    "Castries (Santa Lucia)": (14.01, -60.98),
    "Kingstown (Saint Vincent e Grenadine)": (13.16, -61.22),
    "Washington D.C. (USA)": (38.90, -77.03),

    # --- Sud America ---
    "Buenos Aires (Argentina)": (-34.60, -58.38),
    "Sucre (Bolivia)": (-19.01, -65.26), # Costituzionale (La Paz è governativa)
    "La Paz (Bolivia)": (-16.48, -68.11),
    "Brasilia (Brasile)": (-15.79, -47.88),
    "Santiago (Cile)": (-33.44, -70.66),
    "Bogotà (Colombia)": (4.71, -74.07),
    "Georgetown (Guyana)": (6.80, -58.15),
    "Asunción (Paraguay)": (-25.26, -57.57),
    "Lima (Perù)": (-12.04, -77.04),
    "Paramaribo (Suriname)": (5.85, -55.20),
    "Montevideo (Uruguay)": (-34.90, -56.16),
    "Caracas (Venezuela)": (10.48, -66.90),

    # --- Oceania ---
    "Canberra (Australia)": (-35.28, 149.13),
    "Suva (Figi)": (-18.12, 178.44),
    "Tarawa Sud (Kiribati)": (1.33, 172.97),
    "Majuro (Isole Marshall)": (7.11, 171.37),
    "Palikir (Micronesia)": (6.92, 158.15),
    "Yaren (Nauru)": (-0.54, 166.91), # De facto
    "Wellington (Nuova Zelanda)": (-41.28, 174.77),
    "Ngerulmud (Palau)": (7.50, 134.62),
    "Port Moresby (Papua Nuova Guinea)": (-9.44, 147.18),
    "Apia (Samoa)": (-13.83, -171.76),
    "Honiara (Isole Salomone)": (-9.44, 159.95),
    "Nuku'alofa (Tonga)": (-21.13, -175.20),
    "Funafuti (Tuvalu)": (-8.52, 179.19),
    "Port Vila (Vanuatu)": (-17.73, 168.32)
}

EVENTI = [
    {"data": (1, 3), "nome": "Sciame Quadrantidi", "tipo": "Meteore"},
    {"data": (1, 10), "nome": "Giove all'opposizione", "tipo": "Astro"},
    {"data": (2, 17), "nome": "Eclissi Solare Anulare", "tipo": "Eclissi"},
    {"data": (2, 19), "nome": "Mercurio Elong. Est", "tipo": "Astro"},
    {"data": (3, 3), "nome": "Eclissi Lunare Totale", "tipo": "Eclissi"},
    {"data": (3, 20), "nome": "Equinozio di Primavera", "tipo": "Stagione"},
    {"data": (4, 14), "nome": "Galassia Whirlpool visibile", "tipo": "Astro"},
    {"data": (4, 22), "nome": "Sciame Liridi", "tipo": "Meteore"},
    {"data": (5, 6), "nome": "Sciame Eta Aquaridi", "tipo": "Meteore"},
    {"data": (6, 15), "nome": "Mercurio Elong. Est", "tipo": "Astro"},
    {"data": (6, 21), "nome": "Solstizio d'Estate", "tipo": "Stagione"},
    {"data": (6, 27), "nome": "Sciame Giugno Bootidi", "tipo": "Meteore"},
    {"data": (7, 7), "nome": "Nettuno retrogrado", "tipo": "Astro"},
    {"data": (8, 2), "nome": "Mercurio Elong. Ovest", "tipo": "Astro"},
    {"data": (8, 12), "nome": "Eclissi Solare Totale", "tipo": "Eclissi"},
    {"data": (8, 12), "nome": "Notte di San Lorenzo", "tipo": "Meteore"},
    {"data": (8, 28), "nome": "Eclissi Lunare Parziale", "tipo": "Eclissi"},
    {"data": (9, 22), "nome": "Equinozio d'Autunno", "tipo": "Stagione"},
    {"data": (10, 2), "nome": "Galassia Andromeda visibile", "tipo": "Astro"},
    {"data": (10, 21), "nome": "Sciame Orionidi", "tipo": "Meteore"},
    {"data": (11, 17), "nome": "Sciame Leonidi", "tipo": "Meteore"},
    {"data": (11, 27), "nome": "Venere max luminosità", "tipo": "Astro"},
    {"data": (12, 14), "nome": "Sciame Geminidi", "tipo": "Meteore"},
    {"data": (12, 21), "nome": "Solstizio d'Inverno", "tipo": "Stagione"},
]

class SolarDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar Dashboard - Worldwide Edition")
        self.root.configure(bg='#121212')
        self.root.resizable(False, False)

        # --- SYSTEM TRAY SETUP ---
        # Intercetta il click sulla "X" della finestra
        self.root.protocol('WM_DELETE_WINDOW', self.nascondi_in_tray)
        
        # Avvia l'icona della tray in un thread separato (per non bloccare la grafica)
        self.thread_tray = threading.Thread(target=self.avvia_tray_icon, daemon=True)
        self.thread_tray.start()
        # -------------------------

        try:
            icon_path = resource_path("analemma.ico") 
            root.iconbitmap(icon_path)
        except: pass

        # --- STATO INIZIALE ---
        # Impostiamo una città di default (es. la prima della lista o Roma)
        self.nome_citta_corrente = "Napoli (Italia)"
        # Recuperiamo lat/lon dal dizionario
        self.lat, self.lon = DB_CITTA[self.nome_citta_corrente]

        self.current_view_mode = "LOCAL"
        self.current_style = "learth"
        self.current_url = ""
        self.loop_id = None 
        self.timer_seconds = 600
        self.timer_job = None 

        # --- LAYOUT SINISTRO ---
        self.frame_left = tk.Frame(root, bg='#121212')
        self.frame_left.pack(side=tk.LEFT, padx=15, pady=15, anchor="n", fill='y')

        self.frame_img_container = tk.Frame(self.frame_left, bg='black', width=EARTH_SIZE, height=EARTH_SIZE)
        self.frame_img_container.pack()
        self.frame_img_container.pack_propagate(False)

        self.lbl_earth = tk.Label(self.frame_img_container, bg='black', text="")
        self.lbl_earth.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.lbl_loading = tk.Label(self.frame_img_container, text="Caricamento...", 
                                    bg='black', fg='#00CED1', font=('Verdana', 14, 'bold'))
        self.lbl_loading.place(relx=0.5, rely=0.5, anchor="center") 

        self.frame_info_under = tk.Frame(self.frame_left, bg='#121212')
        self.frame_info_under.pack(fill='x', pady=(5, 0))

        self.canvas_timer = tk.Canvas(self.frame_info_under, width=24, height=24, bg='#121212', highlightthickness=0)
        self.canvas_timer.pack(side=tk.LEFT, padx=(0, 10))

        self.lbl_view_name = tk.Label(self.frame_info_under, text="Prossimo download...", 
                                      bg='#121212', fg='#888', font=('Arial', 9))
        self.lbl_view_name.pack(side=tk.LEFT)

        self.lbl_coords = tk.Label(self.frame_left, text="", bg='#121212', fg='#555', font=('Arial', 8))
        self.lbl_coords.pack(pady=(2, 0), anchor="w")

        # Eventi
        self.lbl_event_title = tk.Label(self.frame_left, text="Prossimi eventi astronomici", 
                                        fg='#888', bg='#121212', font=('Arial', 9, 'bold'), pady=5)
        self.lbl_event_title.pack(fill='x', pady=(10,0))
        self.lbl_event_name = tk.Label(self.frame_left, text="Calcolo...", fg='#00CED1', bg='#121212', font=('Verdana', 11, 'bold'), justify="center") 
        self.lbl_event_name.pack(fill='x')
        self.lbl_event_days = tk.Label(self.frame_left, text="", fg='white', bg='#121212', font=('Arial', 10))
        self.lbl_event_days.pack(fill='x', pady=(0, 10))

        txt_credits = "Image/Data Usage: This image has been kindly placed in the\npublic domain by Fourmilab. See www.fourmilab.ch"
        self.lbl_credits = tk.Label(self.frame_left, text=txt_credits, fg='#444', bg='#121212', font=('Arial', 7), justify="center")
        self.lbl_credits.pack(side=tk.BOTTOM, pady=(30, 0), fill='x')

        # --- FRAME DESTRO ---
        self.frame_right = tk.Frame(root, bg='#121212')
        self.frame_right.pack(side=tk.RIGHT, padx=15, pady=15, fill='y')
        
        # === 1. MENU A TENDINA CITTÀ  ===
        self.lbl_ctrl_city = tk.Label(self.frame_right, text="Seleziona città", fg='#666', bg='#121212', font=('Arial', 7, 'bold'))
        self.lbl_ctrl_city.pack(anchor='w', pady=(0,2))
        
        # Creiamo una lista ordinata dei nomi per il menu
        nomi_citta = sorted(list(DB_CITTA.keys()))
        
        self.combo_citta = ttk.Combobox(self.frame_right, values=nomi_citta, state="readonly", font=('Arial', 10))
        self.combo_citta.set(self.nome_citta_corrente) # Imposta valore iniziale
        self.combo_citta.pack(fill='x', pady=(0, 5)) # Riduci pady a 5
        self.combo_citta.bind("<<ComboboxSelected>>", self.on_cambia_citta)

        # --- PULSANTE INPUT MANUALE ---
        btn_style_man = {'bg': '#222', 'fg': '#aaa', 'activebackground': '#444', 'activeforeground': 'white', 'borderwidth': 1, 'font': ('Arial', 8)}
        self.btn_manual = tk.Button(self.frame_right, text="Inserisci Coordinate Manuali...", 
                                    command=self.chiedi_coordinate_manuali, **btn_style_man)
        self.btn_manual.pack(fill='x', pady=(0, 15))
        # -------------------------------------
        
        # Colleghiamo l'evento "Selezione Cambiata" alla funzione 'cambia_citta'
        self.combo_citta.bind("<<ComboboxSelected>>", self.on_cambia_citta)

        # === 2. BOTTONI VISTA ===
        self.lbl_ctrl_view = tk.Label(self.frame_right, text="Punto di vista", fg='#666', bg='#121212', font=('Arial', 7, 'bold'))
        self.lbl_ctrl_view.pack(anchor='w', pady=(0,2))
        self.frame_btns_view = tk.Frame(self.frame_right, bg='#121212')
        self.frame_btns_view.pack(fill='x', pady=(0, 15))

        btn_style = {'bg': '#333', 'fg': 'white', 'activebackground': '#555', 'activeforeground': 'white', 'borderwidth': 0, 'font': ('Arial', 9), 'width': 9, 'pady': 5}
        self.btn_north = tk.Button(self.frame_btns_view, text="Polo Nord", command=lambda: self.imposta_visuale("NORTH"), **btn_style)
        self.btn_north.pack(side=tk.LEFT, padx=2)
        self.btn_local = tk.Button(self.frame_btns_view, text="Locale", command=lambda: self.imposta_visuale("LOCAL"), **btn_style)
        self.btn_local.pack(side=tk.LEFT, padx=2)
        self.btn_south = tk.Button(self.frame_btns_view, text="Polo Sud", command=lambda: self.imposta_visuale("SOUTH"), **btn_style)
        self.btn_south.pack(side=tk.LEFT, padx=2)

        # === 3. STILI ===
        self.lbl_ctrl_style = tk.Label(self.frame_right, text="Stile Terra", fg='#666', bg='#121212', font=('Arial', 7, 'bold'))
        self.lbl_ctrl_style.pack(anchor='w', pady=(0,2))
        self.frame_btns_style = tk.Frame(self.frame_right, bg='#121212')
        self.frame_btns_style.pack(fill='x', pady=(0, 15))

        self.btn_style_living = tk.Button(self.frame_btns_style, text="Living", command=lambda: self.cambia_stile("learth"), **btn_style)
        self.btn_style_living.pack(side=tk.LEFT, padx=2)
        self.btn_style_monthlies = tk.Button(self.frame_btns_style, text="Monthlies", command=lambda: self.cambia_stile("NASAmMM"), **btn_style)
        self.btn_style_monthlies.pack(side=tk.LEFT, padx=2)
        self.btn_style_marble = tk.Button(self.frame_btns_style, text="Marble", command=lambda: self.cambia_stile("NASA500m"), **btn_style)
        self.btn_style_marble.pack(side=tk.LEFT, padx=2)

        # === 4. CANVAS ANALEMMA ===
        # Canvas inizialmente largo, poi lo ridimensioniamo dinamicamente
        self.canvas_w = 250
        self.canvas_h = EARTH_SIZE 
        self.canvas = tk.Canvas(self.frame_right, width=self.canvas_w, height=self.canvas_h, bg='#1e1e1e', highlightthickness=0)
        self.canvas.pack()

        self.coords_analemma = []
        self.min_az = self.max_az = 0
        self.min_alt = self.max_alt = 0

        # Avvio
        self.cambia_stile("learth", aggiorna=False) 
        self.aggiorna_tutto_per_nuova_citta() # Calcola analemma e avvia
        self.imposta_visuale("LOCAL", first_run=True)

    # ---------------------------------------------------------
    # GESTIONE CAMBIO CITTÀ (NUOVO)
    # ---------------------------------------------------------
    def on_cambia_citta(self, event):
        """Chiamata quando l'utente seleziona un nome dal menu"""
        nuovo_nome = self.combo_citta.get()
        if nuovo_nome in DB_CITTA:
            self.nome_citta_corrente = nuovo_nome
            self.lat, self.lon = DB_CITTA[nuovo_nome]
            print(f"Cambio città: {nuovo_nome} ({self.lat}, {self.lon})")
            
            # Ricalcola tutto e ricarica immagine
            self.aggiorna_tutto_per_nuova_citta()
            
            # Se siamo in vista locale, forziamo il ricaricamento dell'URL
            if self.current_view_mode == "LOCAL":
                self.imposta_visuale("LOCAL")
            else:
                # Se siamo su Nord/Sud, aggiorniamo solo l'analemma a destra
                self.aggiorna_analemma_oggi()

    def aggiorna_tutto_per_nuova_citta(self):
        # 1. Ricalcola Analemma con le nuove coordinate
        self.calcola_analemma_completo()
        
        # 2. Adatta dimensione Canvas (Se Equatore -> Largo, Altrimenti -> Stretto)
        is_equatorial = abs(self.lat) < 5.0
        new_w = EARTH_SIZE if is_equatorial else 250
        new_h = 250        if is_equatorial else EARTH_SIZE
        
        # Aggiorna larghezza canvas senza distruggere tutto
        if new_w != self.canvas_w:
            self.canvas_w = new_w
            self.canvas.config(width=new_w)

            self.canvas_h = new_h
            self.canvas.config(height=new_h)
            # Dobbiamo ricalcolare la proiezione grafica dell'analemma per la nuova larghezza
            self.calcola_analemma_completo() 

        # 3. Ridisegna
        self.disegna_sfondo_analemma()
        self.aggiorna_analemma_oggi()
        
        # 4. Aggiorna etichette coordinate UI
        lat_char = "N" if self.lat >= 0 else "S"
        lon_char = "E" if self.lon >= 0 else "W"
        txt_coords = f"📍 {abs(self.lat)}°{lat_char}  {abs(self.lon)}°{lon_char}"
        self.lbl_coords.config(text=txt_coords)

    # ---------------------------------------------------------
    # GESTIONE INPUT MANUALE
    # ---------------------------------------------------------
    def chiedi_coordinate_manuali(self):
        # 1. Chiedi Latitudine
        lat = simpledialog.askfloat("Input", "Inserisci Latitudine (-90 a +90):", 
                                    minvalue=-90.0, maxvalue=90.0, parent=self.root)
        if lat is None: return # L'utente ha premuto Annulla

        # 2. Chiedi Longitudine
        lon = simpledialog.askfloat("Input", "Inserisci Longitudine (-180 a +180):", 
                                    minvalue=-180.0, maxvalue=180.0, parent=self.root)
        if lon is None: return # L'utente ha premuto Annulla

        # 3. Applica i dati
        self.lat = lat
        self.lon = lon
        
        # Crea un nome personalizzato
        self.nome_citta_corrente = f"Custom ({lat:.2f}, {lon:.2f})"
        
        # Aggiorna il menu a tendina per mostrare il valore custom
        self.combo_citta.set(self.nome_citta_corrente)
        
        # Avvia l'aggiornamento
        print(f"Input Manuale: {self.nome_citta_corrente}")
        self.aggiorna_tutto_per_nuova_citta()
        
        # Forza la visuale Locale
        self.imposta_visuale("LOCAL")

    # ---------------------------------------------------------
    # GESTIONE SYSTEM TRAY
    # ---------------------------------------------------------
    def avvia_tray_icon(self):
        # Carica l'immagine per l'icona piccola (usa la stessa dell'exe)
        try:
            image = Image.open(resource_path("analemma.ico"))
        except:
            # Fallback se non trova l'icona: crea un quadrato colorato
            image = Image.new('RGB', (64, 64), color = (0, 206, 209))

        # Definisci il menu del tasto destro
        menu = (
            item('Apri Dashboard', self.mostra_da_tray, default=True), # Default = doppio click
            item('Chiudi Definitivamente', self.esci_tutto)
        )

        self.tray_icon = pystray.Icon("SolarDashboard", image, "Solar Dashboard", menu)
        self.tray_icon.run()

    def nascondi_in_tray(self):
        """Nasconde la finestra principale ma lascia il programma attivo"""
        self.root.withdraw()  # Nasconde la finestra di Tkinter
        
        # Opzionale: Mostra una notifica (balloon) la prima volta
        # self.tray_icon.notify("Il programma è ancora attivo qui!", "Solar Dashboard")

    def mostra_da_tray(self, icon=None, item=None):
        """Riporta la finestra visibile"""
        self.root.deiconify() # Mostra la finestra
        self.root.lift()      # Portala in primo piano
        
    def esci_tutto(self, icon=None, item=None):
        """Chiude veramente tutto"""
        self.tray_icon.stop() # Ferma l'icona della tray
        self.root.quit()      # Ferma Tkinter
        self.root.destroy()   # Distrugge la finestra
        sys.exit()

    # ---------------------------------------------------------
    # GENERATORE URL
    # ---------------------------------------------------------
    def costruisci_url(self, view_mode, style):
        base = "https://www.fourmilab.ch/cgi-bin/Earth"
        params = f"?img={style}&opt=-l&dynimg=y&alt=150000000&date=0&imgsize={EARTH_SIZE}&ew=West"
        
        # Qui usiamo self.lat e self.lon invece delle vecchie costanti globali!
        dir_lat = "North" if self.lat >= 0 else "South"
        dir_lon = "East" if self.lon >= 0 else "West"
        
        if view_mode == "NORTH":
            return f"{base}{params}&ns=North&lat=90&lon=180"
        elif view_mode == "SOUTH":
            return f"{base}{params}&ns=South&lat=90&lon=0"
        elif view_mode == "LOCAL":
            return f"{base}{params}&ns={dir_lat}&ew={dir_lon}&lat={abs(self.lat)}&lon={abs(self.lon)}"
        return ""

    # ---------------------------------------------------------
    # METODI STANDARD
    # ---------------------------------------------------------
    def cambia_stile(self, nuovo_stile, aggiorna=True):
        self.current_style = nuovo_stile
        bg_inactive, fg_inactive = '#333', 'white'
        bg_active, fg_active = '#00CED1', '#121212'
        self.btn_style_living.config(bg=bg_inactive, fg=fg_inactive)
        self.btn_style_monthlies.config(bg=bg_inactive, fg=fg_inactive)
        self.btn_style_marble.config(bg=bg_inactive, fg=fg_inactive)
        
        if nuovo_stile   == "learth":    self.btn_style_living.config(bg=bg_active, fg=fg_active)
        elif nuovo_stile == "NASAmMM": self.btn_style_monthlies.config(bg=bg_active, fg=fg_active)
        elif nuovo_stile == "NASA500m":    self.btn_style_marble.config(bg=bg_active, fg=fg_active)
        
        if aggiorna:
            self.current_url = self.costruisci_url(self.current_view_mode, self.current_style)
            self.avvia_download_immagine()

    def imposta_visuale(self, modo, first_run=False):
        self.current_view_mode = modo
        bg_inactive, fg_inactive = '#333', 'white'
        bg_active, fg_active = '#00CED1', '#121212'
        self.btn_north.config(bg=bg_inactive, fg=fg_inactive)
        self.btn_local.config(bg=bg_inactive, fg=fg_inactive)
        self.btn_south.config(bg=bg_inactive, fg=fg_inactive)

        if modo == "NORTH":
            self.lbl_view_name.config(text="Prossimo download...")
            self.btn_north.config(bg=bg_active, fg=fg_active)
        elif modo == "LOCAL":
            lat_char = "N" if self.lat >= 0 else "S"
            self.lbl_view_name.config(text="Prossimo download...")
            self.btn_local.config(bg=bg_active, fg=fg_active)
        elif modo == "SOUTH":
            self.lbl_view_name.config(text="Prossimo download...")
            self.btn_south.config(bg=bg_active, fg=fg_active)

        self.current_url = self.costruisci_url(self.current_view_mode, self.current_style)
        if not first_run:
            if self.loop_id: self.root.after_cancel(self.loop_id)
            self.aggiorna_dati_loop()
        else:
            self.aggiorna_dati_loop()

    def avvia_download_immagine(self):
        self.lbl_loading.place(relx=0.5, rely=0.5, anchor="center")
        thread = threading.Thread(target=self.task_scarica_immagine, daemon=True)
        thread.start()

    def task_scarica_immagine(self):
        try:
            # Timeout impostato a 60 secondi
            risposta = requests.get(self.current_url, timeout=60)
            risposta.raise_for_status()
            img_data = BytesIO(risposta.content)
            pil_image = Image.open(img_data)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.root.after(0, self.aggiorna_immagine_gui, tk_image)
        except Exception as e:
            # INVECE DI print(e), CHIAMIAMO LA GUI
            errore_str = str(e)
            print(f"Debug (invisibile in exe): {errore_str}") 
            self.root.after(0, self.mostra_errore_gui, errore_str)

    def aggiorna_immagine_gui(self, tk_image):
        self.lbl_earth.config(image=tk_image)
        self.lbl_earth.image = tk_image
        self.lbl_loading.place_forget()

    def mostra_errore_gui(self, messaggio_errore):
        self.lbl_loading.place_forget()
        # Mostra una finestra di errore rossa
        tk.messagebox.showerror("Errore di Connessione", f"Impossibile scaricare l'immagine:\n\n{messaggio_errore}")

    def aggiorna_dati_loop(self):
        self.avvia_download_immagine()
        self.aggiorna_analemma_oggi()
        self.aggiorna_eventi()
        self.timer_seconds = 600
        if self.timer_job: self.root.after_cancel(self.timer_job)
        self.animazione_timer()
        self.loop_id = self.root.after(600000, self.aggiorna_dati_loop)

    def animazione_timer(self):
        self.canvas_timer.delete("all")
        self.canvas_timer.create_oval(2, 2, 22, 22, outline="#444", width=2)
        angle = (self.timer_seconds / 600.0) * 360
        if angle > 0:
            self.canvas_timer.create_arc(2, 2, 22, 22, start=90, extent=angle, outline="#00CED1", width=2, style="arc")
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_job = self.root.after(1000, self.animazione_timer)

    def aggiorna_analemma_oggi(self):
        self.canvas.delete("oggi")
        giorno_anno = datetime.datetime.now().timetuple().tm_yday
        idx = min(giorno_anno - 1, len(self.coords_analemma) - 1)
        if idx >= 0:
            x, y = self.coords_analemma[idx]
            r = 6
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='#FF4500', outline='white', width=2, tags="oggi")
            self.canvas.create_text(x, y-15, text="Oggi", fill='#FF4500', font=('Arial', 8, 'bold'), tags="oggi")

    def aggiorna_eventi(self):
        lista, giorni = self.trova_prossimi_eventi()
        if lista:
            data_str = lista[0]["data_obj"].strftime("%d %B")
            nomi = "\n".join([f"• {e['nome']}" for e in lista])
            if giorni == 0: txt, col = "OGGI!", "#FF4500"
            elif giorni == 1: txt, col = "Domani", "white"
            else: txt, col = f"Tra {giorni} giorni ({data_str})", "white"
            self.lbl_event_name.config(text=nomi)
            self.lbl_event_days.config(text=txt, fg=col)
        else:
            self.lbl_event_name.config(text="Nessun evento")
            self.lbl_event_days.config(text="")

    def trova_prossimi_eventi(self):
        oggi = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        anno = datetime.datetime.now().year
        candidati = []
        min_giorni = 400
        for ev in EVENTI:
            m, g = ev["data"]
            try: d_ev = datetime.datetime(anno, m, g)
            except: continue
            delta = (d_ev - oggi).days
            if delta < 0: continue
            if delta < min_giorni:
                min_giorni = delta
                c = ev.copy(); c["data_obj"] = d_ev
                candidati = [c]
            elif delta == min_giorni:
                c = ev.copy(); c["data_obj"] = d_ev
                candidati.append(c)
        return candidati, min_giorni

    def calcola_analemma_completo(self):
        self.coords_analemma = []
        azimuths = []
        altitudes = []
        
        # 1. Calcola tutti i punti grezzi
        for d in range(1, 366):
            az, alt = self.calcola_pos_solare(d)
            azimuths.append(az)
            altitudes.append(alt)
            
        # 2. MAGIC FIX: "Srotolamento" (Unwrapping) degli angoli
        # Questo rende il grafico continuo ovunque, senza bisogno di if lat < -5 etc.
        # Se c'è un salto da 359 a 1, trasforma il 359 in -1 (o viceversa) per unirli.
        for i in range(1, len(azimuths)):
            delta = azimuths[i] - azimuths[i-1]
            if delta > 180:
                azimuths[i] -= 360
            elif delta < -180:
                azimuths[i] += 360
        
        # 3. Normalizzazione e Creazione Grafica (uguale a prima)
        self.min_az, self.max_az = min(azimuths), max(azimuths)
        self.min_alt, self.max_alt = min(altitudes), max(altitudes)
        
        dx = (self.max_az - self.min_az) or 1
        dy = (self.max_alt - self.min_alt) or 1
        margin = 40 
        
        for az, alt in zip(azimuths, altitudes):
            norm_az = (az - self.min_az) / dx
            norm_alt = (alt - self.min_alt) / dy
            
            x = margin + norm_az * (self.canvas_w - 2 * margin)
            y = (self.canvas_h - margin) - norm_alt * (self.canvas_h - 2 * margin)
            
            self.coords_analemma.append((x, y))

    def calcola_pos_solare(self, day_of_year):
        B = 2 * math.pi * (day_of_year - 81) / 365
        eot = 9.87*math.sin(2*B) - 7.53*math.cos(B) - 1.5*math.sin(B)
        decl = math.asin(math.sin(23.45*RAD)*math.sin(B))
        
        meridiano_fuso = round(self.lon / 15) * 15
        lon_corr_min = (self.lon - meridiano_fuso) * 4 
        
        # --- MODIFICA ORARIO PER EQUATORE ---
        # Se siamo nella fascia tropicale (±20°), usiamo le 7:00 invece delle 12:00.
        if abs(self.lat) < 20.0:
            clock_time_h = 7.0  # Ore 07:00
        else:
            clock_time_h = 12.0  # Mezzogiorno standard
        # ------------------------------------
        
        solar_time_h = clock_time_h + (lon_corr_min + eot)/60
        
        H = (solar_time_h - 12)*15*RAD
        lat = self.lat*RAD
        sin_alt = math.sin(lat)*math.sin(decl) + math.cos(lat)*math.cos(decl)*math.cos(H)
        alt = math.asin(sin_alt)/RAD
        
        denom = (math.cos(lat)*math.cos(math.asin(sin_alt)))
        if abs(denom) < 0.0001: denom = 0.0001
        val_az = (math.sin(decl) - math.sin(lat)*sin_alt)/denom
        val_az = max(-1, min(1, val_az))
        az = math.acos(val_az)/RAD
        
        # Calcolo finale azimuth
        if math.sin(H) > 0:
            final_az = 360 - az
        else:
            final_az = az
            
        return final_az, alt

    def disegna_sfondo_analemma(self):
        self.canvas.delete("all")
        margin = 40 
        y_max = margin
        y_min = self.canvas_h - margin
        
        # Linee Min/Max
        self.canvas.create_line(margin, y_max, self.canvas_w - margin, y_max, fill='#444', dash=(4, 4), width=1)
        self.canvas.create_text(5, y_max, text=f"{self.max_alt:.1f}°", fill='#888', font=('Arial', 8), anchor="w")

        self.canvas.create_line(margin, y_min, self.canvas_w - margin, y_min, fill='#444', dash=(4, 4), width=1)
        self.canvas.create_text(5, y_min, text=f"{self.min_alt:.1f}°", fill='#888', font=('Arial', 8), anchor="w")

        # --- DISEGNO CURVA (SENZA LIMITI) ---
        # Abbiamo rimosso il controllo "if dist < 50" perché a Singapore (e ai Tropici)
        # il salto da Sud a Nord allo Zenith è reale e deve essere disegnato 
        # per chiudere la figura.
        for i in range(len(self.coords_analemma) - 1):
            x1, y1 = self.coords_analemma[i]
            x2, y2 = self.coords_analemma[i+1]
            
            # Disegna SEMPRE la linea, fidandosi della matematica "srotolata"
            self.canvas.create_line(x1, y1, x2, y2, fill='#555', width=2, smooth=True)
        
        # Etichette Assi
        cx, cy = self.canvas_w/2, self.canvas_h/2
        self.canvas.create_text(cx, self.canvas_h-10, text="Azimuth", fill='#888', font=('Arial', 8, 'bold'))
        self.canvas.create_text(10, cy, text="Altitudine", fill='#888', angle=90, font=('Arial', 8, 'bold'))

        # Pallini Mesi
        mesi = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        nomi = ['Gen','Feb','Mar','Apr','Mag','Giu','Lug','Ago','Set','Ott','Nov','Dic']
        for i, d in enumerate(mesi):
            if d < len(self.coords_analemma):
                x, y = self.coords_analemma[d]
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='#00CED1', outline='')
                offset = 15 if x < cx else -25
                self.canvas.create_text(x+offset, y, text=nomi[i], fill='#00CED1', font=('Arial', 7))

if __name__ == "__main__":
    root = tk.Tk()
    app = SolarDashboard(root)
    root.mainloop()