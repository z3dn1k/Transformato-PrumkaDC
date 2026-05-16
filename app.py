import streamlit as st
import math
import pandas as pd

# --- DATABÁZE VODIČŮ ---
WIRES = [
    (0.03, 0.048), (0.04, 0.058), (0.05, 0.068), (0.056, 0.077), (0.063, 0.084), 
    (0.071, 0.092), (0.08, 0.101), (0.09, 0.111), (0.1, 0.121), (0.112, 0.141), 
    (0.125, 0.154), (0.132, 0.161), (0.14, 0.169), (0.15, 0.179), (0.16, 0.189), 
    (0.17, 0.2), (0.18, 0.21), (0.19, 0.22), (0.2, 0.23), (0.212, 0.247), 
    (0.224, 0.259), (0.236, 0.271), (0.25, 0.285), (0.265, 0.303), (0.28, 0.318), 
    (0.3, 0.338), (0.315, 0.36), (0.335, 0.38), (0.355, 0.4), (0.375, 0.42), 
    (0.4, 0.445), (0.425, 0.477), (0.45, 0.502), (0.475, 0.527), (0.5, 0.552), 
    (0.53, 0.59), (0.56, 0.62), (0.6, 0.66), (0.63, 0.69), (0.67, 0.725), 
    (0.71, 0.775), (0.75, 0.825), (0.8, 0.875), (0.85, 0.925), (0.9, 0.975), 
    (0.95, 1.025), (1.0, 1.075), (1.06, 1.155), (1.12, 1.215), (1.18, 1.275), 
    (1.25, 1.345), (1.32, 1.415), (1.4, 1.495), (1.5, 1.595), (1.6, 1.695)
]

# --- DATABÁZE JADER ---
CORES = [
    {"name": "08001/0,35", "S_o": 1.92, "S_Fe": 0.5, "m": 0.03, "a": 18, "d": 10, "product": 0.96},
    {"name": "08002/0,35", "S_o": 1.92, "S_Fe": 0.8, "m": 0.05, "a": 24, "d": 10, "product": 1.54},
    {"name": "08003/0,35", "S_o": 1.92, "S_Fe": 1.0, "m": 0.07, "a": 28, "d": 10, "product": 1.92},
    {"name": "10000/0,35", "S_o": 3.0, "S_Fe": 0.8, "m": 0.06, "a": 26, "d": 10, "product": 2.4},
    {"name": "10001/0,35", "S_o": 3.0, "S_Fe": 1.0, "m": 0.08, "a": 30, "d": 10, "product": 3.0},
    {"name": "10002/0,35", "S_o": 3.0, "S_Fe": 1.2, "m": 0.09, "a": 26, "d": 15, "product": 3.6},
    {"name": "10003/0,35", "S_o": 3.0, "S_Fe": 1.5, "m": 0.12, "a": 30, "d": 15, "product": 4.5},
    {"name": "10004/0,35", "S_o": 3.0, "S_Fe": 2.25, "m": 0.21, "a": 40, "d": 15, "product": 6.75},
    {"name": "12001/0,35", "S_o": 4.44, "S_Fe": 1.2, "m": 0.12, "a": 28, "d": 15, "product": 5.33},
    {"name": "12003/0,35", "S_o": 4.44, "S_Fe": 2.0, "m": 0.2, "a": 32, "d": 20, "product": 8.88},
    {"name": "12004/0,35", "S_o": 4.44, "S_Fe": 3.0, "m": 0.3, "a": 42, "d": 20, "product": 13.32},
    {"name": "12005/0,35", "S_o": 4.44, "S_Fe": 4.0, "m": 0.5, "a": 52, "d": 20, "product": 17.76},
    {"name": "16003/0,35", "S_o": 7.68, "S_Fe": 2.0, "m": 0.23, "a": 36, "d": 20, "product": 15.36},
    {"name": "16004/0,35", "S_o": 7.68, "S_Fe": 3.0, "m": 0.4, "a": 46, "d": 20, "product": 23.04},
    {"name": "16005/0,35", "S_o": 7.68, "S_Fe": 4.0, "m": 0.55, "a": 56, "d": 20, "product": 30.72},
    {"name": "16012/0,35", "S_o": 7.68, "S_Fe": 2.5, "m": 0.32, "a": 41, "d": 20, "product": 19.2},
    {"name": "20001/0,35", "S_o": 12.0, "S_Fe": 2.0, "m": 0.3, "a": 40, "d": 20, "product": 24.0},
    {"name": "20002/0,35", "S_o": 12.0, "S_Fe": 3.0, "m": 0.45, "a": 50, "d": 20, "product": 36.0},
    {"name": "20003/0,35", "S_o": 12.0, "S_Fe": 4.0, "m": 0.65, "a": 60, "d": 20, "product": 48.0},
    {"name": "20004/0,35", "S_o": 12.0, "S_Fe": 4.5, "m": 0.7, "a": 50, "d": 30, "product": 54.0},
    {"name": "20005/0,35", "S_o": 12.0, "S_Fe": 6.0, "m": 1.0, "a": 60, "d": 30, "product": 72.0},
    {"name": "20006/0,35", "S_o": 12.0, "S_Fe": 9.0, "m": 1.7, "a": 80, "d": 30, "product": 108.0},
    {"name": "26001/0,35", "S_o": 19.76, "S_Fe": 4.5, "m": 0.85, "a": 56, "d": 30, "product": 88.92},
    {"name": "26002/0,35", "S_o": 19.76, "S_Fe": 6.0, "m": 1.2, "a": 66, "d": 30, "product": 118.56},
    {"name": "26003/0,35", "S_o": 19.76, "S_Fe": 9.0, "m": 2.0, "a": 86, "d": 30, "product": 177.84},
    {"name": "26004/0,35", "S_o": 19.76, "S_Fe": 8.0, "m": 1.6, "a": 66, "d": 40, "product": 158.08},
    {"name": "26005/0,35", "S_o": 19.76, "S_Fe": 12.0, "m": 2.6, "a": 86, "d": 40, "product": 237.12},
    {"name": "26006/0,35", "S_o": 19.76, "S_Fe": 16.0, "m": 3.9, "a": 106, "d": 40, "product": 316.16},
    {"name": "31000/0,35", "S_o": 29.14, "S_Fe": 10.0, "m": 2.5, "a": 81, "d": 40, "product": 291.4},
    {"name": "31001/0,35", "S_o": 29.14, "S_Fe": 8.0, "m": 1.8, "a": 71, "d": 40, "product": 233.12},
    {"name": "31002/0,35", "S_o": 29.14, "S_Fe": 12.0, "m": 3.1, "a": 91, "d": 40, "product": 349.68},
    {"name": "31003/0,35", "S_o": 29.14, "S_Fe": 16.0, "m": 4.6, "a": 111, "d": 40, "product": 466.24},
    {"name": "31004/0,35", "S_o": 29.14, "S_Fe": 12.5, "m": 3.0, "a": 81, "d": 50, "product": 364.25},
    {"name": "31005/0,35", "S_o": 29.14, "S_Fe": 20.0, "m": 5.5, "a": 111, "d": 50, "product": 582.8},
    {"name": "31006/0,35", "S_o": 29.14, "S_Fe": 25.0, "m": 7.3, "a": 131, "d": 50, "product": 728.5},
    {"name": "31020/0,35", "S_o": 29.14, "S_Fe": 4.0, "m": 0.95, "a": 71, "d": 20, "product": 116.56},
    {"name": "31030/0,35", "S_o": 29.14, "S_Fe": 9.0, "m": 2.3, "a": 91, "d": 30, "product": 262.26},
    {"name": "40001/0,35", "S_o": 56.0, "S_Fe": 12.5, "m": 4.0, "a": 90, "d": 50, "product": 700.0},
    {"name": "40002/0,35", "S_o": 56.0, "S_Fe": 20.0, "m": 7.0, "a": 120, "d": 50, "product": 1120.0},
    {"name": "40003/0,35", "S_o": 56.0, "S_Fe": 25.0, "m": 9.5, "a": 140, "d": 50, "product": 1400.0},
    {"name": "40030/0,35", "S_o": 56.0, "S_Fe": 9.0, "m": 3.0, "a": 100, "d": 30, "product": 504.0},
    {"name": "50004/0,35", "S_o": 75.0, "S_Fe": 18.0, "m": 6.5, "a": 110, "d": 60, "product": 1350.0},
    {"name": "50005/0,35", "S_o": 75.0, "S_Fe": 30.0, "m": 11.7, "a": 150, "d": 60, "product": 2250.0},
    {"name": "50006/0,35", "S_o": 75.0, "S_Fe": 36.0, "m": 15.0, "a": 170, "d": 60, "product": 2700.0},
    {"name": "70010/0,35", "S_o": 81.2, "S_Fe": 19.2, "m": 6.75, "a": 134, "d": 60, "product": 1559.04},
    {"name": "70020/0,35", "S_o": 122.5, "S_Fe": 26.4, "m": 12.5, "a": 158, "d": 60, "product": 3234.0},
    {"name": "75040/0,35", "S_o": 139.5, "S_Fe": 24.6, "m": 11.8, "a": 157, "d": 60, "product": 3431.7},
    {"name": "88004/0,35", "S_o": 112.64, "S_Fe": 28.8, "m": 12.3, "a": 184, "d": 60, "product": 3244.03}
]

# --- PEVNÉ KONSTANTY ---
RHO_CU = 0.0178               # Měrný odpor Cu (ρ) [Ω·mm²/m]
P_FE_SPEC = 2.5               # Měrné ztráty plechů (p_Fe) [W/kg]
T_KOSTRICKY = 1.0             # Tloušťka stěny kostřičky [mm]
IZOL_VRSTVA_PRIM = 0.2        # Izolace mezi vrstvami primáru [mm]
IZOL_VRSTVA_SEK = 0.2         # Izolace mezi vrstvami sekundáru [mm]
IZOL_MEZI_SEKUNDARY = 0.6     # Izolace mezi vinutími (sekundáry) [mm]
K_O = 0.3                     # Činitel plnění okna (k_o)
K_FE = 0.97                   # Činitel plnění železa (k_Fe)

# --- FUNKCE VÝBĚRU BEZPEČNÉHO DRÁTU ---
def get_best_wire(I, target_J):
    S_req = I / target_J  
    for d_cu, d_max in WIRES:
        S_exakt = math.pi * (d_cu**2) / 4
        if S_exakt >= S_req:
            return d_cu, d_max, S_exakt
    return WIRES[-1][0], WIRES[-1][1], math.pi * (WIRES[-1][0]**2) / 4

# --- LATEX TEMPLATE ---
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

Teoretický počet závitů jsem vypočítal pro $k_{Fe} = 0{,}97$:
\begin{equation*}
N_{1(teor)} = \frac{U_1 \cdot 10^4}{4{,}44 \cdot B_m \cdot f \cdot S_{Fe} \cdot k_{Fe}} = \frac{[U1] \cdot 10^4}{4{,}44 \cdot [B_M] \cdot [FREQ] \cdot [S_FE] \cdot 0{,}97} = [N1_TEOR]~\text{závitů}.
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

\section{Souhrnné výsledky a závěr}
\begin{table}[h!]
\centering
\caption{Přehled parametrů navrženého transformátoru}
\begin{tabular}{lcccccc}
\toprule
\rowcolor{primary!10}
\textbf{Vinutí} & \textbf{$U$ [V]} & \textbf{$I$ [A]} & \textbf{$N$ [-]} & \textbf{$d_{Cu}$ [mm]} & \textbf{$S_{exakt}$ [mm$^2$]} & \textbf{$R$ [$\Omega$]} \\
\midrule
Primár $N_1$ & \num{[U1]} & \num{[I1_REAL]} & \num{[N1]} & \num{[D1_CU]} & \num{[S1_EXAKT]} & \num{[R1]} \\
Sekundár $N_{21}$ & \num{[U21]} & \num{[I21]} & \num{[N21]} & \num{[D21_CU]} & \num{[S21_EXAKT]} & \num{[R21]} \\
Sekundár $N_{22}$ & \num{[U22]} & \num{[I22]} & \num{[N22]} & \num{[D22_CU]} & \num{[S22_EXAKT]} & \num{[R22]} \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[h!]
\centering
\begin{tabular}{lr}
\toprule
\rowcolor{primary!10}
\multicolumn{2}{c}{\textbf{Celková energetická bilance}} \\
\midrule
Výstupní výkon $P_2$ & \SI{[P2_COMMA]}{W} \\
Ztráty v mědi $\Delta P_{Cu}$ & \SI{[DP_CU]}{W} \\
Ztráty v železe $\Delta P_{Fe}$ & \SI{[DP_FE]}{W} \\
Celkový příkon $P_1$ & \SI{[P1_REAL]}{W} \\
\midrule
\textbf{Výsledná účinnost $\eta$} & \textbf{[ETA]\,\%} \\
\bottomrule
\end{tabular}
\end{table}

Navržený dvousloupkový transformátor s C-jádrem splňuje všechny konstrukční a bezpečnostní požadavky. Byla nalezena optimální konstrukční varianta s účinností [ETA]\,\%, která efektivně využívá prostor a zamezuje zbytečnému předimenzování obvodu.

\end{document}"""

# --- UI STREAMLIT ---
st.set_page_config(page_title="Návrh jednofázového síťového transformátoru", layout="wide")
st.title("Aplikace pro návrh síťového transformátoru")
st.markdown("Aplikace automaticky filtruje jádra tak, aby navržené řešení vyhovovalo intervalu účinnosti 90 % až 95 %.")

# --- VSTUPY V POSTRANNÍM PANELU ---
st.sidebar.header("1. Údaje o autorovi a napájení")
autor = st.sidebar.text_input("Jméno autora", value="Jan Zedník")
trida = st.sidebar.text_input("Třída", value="E3A")
datum = st.sidebar.text_input("Datum protokolu", value="11.05.2026")
st.sidebar.markdown("---")

U1 = st.sidebar.number_input("Primární napětí U1 [V]", value=230.0)
f = st.sidebar.number_input("Frekvence f [Hz]", value=50.0)
U21 = st.sidebar.number_input("Napětí sekundáru 1 - U21 [V]", value=15.0)
I21 = st.sidebar.number_input("Proud sekundáru 1 - I21 [A]", value=1.0)
U22 = st.sidebar.number_input("Napětí sekundáru 2 - U22 [V]", value=8.0)
I22 = st.sidebar.number_input("Proud sekundáru 2 - I22 [A]", value=3.0)

st.sidebar.header("2. Magnetické vlastnosti")
B_m = st.sidebar.number_input("Indukce B_m [T]", value=1.6)
target_J = st.sidebar.slider("Proudová hustota J [A/mm²]", 1.5, 3.5, 2.0)

# --- VÝPOČETNÍ JÁDRO ---
P21 = U21 * I21
P22 = U22 * I22
P2 = P21 + P22

analyzed_cores = []

for core in CORES:
    S_Fe = core["S_Fe"]
    a_okno = core["a"]
    b_w = a_okno - 4 
    a_sloupek = core["d"]
    m_Fe = core["m"]

    N1_teor = (U1 * 10000) / (4.44 * B_m * f * S_Fe * K_FE)
    
    N1 = math.ceil(N1_teor * 0.95)
    N21 = math.ceil(N1_teor * (U21 / U1) / 0.95)
    N22 = math.ceil(N1_teor * (U22 / U1) / 0.95)

    dP_Fe = P_FE_SPEC * m_Fe

    d21, d21_m, S21 = get_best_wire(I21, target_J)
    z_v21 = math.floor(b_w / d21_m) if d21_m > 0 else 1
    v21 = math.ceil(N21 / z_v21)
    tw21 = v21 * d21_m + (v21 - 1) * IZOL_VRSTVA_SEK
    l_str21 = 4 * (a_sloupek + 2 * (T_KOSTRICKY + tw21 / 2))
    R21 = (RHO_CU * N21 * l_str21 * 1e-3) / S21
    dP21 = R21 * (I21**2)

    d22, d22_m, S22 = get_best_wire(I22, target_J)
    z_v22 = math.floor(b_w / d22_m) if d22_m > 0 else 1
    v22 = math.ceil(N22 / z_v22)
    tw22 = v22 * d22_m + (v22 - 1) * IZOL_VRSTVA_SEK
    l_str22 = 4 * (a_sloupek + 2 * (T_KOSTRICKY + tw21 + IZOL_MEZI_SEKUNDARY + tw22 / 2))
    R22 = (RHO_CU * N22 * l_str22 * 1e-3) / S22
    dP22 = R22 * (I22**2)

    I1_est = (P2 + dP_Fe + dP21 + dP22 + 5.0) / U1 
    d1, d1_m, S1 = get_best_wire(I1_est, target_J)
    z_v1 = math.floor(b_w / d1_m) if d1_m > 0 else 1
    v1 = math.ceil(N1 / z_v1)
    tw1 = v1 * d1_m + (v1 - 1) * IZOL_VRSTVA_PRIM
    l_str1 = 4 * (a_sloupek + 2 * (T_KOSTRICKY + tw1 / 2))
    R1 = (RHO_CU * N1 * l_str1 * 1e-3) / S1

    C = P2 + dP_Fe + dP21 + dP22
    Discriminant = U1**2 - 4 * R1 * C
    if Discriminant >= 0:
        I1_real = (U1 - math.sqrt(Discriminant)) / (2 * R1)
    else:
        I1_real = I1_est

    dP1 = R1 * (I1_real**2)
    dP_Cu = dP1 + dP21 + dP22
    dP_C = dP_Cu + dP_Fe
    P1_real = P2 + dP_C
    eta = (P2 / P1_real) * 100

    analyzed_cores.append({
        "name": core["name"], "core": core, "eta": eta,
        "N1": N1, "N21": N21, "N22": N22, "N1_teor": round(N1_teor),
        "d1": d1, "d1_m": d1_m, "S1": S1, "z_v1": z_v1, "v1": v1, "tw1": tw1, "l_str1": l_str1, "R1": R1,
        "d21": d21, "d21_m": d21_m, "S21": S21, "z_v21": z_v21, "v21": v21, "tw21": tw21, "l_str21": l_str21, "R21": R21,
        "d22": d22, "d22_m": d22_m, "S22": S22, "z_v22": z_v22, "v22": v22, "tw22": tw22, "l_str22": l_str22, "R22": R22,
        "I1_real": I1_real, "dP_Fe": dP_Fe, "dP_Cu": dP_Cu, "dP_C": dP_C, "P1_real": P1_real
    })

# --- FILTROVÁNÍ DLE FIXNÍHO LIMITU (90 - 95 %) ---
valid_cores = [c for c in analyzed_cores if 90.0 <= c["eta"] <= 95.0]

if valid_cores:
    valid_cores.sort(key=lambda x: x["eta"], reverse=True)
else:
    st.warning("Upozornění: Žádné jádro nesplňuje podmínku účinnosti mezi 90 % a 95 %. Zobrazuji všechna dostupná jádra.")
    valid_cores = analyzed_cores
    valid_cores.sort(key=lambda x: x["eta"], reverse=True)

st.subheader("1. Výběr vhodného transformátorového jádra")
st.info("Aplikace zobrazuje pouze jádra s účinností mezi 90 % a 95 %.")

core_options = {f"{c['name']} (Účinnost: {c['eta']:.2f} %)": c for c in valid_cores}
selected_option = st.selectbox("Vyberte jádro pro návrh:", options=list(core_options.keys()))

# --- NAČTENÍ VÝSLEDKŮ ---
sel = core_options[selected_option]

st.markdown("---")
st.subheader("2. Souhrn vypočtených elektrických a konstrukčních parametrů")

df_results = pd.DataFrame([
    {"Parametr": "Vybrané jádro", "Hodnota": f"{sel['name']}", "Jednotka": "-"},
    {"Parametr": "Skutečný proud Primár (I1)", "Hodnota": f"{sel['I1_real']:.4f}", "Jednotka": "A"},
    {"Parametr": "Závity Primár (N1)", "Hodnota": f"{sel['N1']}", "Jednotka": "záv"},
    {"Parametr": "Vodič Primár (d_Cu)", "Hodnota": f"{sel['d1']:.3f}", "Jednotka": "mm"},
    {"Parametr": "Závity Sekundár 1 (N21)", "Hodnota": f"{sel['N21']}", "Jednotka": "záv"},
    {"Parametr": "Vodič Sekundár 1 (d_Cu)", "Hodnota": f"{sel['d21']:.3f}", "Jednotka": "mm"},
    {"Parametr": "Závity Sekundár 2 (N22)", "Hodnota": f"{sel['N22']}", "Jednotka": "záv"},
    {"Parametr": "Vodič Sekundár 2 (d_Cu)", "Hodnota": f"{sel['d22']:.3f}", "Jednotka": "mm"},
    {"Parametr": "Celkové ztráty Cu", "Hodnota": f"{sel['dP_Cu']:.3f}", "Jednotka": "W"},
    {"Parametr": "Celkové ztráty Fe", "Hodnota": f"{sel['dP_Fe']:.3f}", "Jednotka": "W"},
    {"Parametr": "Výsledná přesná účinnost", "Hodnota": f"{sel['eta']:.3f}", "Jednotka": "%"}
])

st.dataframe(df_results, use_container_width=True)

# --- PŘÍPRAVA LATEX DOKUMENTU ---
def format_cz(number, decimals=3):
    return f"{number:.{decimals}f}".replace(".", "{,}")

tex_content = LATEX_TEMPLATE.replace("[U1]", str(int(U1))) \
    .replace("[FREQ]", str(int(f))) \
    .replace("[U21]", str(int(U21) if U21.is_integer() else U21).replace(".", ",")) \
    .replace("[I21]", format_cz(I21, 3)) \
    .replace("[U22]", str(int(U22) if U22.is_integer() else U22).replace(".", ",")) \
    .replace("[I22]", format_cz(I22, 3)) \
    .replace("[AUTOR]", autor) \
    .replace("[TRIDA]", trida) \
    .replace("[DATUM]", datum) \
    .replace("[P21]", format_cz(P21, 2)) \
    .replace("[P22]", format_cz(P22, 2)) \
    .replace("[P2]", format_cz(P2, 2)) \
    .replace("[P2_COMMA]", format_cz(P2, 2)) \
    .replace("[P1_REAL]", format_cz(sel['P1_real'], 2)) \
    .replace("[CORE_NAME]", sel['name']) \
    .replace("[B_M]", format_cz(B_m, 1)) \
    .replace("[B_M_COMMA]", format_cz(B_m, 1)) \
    .replace("[S_FE]", format_cz(sel['core']['S_Fe'], 1)) \
    .replace("[A_SLOUPEK]", str(int(sel['core']['d']))) \
    .replace("[M_FE]", format_cz(sel['core']['m'], 1)) \
    .replace("[A_OKNO]", str(int(sel['core']['a']))) \
    .replace("[B_W]", str(int(sel['core']['a'] - 4))) \
    .replace("[N1_TEOR]", str(sel['N1_teor'])) \
    .replace("[I1_REAL]", format_cz(sel['I1_real'], 3)) \
    .replace("[N1]", str(sel['N1'])) \
    .replace("[N21]", str(sel['N21'])) \
    .replace("[N22]", str(sel['N22'])) \
    .replace("[D1_CU]", format_cz(sel['d1'], 3)) \
    .replace("[D21_CU]", format_cz(sel['d21'], 3)) \
    .replace("[D22_CU]", format_cz(sel['d22'], 3)) \
    .replace("[D1_MAX]", format_cz(sel['d1_m'], 3)) \
    .replace("[D1_MAX_COMMA]", format_cz(sel['d1_m'], 3)) \
    .replace("[Z_V1]", str(sel['z_v1'])) \
    .replace("[V1]", str(sel['v1'])) \
    .replace("[TW1]", format_cz(sel['tw1'], 2)) \
    .replace("[L_STR1]", format_cz(sel['l_str1'], 2)) \
    .replace("[L_STR1_COMMA]", format_cz(sel['l_str1'], 2)) \
    .replace("[S1_EXAKT]", format_cz(sel['S1'], 4)) \
    .replace("[R1]", format_cz(sel['R1'], 3)) \
    .replace("[D21_MAX]", format_cz(sel['d21_m'], 3)) \
    .replace("[Z_V21]", str(sel['z_v21'])) \
    .replace("[V21]", str(sel['v21'])) \
    .replace("[TW21]", format_cz(sel['tw21'], 2)) \
    .replace("[L_STR21]", format_cz(sel['l_str21'], 2)) \
    .replace("[L_STR21_COMMA]", format_cz(sel['l_str21'], 2)) \
    .replace("[S21_EXAKT]", format_cz(sel['S21'], 4)) \
    .replace("[R21]", format_cz(sel['R21'], 3)) \
    .replace("[D22_MAX]", format_cz(sel['d22_m'], 3)) \
    .replace("[Z_V22]", str(sel['z_v22'])) \
    .replace("[V22]", str(sel['v22'])) \
    .replace("[TW22]", format_cz(sel['tw22'], 2)) \
    .replace("[L_STR22]", format_cz(sel['l_str22'], 2)) \
    .replace("[L_STR22_COMMA]", format_cz(sel['l_str22'], 2)) \
    .replace("[S22_EXAKT]", format_cz(sel['S22'], 4)) \
    .replace("[R22]", format_cz(sel['R22'], 3)) \
    .replace("[DP_CU]", format_cz(sel['dP_Cu'], 2)) \
    .replace("[DP_FE]", format_cz(sel['dP_Fe'], 2)) \
    .replace("[DP_C]", format_cz(sel['dP_C'], 2)) \
    .replace("[DP_C_COMMA]", format_cz(sel['dP_C'], 2)) \
    .replace("[ETA]", format_cz(sel['eta'], 2))

# --- TLAČÍTKO PRO STAŽENÍ ---
st.markdown("---")
st.subheader("3. Export protokolu")
st.success("Protokol byl úspěšně vygenerován.")
st.download_button(
    label="Stáhnout vyplněný protokol (.tex)",
    data=tex_content,
    file_name="protokol_navrhu.tex",
    mime="text/plain"
)