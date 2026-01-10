#Opdracht 1
import pandas as pd
import matplotlib.pyplot as plt

chemdata = pd.read_csv('csv/inventarisatie_DC_X.csv')

#opdracht 2
plank_k = chemdata[chemdata['Locatie'] == 'Plank K']
print(plank_k)

#opdracht 3

#opdracht 4

#opdracht 5
aantal_vloeistof = (chemdata['Fase (l,s,g)'] == 'l').sum()
print(f"Er zijn in totaal {aantal_vloeistof} vloeistoffen aanwezig op DC.")
