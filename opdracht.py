#Opdracht 1
import pandas as pd
import matplotlib.pyplot as plt

chemdata = pd.read_csv('csv/inventarisatie_DC_X.csv')
opdracht = input("Welke opdracht wil je uitvoeren? (Voer 2, 3, 4 of 5 in): ")

#opdracht 2
if opdracht == "2":
    plank_k = chemdata[chemdata['Locatie'] == 'Plank K']
    print(plank_k)

#opdracht 3
elif opdracht == 3:
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

#opdracht 5
if opdracht == 5:
    aantal_vloeistof = (chemdata['Fase (l,s,g)'] == 'l').sum()
    print(f"Er zijn in totaal {aantal_vloeistof} vloeistoffen aanwezig op DC.")
