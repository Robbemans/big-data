#Opdracht 1
import pandas as pd
import matplotlib.pyplot as plt
import os

chemdata = pd.read_csv('csv/inventarisatie_DC_X.csv')
opdracht = input("Welke opdracht wil je uitvoeren? (Voer 2, 3, 4 of 5 in): ")


#opdracht 2
if opdracht == "2":
    plank_k = chemdata[chemdata['Locatie'] == 'Plank K']
    print(plank_k)

#opdracht 3
elif opdracht == "3":
    chemdata['Locatie'] = chemdata['Locatie'].str.title() #fixt dubbel N plank, alles is nu hoofdletter :)

    aantal_per_plank = chemdata['Locatie'].value_counts()

    def plank_sort_key(x: str):
        parts = str(x).split()
        return parts[1] if len(parts) > 1 else str(x)

    aantal_per_plank = aantal_per_plank.sort_index(key=lambda idx: idx.map(plank_sort_key))

    plt.figure(figsize=(10, 5))
    ax = aantal_per_plank.plot(kind='bar')

    ax.set_xlabel("Plank")
    ax.set_ylabel("Aantal potjes")
    ax.set_title("Aantal potjes per plank op DC")

    for i, v in enumerate(aantal_per_plank.values):
        ax.text(i, v, str(v), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

#opdracht 4
elif opdracht == "4":
    CHAR_TO_GHS = {
    "<": "GHS01",  # explosief
    ">": "GHS02",  # ontvlambaar
    "O": "GHS03",  # oxiderend
    "/": "GHS04",  # gas onder druk
    "-": "GHS05",  # corrosief
    "\\": "GHS06", # toxisch (skull)
    "(": "GHS07",  # irritatie/waarschuwing
    ")": "GHS08",  # gezondheidsgevaar
    ".": "GHS09",  # milieu
}

    def decode_ghs_symbols(symbol_str: str):
        """Zet een string zoals '().\\=' om naar een lijst GHS codes."""
        if pd.isna(symbol_str) or symbol_str == "-" or symbol_str.strip() == "":
            return []

        codes = []
        for ch in str(symbol_str):
            if ch in ("=", " "):
                continue
            code = CHAR_TO_GHS.get(ch)
            if code and code not in codes:
                codes.append(code)
        return codes

    def show_ghs_icons(ghs_codes, icons_folder="ghs"):
        """Toon GHS icons naast elkaar met matplotlib."""
        if not ghs_codes:
            print("Geen GHS-symbolen gevonden voor deze stof.")
            return

        n = len(ghs_codes)
        fig, axes = plt.subplots(1, n, figsize=(1.6*n, 1.8))
        if n == 1:
            axes = [axes]

        for ax, code in zip(axes, ghs_codes):
            img_path = os.path.join(icons_folder, f"{code}.png")
            if not os.path.exists(img_path):
                ax.text(0.5, 0.5, f"{code}\n(niet gevonden)", ha="center", va="center")
            else:
                img = plt.imread(img_path)
                ax.imshow(img)
            ax.axis("off")
            ax.set_title(code, fontsize=9)

        plt.tight_layout()
        plt.show()

    def zoek_stof_en_toon_ghs(chemdata: pd.DataFrame, query: str, icons_folder="ghs"):
        """Zoek op (deel van) Naam stof en toon GHS symbolen."""
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

    zoekterm = input("Welke stof wil je opzoeken? ")
    zoek_stof_en_toon_ghs(chemdata, zoekterm, icons_folder="ghs")

#opdracht 5
elif opdracht == "5":
    aantal_vloeistof = (chemdata['Fase (l,s,g)'] == 'l').sum()
    print(f"Er zijn in totaal {aantal_vloeistof} vloeistoffen aanwezig op DC.")
