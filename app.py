import streamlit as st
import math
import pandas as pd

# --- DATABÁZE VODIČŮ ---
WIRES = [
    (0.355, 0.400), (0.375, 0.420), (0.400, 0.445), (0.425, 0.477),
    (0.450, 0.502), (0.475, 0.527), (0.500, 0.552), (0.530, 0.590),
    (0.560, 0.620), (0.600, 0.660), (0.630, 0.690), (0.670, 0.725),
    (0.710, 0.775), (0.750, 0.825), (0.800, 0.875), (0.850, 0.925),
    (0.900, 0.975), (0.950, 1.025), (1.000, 1.075), (1.060, 1.155),
    (1.120, 1.215), (1.180, 1.275), (1.250, 1.345), (1.320, 1.415),
    (1.400, 1.495), (1.500, 1.595), (1.600, 1.695)
]

# --- DATABÁZE JADER ---
CORES = [
    {"name": "12003/0,35", "S_o": 4.44, "S_Fe": 2.0, "m": 0.2, "a": 32, "d": 20, "product": 8.88},
    {"name": "12004/0,35", "S_o": 4.44, "S_Fe": 3.0, "m": 0.3, "a": 42, "d": 20, "product": 13.32},
    {"name": "16003/0,35", "S_o": 7.68, "S_Fe": 2.0, "m": 0.23, "a": 36, "d": 20, "product": 15.36},
    {"name": "16012/0,35", "S_o": 7.68, "S_Fe": 2.5, "m": 0.32, "a": 41, "d": 20, "product": 19.2},
    {"name": "16004/0,35", "S_o": 7.68, "S_Fe": 3.0, "m": 0.4, "a": 46, "d": 20, "product": 23.04},
    {"name": "20001/0,35", "S_o": 12.0, "S_Fe": 2.0, "m": 0.3, "a": 40, "d": 20, "product": 24.0},
    {"name": "16005/0,35", "S_o": 7.68, "S_Fe": 4.0, "m": 0.55, "a": 56, "d": 20, "product": 30.72},
    {"name": "20002/0,35", "S_o": 12.0, "S_Fe": 3.0, "m": 0.45, "a": 50, "d": 20, "product": 36.0},
    {"name": "20003/0,35", "S_o": 12.0, "S_Fe": 4.0, "m": 0.65, "a": 60, "d": 20, "product": 48.0},
    {"name": "20005/0,35", "S_o": 12.0, "S_Fe": 6.0, "m": 1.0, "a": 60, "d": 30, "product": 72.0},
    {"name": "26001/0,35", "S_o": 19.76, "S_Fe": 4.5, "m": 0.85, "a": 56, "d": 30, "product": 88.92},
    {"name": "20006/0,35", "S_o": 12.0, "S_Fe": 9.0, "m": 1.7, "a": 80, "d": 30, "product": 108.0},
    {"name": "26002/0,35", "S_o": 19.76, "S_Fe": 6.0, "m": 1.2, "a": 66, "d": 30, "product": 118.56},
    {"name": "26004/0,35", "S_o": 19.76, "S_Fe": 8.0, "m": 1.6, "a": 66, "d": 40, "product": 158.08},
    {"name": "26003/0,35", "S_o": 19.76, "S_Fe": 9.0, "m": 2.0, "a": 86, "d": 30, "product": 177.84},
    {"name": "26005/0,35", "S_o": 19.76, "S_Fe": 12.0, "m": 2.6, "a": 86, "d": 40, "product": 237.12},
    {"name": "31030/0,35", "S_o": 29.14, "S_Fe": 9.0, "m": 2.3, "a": 91, "d": 30, "product": 262.26},
    {"name": "40030/0,35", "S_o": 56.0, "S_Fe": 9.0, "m": 3.0, "a": 100, "d": 30, "product": 504.0}
]

# --- PEVNÉ KONSTANTY ---
RHO_CU = 0.0178
P_FE_SPEC = 2.0
T_KOSTRICKY = 1.5
IZOL_VRSTVA_PRIM = 0.05
IZOL_VRSTVA_SEK = 0.10
IZOL_MEZI_SEKUNDARY = 0.20
K_O = 0.28  
K_FE = 0.95 

# --- LATEX TEMPLATE S PLACEHOLDERY ---
LATEX_TEMPLATE = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[czech]{babel}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{siunitx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{longtable}
\usepackage{hyperref}
\usepackage[table,xcdraw]{xcolor}
\usepackage{enumitem}

\usepackage{mathpazo} 
\usepackage{titlesec} 
\usepackage{fancyhdr} 
\usepackage[most]{tcolorbox} 

\geometry{margin=22mm, headheight=15pt}

\sisetup{
  output-decimal-marker={,},
  per-mode=symbol,
  exponent-product=\cdot,
  detect-all
}

\definecolor{primary}{RGB}{0, 75, 140} 

\titleformat{\section}{\Large\bfseries\color{primary}}{\thesection.}{1em}{}
\titleformat{\subsection}{\large\bfseries\color{primary}}{\thesubsection.}{1em}{}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{primary}\leaders\hrule height \headrulewidth\hfill}}
\renewcommand{\footrule}{\hbox to\headwidth{\color{primary}\leaders\hrule height \footrulewidth\hfill}}
\fancyhead[L]{\textcolor{gray}{\small \textit{Návrh dvousloupkového síťového transformátoru}}}
\fancyhead[R]{\textcolor{gray}{\small [AUTOR]}}
\fancyfoot[C]{\thepage}

\newtcolorbox{infobox}[1][]{
  colback=primary!4!white,
  colframe=primary,
  fonttitle=\bfseries,
  title=#1,
  arc=3pt,
  boxrule=0.8pt,
  left=6pt, right=6pt, top=4pt, bottom=4pt
}

\renewcommand{\arraystretch}{1.3}

\newcommand{\Uone}{[U1]}
\newcommand{\freq}{[FREQ]}
\newcommand{\Utwentyone}{[U21]}
\newcommand{\Itwentyone}{[I21]}
\newcommand{\Utwentytwo}{[U22]}
\newcommand{\Itwentytwo}{[I22]}

\begin{document}

\begin{titlepage}
    \centering
    \vspace*{10mm}
    
    {\Large\scshape Vyšší odborná škola a Střední průmyslová škola\\[0.3em] 
    strojní, stavební a dopravní, Děčín, p. o. \par}
    
    \vspace{20mm}

    \IfFileExists{logo-skoly.png}{%
        \includegraphics[width=0.35\textwidth]{logo-skoly.png}%
    }{%
        \fbox{\parbox[c][40mm][c]{0.35\textwidth}{\centering \textcolor{gray}{\textit{Prostor pro logo školy}}}}%
    }

    \vspace{25mm}
    
    \textcolor{primary}{\rule{\textwidth}{1.5pt}}\\[0.6cm]
    {\Huge\bfseries Seminární práce:\\[0.3em] Návrh dvousloupkového transformátoru\par}
    \vspace{0.5cm}
    \textcolor{primary}{\rule{\textwidth}{1.5pt}}
    
    \vfill

    \begin{Large}
    \begin{tabular}{>{\bfseries\color{primary}}rl}
        Vypracoval: & \textcolor{black}{[AUTOR]} \\
        Třída: & \textcolor{black}{[TRIDA]} \\
        Datum: & \textcolor{black}{[DATUM]} \\
    \end{tabular}
    \end{Large}
    \vspace*{20mm}
\end{titlepage}

\tableofcontents
\newpage

\section{Zadání}
Navrhuji jednofázový síťový transformátor pro napájení lineárního zdroje ze sítě \SI{\Uone}{V} / \SI{\freq}{Hz}. Požadované výstupní parametry jsou definovány v tabulce níže.

\begin{table}[h!]
\centering
\caption{Požadované výstupní parametry}
\begin{tabular}{cccc}
\toprule
\rowcolor{primary!10}
\textbf{Vinutí} & \textbf{Napětí $U_{2i}$ [V]} & \textbf{Proud $I_{2i}$ [A]} & \textbf{Výkon $P_{2i}$ [W]} \\
\midrule
$N_{21}$ & \num{\Utwentyone} & \num{\Itwentyone} & \num{[P21]} \\
$N_{22}$ & \num{\Utwentytwo} & \num{\Itwentytwo} & \num{[P22]} \\
\midrule
\textbf{Celkem} & -- & -- & \textbf{\SI{[P2]}{W}} \\
\bottomrule
\end{tabular}
\end{table}

\section{Konstrukce magnetického obvodu}
Zvolil jsem dvousloupkové vinuté C-jádro typu \textbf{[CORE_NAME]} z orientované oceli, které umožňuje pracovat s vyšší magnetickou indukcí $B_m = \SI{[B_M]}{T}$ při zachování nízkých ztrát v železe.

\begin{itemize}[label=\textcolor{primary}{\textbullet}]
    \item Průřez sloupku: $S_{Fe} = \SI{[S_FE]}{cm^2}$ (čtverec $[A_SLOUPEK] \times [A_SLOUPEK]$\,mm).
    \item Hmotnost jádra: $m_{Fe} = \SI{[M_FE]}{kg}$.
    \item Výška okna: $a = \SI{[A_OKNO]}{mm}$ $\implies$ navíjecí šířka $b_w = \SI{[B_W]}{mm}$ (po odečtení čel kostřičky).
\end{itemize}

Teoretický počet závitů jsem vypočítal pro $k_{Fe} = 0{,}95$:
\begin{equation*}
N_{1(teor)} = \frac{U_1 \cdot 10^4}{4{,}44 \cdot B_m \cdot f \cdot S_{Fe} \cdot k_{Fe}} = \frac{[U1] \cdot 10^4}{4{,}44 \cdot [B_M] \cdot [FREQ] \cdot [S_FE] \cdot 0{,}95} = [N1_TEOR]~\text{závitů}.
\end{equation*}

Po korekci úbytků napětí ($-5\,\%$ primár, $+5\,\%$ sekundár) vychází korigovaný počet závitů:
$N_1 = [N1]$, $N_{21} = [N21]$, $N_{22} = [N22]$.

\section{Fyzické uspořádání vinutí}
Dle zadání využívám dvě samostatné kostřičky nasazené na obou sloupcích jádra bez vnitřních přepážek. Každé vinutí využívá plnou šířku okna $b_w = \SI{[B_W]}{mm}$.

\subsection{Sloupek 1: Primární vinutí ($N_1$)}
Celé primární vinutí navíjím na první kostřičku. Při průměru drátu $d_{max} = \SI{[D1_MAX]}{mm}$ vychází:
\begin{itemize}[label=\textcolor{primary}{\textbullet}]
    \item Počet závitů na vrstvu: $[B_W] / [D1_MAX_COMMA] = [Z_V1]$.
    \item Celkový počet vrstev: $[N1] / [Z_V1] \implies [V1]$ vrstev.
    \item Tloušťka vinutí $t_{w1} = \SI{[TW1]}{mm}$. Střední délka závitu $l_{str1} = \SI{[L_STR1]}{mm}$.
\end{itemize}

\subsection{Sloupek 2: Sekundární vinutí ($N_{21}, N_{22}$)}
Na druhou kostřičku navíjím nejprve Sekundár 1 ($[U21]$\,V) a bezprostředně na něj Sekundár 2 ($[U22]$\,V).
\begin{itemize}[label=\textcolor{primary}{\textbullet}]
    \item \textbf{Sekundár 1:} $d_{max} = \SI{[D21_MAX]}{mm}$. Vejde se [Z_V21] závitů/vrstvu $\implies [V21]$ vrstvy. Tloušťka $t_{w21} = \SI{[TW21]}{mm}$, $l_{str21} = \SI{[L_STR21]}{mm}$.
    \item \textbf{Sekundár 2:} $d_{max} = \SI{[D22_MAX]}{mm}$. Vejde se [Z_V22] závitů/vrstvu $\implies [V22]$ vrstva. $l_{str22} = \SI{[L_STR22]}{mm}$.
\end{itemize}

\section{Elektrické odpory a ztráty}
Odpory vinutí jsem spočítal z exaktních délek vodičů a průřezů mědi $S = \pi \cdot d_{Cu}^2 / 4$.

\begin{align*}
R_1 &= \frac{0{,}0178 \cdot [N1] \cdot [L_STR1_COMMA] \cdot 10^{-3}}{[S1_EXAKT]} = \mathbf{[R1]\,\Omega} \\
R_{21} &= \frac{0{,}0178 \cdot [N21] \cdot [L_STR21_COMMA] \cdot 10^{-3}}{[S21_EXAKT]} = \mathbf{[R21]\,\Omega} \\
R_{22} &= \frac{0{,}0178 \cdot [N22] \cdot [L_STR22_COMMA] \cdot 10^{-3}}{[S22_EXAKT]} = \mathbf{[R22]\,\Omega}
\end{align*}

\begin{infobox}[Energetická bilance]
Celkové ztráty v mědi činí $\Delta P_{Cu} = \SI{[DP_CU]}{W}$. Ztráty v železe u orientovaných plechů pro indukci $[B_M_COMMA]\,\mathrm{T}$ odhaduji na $\Delta P_{Fe} = \SI{[DP_FE]}{W}$.
\end{infobox}

\section{Závěr}
\begin{itemize}[label=\textcolor{primary}{\textbullet}]
    \item Výstupní výkon: $P_2 = \SI{[P2]}{W}$.
    \item Celkové ztráty: $\Delta P_C = \SI{[DP_C]}{W}$.
    \item Účinnost: $\eta = \frac{[P2_COMMA]}{[P2_COMMA] + [DP_C_COMMA]} \cdot 100 \approx \mathbf{[ETA]\,\%}$.
\end{itemize}

Navržený dvousloupkový transformátor s C-jádrem splňuje všechny konstrukční a bezpečnostní požadavky při dosažení vysoké účinnosti. Rozdělení vinutí na dva sloupky zajišťuje vynikající odvod tepla a snadnou realizaci navíjení.

\end{document}"""

def get_best_wire(I, target_J):
    S_req = I / target_J
    for d_cu, d_max in WIRES:
        S_exakt = math.pi * (d_cu**2) / 4
        if S_exakt >= S_req:
            return d_cu, d_max, S_exakt
    return WIRES[-1][0], WIRES[-1][1], math.pi * (WIRES[-1][0]**2) / 4

# --- UI STREAMLIT ---
st.set_page_config(page_title="Návrh dvousloupkového trafa", layout="wide")
st.title("⚡ Návrh nf transformátoru + Generátor LaTeX protokolu")

# --- VSTUPY V POSTRANNÍM PANELU ---
st.sidebar.header("1. Parametry zadání a autor")
autor = st.sidebar.text_input("Jméno autora", value="Jan Zedník")
trida = st.sidebar.text_input("Třída", value="E3A")
datum = st.sidebar.text_input("Datum protokolu", value="11.05.2026")
st.sidebar.markdown("---")
U1 = st.sidebar.number_input("Primární napětí U1 [V]", value=230.0)
f = st.sidebar.number_input("Frekvence f [Hz]", value=50.0)
U21 = st.sidebar.number_input("U21 [V]", value=21.0)
I21 = st.sidebar.number_input("I21 [A]", value=2.9)
U22 = st.sidebar.number_input("U22 [V]", value=12.5)
I22 = st.sidebar.number_input("I22 [A]", value=2.15)


st.sidebar.header("2. Magnetika a limity")
B_m = st.sidebar.number_input("Indukce B_m [T]", value=1.6)
target_J = st.sidebar.slider("Proudová hustota J [A/mm²]", 1.5, 3.5, 2.1)

# --- VÝPOČET POTŘEBNÉHO JÁDRA ---
P21 = U21 * I21
P22 = U22 * I22
P2 = P21 + P22
P1_est = P2 + 7.5
S0Sfe_req = (P1_est * 100) / (2.22 * B_m * f * target_J * K_O * K_FE)

possible_cores = [c for c in CORES if c["product"] >= S0Sfe_req]
suggested = possible_cores[:5] if possible_cores else CORES[-5:]

st.subheader("1. Výběr magnetického jádra")
core_options = {c["name"]: c for c in suggested}
selected_core_name = st.selectbox(
    "Vyberte jádro (Seřazeno od nejvhodnějšího):", 
    options=list(core_options.keys())
)

# --- VLASTNÍ VÝPOČET S VYBRANÝM JÁDREM ---
core = core_options[selected_core_name]
S_Fe = core["S_Fe"]
S_o = core["S_o"]
m_Fe = core["m"]
a_okno = core["a"]
b_w = a_okno - 6
a_sloupek = core["d"]

N1_teor = (U1 * 10000) / (4.44 * B_m * f * S_Fe * K_FE)
N1_teor_round = round(N1_teor)
N1 = round(N1_teor * 0.95)
N21 = round(N1_teor * (U21 / U1) * 1.05)
N22 = round(N1_teor * (U22 / U1) * 1.05)

I1_real = P1_est / U1
d1, d1_m, S1 = get_best_wire(I1_real, target_J)
d21, d21_m, S21 = get_best_wire(I21, target_J)
d22, d22_m, S22 = get_best_wire(I22, target_J)

# Geometrie
z_v1 = math.floor(b_w / d1_m)
v1 = math.ceil(N1 / z_v1)
tw1 = v1 * d1_m + (v1 - 1) * IZOL_VRSTVA_PRIM
l_str1 = 4 * (a_sloupek + 2 * (T_KOSTRICKY + tw1 / 2))
R1 = (RHO_CU * N1 * l_str1 * 1e-3) / S1
dP1 = R1 * (I1_real**2)

z_v21 = math.floor(b_w / d21_m)
v21 = math.ceil(N21 / z_v21)
tw21 = v21 * d21_m + (v21 - 1) * IZOL_VRSTVA_SEK
l_str21 = 4 * (a_sloupek + 2 * (T_KOSTRICKY + tw21 / 2))
R21 = (RHO_CU * N21 * l_str21 * 1e-3) / S21
dP21 = R21 * (I21**2)

z_v22 = math.floor(b_w / d22_m)
v22 = math.ceil(N22 / z_v22)
tw22 = v22 * d22_m + (v22 - 1) * IZOL_VRSTVA_SEK
l_str22 = 4 * (a_sloupek + 2 * (T_KOSTRICKY + tw21 + IZOL_MEZI_SEKUNDARY + tw22 / 2))
R22 = (RHO_CU * N22 * l_str22 * 1e-3) / S22
dP22 = R22 * (I22**2)

dP_Cu = dP1 + dP21 + dP22
dP_Fe = P_FE_SPEC * m_Fe
dP_C = dP_Cu + dP_Fe
eta = (P2 / (P2 + dP_C)) * 100

# --- TABULKA SOUHRNNÝCH VÝSLEDKŮ ---
st.markdown("---")
st.subheader("2. Přehled vypočtených hodnot")

df_results = pd.DataFrame([
    {"Parametr": "Vybrané jádro", "Hodnota": f"{selected_core_name}", "Jednotka": "-"},
    {"Parametr": "Závity Primár (N1)", "Hodnota": f"{N1}", "Jednotka": "záv"},
    {"Parametr": "Vodič Primár (d_Cu)", "Hodnota": f"{d1:.3f}", "Jednotka": "mm"},
    {"Parametr": "Závity Sekundár 1 (N21)", "Hodnota": f"{N21}", "Jednotka": "záv"},
    {"Parametr": "Vodič Sekundár 1 (d_Cu)", "Hodnota": f"{d21:.3f}", "Jednotka": "mm"},
    {"Parametr": "Závity Sekundár 2 (N22)", "Hodnota": f"{N22}", "Jednotka": "záv"},
    {"Parametr": "Vodič Sekundár 2 (d_Cu)", "Hodnota": f"{d22:.3f}", "Jednotka": "mm"},
    {"Parametr": "Celkové ztráty Cu", "Hodnota": f"{dP_Cu:.2f}", "Jednotka": "W"},
    {"Parametr": "Celkové ztráty Fe", "Hodnota": f"{dP_Fe:.2f}", "Jednotka": "W"},
    {"Parametr": "Výsledná účinnost", "Hodnota": f"{eta:.2f}", "Jednotka": "%"}
])

st.dataframe(df_results, use_container_width=True)

# --- PŘÍPRAVA LATEX DOKUMENTU ---
def format_cz(number, decimals=2):
    return f"{number:.{decimals}f}".replace(".", "{,}")

tex_content = LATEX_TEMPLATE.replace("[U1]", str(int(U1))) \
    .replace("[FREQ]", str(int(f))) \
    .replace("[U21]", str(int(U21) if U21.is_integer() else U21).replace(".", ",")) \
    .replace("[I21]", str(I21).replace(".", ",")) \
    .replace("[U22]", str(int(U22) if U22.is_integer() else U22).replace(".", ",")) \
    .replace("[I22]", str(I22).replace(".", ",")) \
    .replace("[AUTOR]", autor) \
    .replace("[TRIDA]", trida) \
    .replace("[DATUM]", datum) \
    .replace("[P21]", format_cz(P21, 2)) \
    .replace("[P22]", format_cz(P22, 3)) \
    .replace("[P2]", format_cz(P2, 3)) \
    .replace("[P2_COMMA]", format_cz(P2, 3)) \
    .replace("[CORE_NAME]", selected_core_name) \
    .replace("[B_M]", format_cz(B_m, 1)) \
    .replace("[B_M_COMMA]", format_cz(B_m, 1)) \
    .replace("[S_FE]", format_cz(S_Fe, 1)) \
    .replace("[A_SLOUPEK]", str(int(a_sloupek))) \
    .replace("[M_FE]", format_cz(m_Fe, 1)) \
    .replace("[A_OKNO]", str(int(a_okno))) \
    .replace("[B_W]", str(int(b_w))) \
    .replace("[N1_TEOR]", str(N1_teor_round)) \
    .replace("[N1]", str(N1)) \
    .replace("[N21]", str(N21)) \
    .replace("[N22]", str(N22)) \
    .replace("[D1_MAX]", format_cz(d1_m, 3)) \
    .replace("[D1_MAX_COMMA]", format_cz(d1_m, 3)) \
    .replace("[Z_V1]", str(z_v1)) \
    .replace("[V1]", str(v1)) \
    .replace("[TW1]", format_cz(tw1, 2)) \
    .replace("[L_STR1]", format_cz(l_str1, 2)) \
    .replace("[L_STR1_COMMA]", format_cz(l_str1, 2)) \
    .replace("[S1_EXAKT]", format_cz(S1, 4)) \
    .replace("[R1]", format_cz(R1, 2)) \
    .replace("[D21_MAX]", format_cz(d21_m, 3)) \
    .replace("[Z_V21]", str(z_v21)) \
    .replace("[V21]", str(v21)) \
    .replace("[TW21]", format_cz(tw21, 2)) \
    .replace("[L_STR21]", format_cz(l_str21, 2)) \
    .replace("[L_STR21_COMMA]", format_cz(l_str21, 2)) \
    .replace("[S21_EXAKT]", format_cz(S21, 4)) \
    .replace("[R21]", format_cz(R21, 2)) \
    .replace("[D22_MAX]", format_cz(d22_m, 3)) \
    .replace("[Z_V22]", str(z_v22)) \
    .replace("[V22]", str(v22)) \
    .replace("[TW22]", format_cz(tw22, 2)) \
    .replace("[L_STR22]", format_cz(l_str22, 2)) \
    .replace("[L_STR22_COMMA]", format_cz(l_str22, 2)) \
    .replace("[S22_EXAKT]", format_cz(S22, 4)) \
    .replace("[R22]", format_cz(R22, 2)) \
    .replace("[DP_CU]", format_cz(dP_Cu, 2)) \
    .replace("[DP_FE]", format_cz(dP_Fe, 1)) \
    .replace("[DP_C]", format_cz(dP_C, 2)) \
    .replace("[DP_C_COMMA]", format_cz(dP_C, 2)) \
    .replace("[ETA]", format_cz(eta, 1))

# --- TLAČÍTKO PRO STAŽENÍ ---
st.markdown("---")
st.subheader("3. Generování protokolu")
st.success("Tvoje šablona protokolu byla úspěšně vyplněna vypočtenými hodnotami včetně tvého jména!")
st.download_button(
    label="⬇️ Stáhnout vyplněný protokol (.tex)",
    data=tex_content,
    file_name="protokol_navrhu.tex",
    mime="text/plain"
)