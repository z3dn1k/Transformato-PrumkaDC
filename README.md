# Návrh nf transformátoru (Generátor pro Průmyslovku Děčín) - Prototype

Ahoj! Tato aplikace byla vytvořena speciálně pro studenty **Vyšší odborné školy a Střední průmyslové školy strojní, stavební a dopravní v Děčíně**. 

Slouží k automatickému výpočtu dvousloupkového síťového transformátoru s vinutým C-jádrem. Nejen že za tebe spočítá všechny odpory, průměry drátů, délky a účinnost, ale hlavně **vygeneruje hotový protokol v LaTeXu**, který stačí jen odevzdat!

**Autor:** Jan Zedník

---

## Co appka umí
- **Přesný inženýrský výpočet:** Počítá exaktní průřezy vodičů a reálnou geometrii pro dvě samostatné kostřičky (primár na levém sloupku, oba sekundáry na pravém).
- **Chytrý výběr jádra:** Na základě tvých parametrů prohledá tabulku jader a nabídne 5 nejvhodnějších C-jader (např. 26003/0,35), aby se ti vše s rezervou vešlo.
- **LaTeX Export na jedno kliknutí:** Aplikace vezme tvé výsledky, tvoje jméno, třídu a rovnou je nasází do profesionální `\documentclass{article}` šablony.

---

## Návod na zprovoznění (Jak to spustit)

Aplikace běží na Python frameworku **Streamlit**. Pokud ještě nemáš nainstalovaný Python, stáhni si ho z [python.org](https://www.python.org/downloads/).

### 1. Stažení projektu
Stáhni si tento repozitář (zelené tlačítko `Code` -> `Download ZIP`) a rozbal ho do libovolné složky, nebo použij git:
` ` `bash
git clone https://github.com/z3dn1k/Transformato-PrumkaDC
` ` `
*(Poznámka: v reálném souboru odstraň mezery mezi zpětnými apostrofy v ukázkách kódu)*

### 2. Instalace knihoven
Otevři si v dané složce terminál (příkazovou řádku) a nainstaluj potřebné knihovny zadáním tohoto příkazu:
` ` `bash
pip install streamlit pandas
` ` `

### 3. Spuštění aplikace
Aplikaci nastartuješ tímto příkazem v terminálu:
` ` `bash
streamlit run app.py
` ` `
*Poznámka: Automaticky se ti otevře okno v prohlížeči. Pokud ne, klikni na Local URL adresu (obvykle `http://localhost:8501`), která se vypíše v terminálu.*

---

## Jak s aplikací pracovat
1. V postranním levém panelu vyplň **své jméno, třídu a parametry trafa** (U1, U21, U22, atd.).
2. Aplikace ti dole nabídne nejlepší **C-jádro**. Zkontroluj, zda ti vyhovuje.
3. V hlavní části obrazovky se ti automaticky přepočítají veškeré hodnoty (počty závitů, úbytky napětí, reálné průřezy vodičů, účinnost).
4. Úplně dole klikni na tlačítko **Stáhnout vyplněný protokol (.tex)**.
5. Stažený soubor otevři např. v [Overleafu](https://www.overleaf.com/) a máš hotovo!

---
**Upozornění:** Konstanty pro izolaci (0,05 mm a 0,10 mm), měrný odpor mědi ($\rho = 0,0178$) a sycení C-jader ($B_m = 1,6\text{ T}$) jsou v kódu nastaveny fixně, aby přesně odpovídaly zadáním a doporučením pro návrh NF traf na naší škole.
