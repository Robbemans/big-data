#Opdracht 1
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from collections import Counter

def running_in_jupyter():
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except ImportError:
        return False

if running_in_jupyter():
    print("Dit programma werkt lekker niet in jupyter, gebruik ALSJEBLIEFT visual studio code :p")
    sys.exit()

BASE_DIR = Path.cwd() if running_in_jupyter() else Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "csv" / "inventarisatie_DC_X.csv"
GHS_DIR = BASE_DIR / "ghs"

chemdata = pd.read_csv(CSV_PATH)
#pop up voor opdracht keuze
def popup_assignment_select():
    import tkinter as tk
    from tkinter import simpledialog

    root = tk.Tk()
    root.title("Opdracht selecteren")

    keuze = tk.StringVar(value="")

    def select(value):
        keuze.set(value)
        root.destroy()

    tk.Label(
        root,
        text="Welke opdracht wil je uitvoeren?",
        padx=20,
        pady=10
    ).pack()

    tk.Button(
        root,
        text="Opdracht 2 – Chemicaliën op plank K",
        width=40,
        command=lambda: select("2")
    ).pack(pady=4)

    tk.Button(
        root,
        text="Opdracht 3 – Aantal potjes per plank",
        width=40,
        command=lambda: select("3")
    ).pack(pady=4)

    tk.Button(
        root,
        text="Opdracht 4 – Zoek stof + GHS symbolen",
        width=40,
        command=lambda: select("4")
    ).pack(pady=4)

    tk.Button(
        root,
        text="Opdracht 5 – Aantal vloeistoffen",
        width=40,
        command=lambda: select("5")
    ).pack(pady=4)

    root.mainloop()
    return keuze.get()

if running_in_jupyter():
    print("Running in Jupyter Notebook")
    opdracht = input("Kies opdracht (2, 3, 4, of 5): ")
else:
    opdracht = popup_assignment_select()


#opdracht 2
if opdracht == "2":
    plank_k = chemdata[chemdata['Locatie'].str.strip().str.title() == 'Plank K']
    print(plank_k)

#opdracht 3
elif opdracht == "3":
    chemdata['Locatie'] = chemdata['Locatie'].str.strip().str.title() #Fixt hoofdlettergevoeligheid en eventuele extra spaties :)

    aantal_per_plank = chemdata['Locatie'].value_counts() #tel aantal punten per plank

    def plank_sort_key(x: str):
        parts = str(x).split() #convert alles naar string, split op spaties (voor alfabetishe volgorde)
        return parts[1] if len(parts) > 1 else str(x) #negeer het eerste woord als er 2 woorden zijn, geef het eerste woord als t er maar 1 is.

    aantal_per_plank = aantal_per_plank.sort_index(key=lambda idx: idx.map(plank_sort_key)) # zet de planken op volgorde

    plt.figure(figsize=(10, 5))
    ax = aantal_per_plank.plot(kind='bar') #maak die grafiek

    ax.set_xlabel("Plank")
    ax.set_ylabel("Aantal potjes")
    ax.set_title("Aantal potjes per plank op DC")

    for i, v in enumerate(aantal_per_plank.values):
        ax.text(i, v, str(v), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

#opdracht 4 --> probeer bijvoorbeeld salicylzuur
#(A)
elif opdracht == "4":
    CHAR_TO_GHS = {
    "<": "GHS01",  # explosief
    ">": "GHS02",  # ontvlambaar
    "O": "GHS03",  # oxiderend
    "/": "GHS04",  # gas onder druk
    "-": "GHS05",  # corrosief
    "\\": "GHS06", # toxisch
    "(": "GHS07",  # irritatie/waarschuwing
    ")": "GHS08",  # gezondheidsgevaar
    ".": "GHS09",  # milieu
}

    def decode_ghs_symbols(symbol_str: str):
        #zet de leestekens gebruikt in excel om naar ghs symbolen
        if pd.isna(symbol_str) or symbol_str == "-" or symbol_str.strip() == "":
            return []

        #maak een lege lijst, voeg het ghs symbool toe die nodig is als hij nog niet in de lijst staat
        codes = []
        for ch in str(symbol_str):
            if ch in ("=", " "):
                continue
            code = CHAR_TO_GHS.get(ch)
            if code and code not in codes:
                codes.append(code)
        return codes

    def show_ghs_icons(ghs_codes, icons_folder=GHS_DIR):
        #zet de ghs symbolen naast elkaar in matplotlib
        if not ghs_codes:
            print("Geen GHS-symbolen gevonden voor deze stof.")
            return

        n = len(ghs_codes)
        fig, axes = plt.subplots(1, n, figsize=(1.6*n, 1.8))
        if n == 1:
            axes = [axes]

        for ax, code in zip(axes, ghs_codes):
            img_path = Path(icons_folder) / f"{code}.png"
            if not img_path.exists():
                ax.text(0.5, 0.5, f"{code}\n(niet gevonden)", ha="center", va="center")
            else:
                img = plt.imread(str(img_path))
                ax.imshow(img)

                ax.axis("off")
                ax.set_title(code, fontsize=9)

        plt.tight_layout()
        plt.show()

    def zoek_stof_en_toon_ghs(chemdata: pd.DataFrame, query: str, icons_folder=GHS_DIR):
        #zoek de naam van de stof en laat ghs zien
        hits = chemdata[chemdata["Naam stof"].str.contains(query, case=False, na=False)]

        if hits.empty:
            print("Geen stof gevonden met die zoekterm.")
            return

        # Als er meerdere hits zijn: laat ze zien en pak de eerste
        if len(hits) > 1:
            print("Meerdere resultaten gevonden, ik pak de eerste. Resultaten:")
            print(hits[["Naam stof", "Locatie", "GHS-symbolen"]].head(10).to_string(index=False))

        row = hits.iloc[0]
        naam = row["Naam stof"]
        sym = row["GHS-symbolen"]

        ghs_codes = decode_ghs_symbols(sym)

        print(f"\nStof: {naam}")
        print(f"Locatie: {row['Locatie']}")
        print(f"GHS-symbolen veld: {sym}")
        print(f"Decoded GHS codes: {ghs_codes}")

        show_ghs_icons(ghs_codes, icons_folder=icons_folder)

    def popup_input(prompt):
        import tkinter as tk
        from tkinter import simpledialog

        root = tk.Tk()
        root.withdraw() 
        answer = simpledialog.askstring("Zoek stof", prompt)
        root.destroy()
        return answer

    if running_in_jupyter():
        zoekterm = input("Welke stof wil je opzoeken? ")
    else:
        zoekterm = popup_input("Welke stof wil je opzoeken?")

    if zoekterm:
        zoek_stof_en_toon_ghs(chemdata, zoekterm, icons_folder=GHS_DIR)
    else:
        print("Geen invoer gegeven.")
#(B)
    def meest_voorkomend(chemdata: pd.DataFrame):
        counter = Counter()

        for sym in chemdata["GHS-symbolen"]:
            codes = decode_ghs_symbols(sym)
            counter.update(codes)

        if not counter:
            print("Geen GHS-symbolen gevonden in de dataset.")
            return

        meest_voorkomend, aantal = counter.most_common(1)[0]

        print("Overzicht GHS-symbolen:")
        for ghs, count in counter.most_common():
            print(f"{ghs}: {count} keer")

        print(f"\nMeest voorkomende GHS-symbool: {meest_voorkomend} ({aantal} keer)")
    meest_voorkomend(chemdata)

#opdracht 5
elif opdracht == "5":
    aantal_vloeistof = (chemdata['Fase (l,s,g)'] == 'l').sum()
    print(f"Er zijn in totaal {aantal_vloeistof} vloeistoffen aanwezig op DC.")