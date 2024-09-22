# 1. Premier site: IMDB

#a) Import de librairies
from bs4 import BeautifulSoup as bs
import requests 

#b)
url_imdb = "https://assets-datascientest.s3.eu-west-1.amazonaws.com/IMDb.html"

#c)
page_imdb = requests.get(url_imdb)

bs_imdb = bs(page_imdb.content, "lxml")


bs_imdb.prettify().splitlines()[0:30]

# d)
"""
Les elements contenant les titre sont: <td class="titleColumn">
Les elements contenant l'année sont: <td class="titleColumn> <span class="secondaryInfo">(1994)</span></td>
Les elements contenant le rang sont: <td class="ratingColumn imdbRating"> <strong title="9,2 based on 2 680 046 user ratings">9.2</span></td>
"""

tbody = bs_imdb.find('tbody', attrs = {'class': "lister-list"})

films_imdb = tbody.find_all('tr')

print(films_imdb)


#e) le titre du premier film
for tr in films_imdb:
    first_td = tr.find('td', attrs = {'class': "titleColumn"}).find('a')
    if first_td:
        print("Titre du premier film: ",first_td.text)
        break

#f) le rang du premier film
for tr in films_imdb:
    first_td = tr.find('td', attrs = {'class': "titleColumn"})
    if first_td:
        variable= first_td.text
        print("Rang du premier film: ",variable.strip().split(".\n")[0])
        break

#g) Année de sorite du premier film
for tr in films_imdb:
    first_td = tr.find('td', attrs = {'class': "titleColumn"}).find('span' ,attrs = {'class': "secondaryInfo"})
    if first_td:
        print("Année du premier titre: ",first_td.text.replace('(', '').replace(')', ''))
        break

# h Identifier les elements contenants les notes des films

notes = [] # liste pour contenir le code source des notes

for tr in films_imdb:
    element = tr.find('td', attrs = {'class': "ratingColumn imdbRating"}).find('strong')
    notes.append(element)

print("La note du premier élément: ",notes[0].text)

###############################################################
#i) importer la librairie Pandas
import pandas as pd

#j) recuperer les titres, rangs, années de sortie, notes pour tous les films dans un Dataframe

titres_list = [] # liste des titres
rangs_list = [] # liste des rangs
annees_list = [] # liste des annees
notes_list = [] # liste des notes

for tr in films_imdb:
    titre = tr.find('td', attrs = {'class': "titleColumn"}).find('a').text
    titres_list.append(titre.strip())

    rang = tr.find('td', attrs = {'class': "titleColumn"}).text
    rangs_list.append(rang.strip().split(".\n")[0])

    annee = tr.find('td', attrs = {'class': "titleColumn"}).find('span' ,attrs = {'class': "secondaryInfo"}).text.replace('(', '').replace(')', '')
    annees_list.append(annee.strip())

    note = tr.find('td', attrs = {'class': "ratingColumn imdbRating"}).find('strong').text
    notes_list.append(note.strip())


data_film = {
    'Titre': titres_list,
    'Rang': rangs_list,
    'Annee': annees_list,
    'Note': notes_list

}

df_imdb = pd.DataFrame(data_film)

#k) Afficher les premières lignes de df_imdb
df_imdb.head(10)

######################################################################################
#2. Deuxième site : Allociné

#a) Import de librairies
from bs4 import BeautifulSoup as bs
import requests 

#a) stocker l'url
url_allocine = "https://assets-datascientest.s3.eu-west-1.amazonaws.com/AlloCin%C3%A9.html"

#b) récuperer le code HTML de la page
page_allocine = requests.get(url_allocine)

bs_allocine = bs(page_allocine.content, "lxml")


#bs_allocine.prettify().splitlines()[0:30]


# c)

films_allocine = bs_allocine.find('body', attrs = {'id': "allocine__movies_top"}).find('div', attrs = {'class':"gd-col-middle"}).find_all('li', attrs = {'class':"mdl"})
#print(films_allocine)

# le nombre de films
films_allocine_titre = [film.find('h2', attrs={'class': "meta-title"}) for film in films_allocine]
print("Le nombre de films est: ",len(films_allocine_titre))

# e) Nettoyer et afficher le premier titre
films_allocine_titre = [film.find('h2', attrs={'class': "meta-title"}) for film in films_allocine]
print("Le titre du premier film est: ",films_allocine_titre[0].text.strip())

# f) la notre de press du premier film

note_presse = [film.find('span', attrs={'class': "stareval-note"}) for film in films_allocine]
print("La note presse du premier film:" ,note_presse[0].text.strip())

#g) la notre de spectateur du premier film
note_spectateur = [film.find('span', attrs={'class': "stareval-note"}).find_next('span') for film in films_allocine]
print("La note spectateur du premier film:" ,note_spectateur[0].text.strip())

#h) Creattion d'un DataFrame df_allocine
import pandas as pd
   # alimentation des listes
titre_list = [film.find('h2', attrs={'class': "meta-title"}).text.strip() for film in films_allocine]
note_presse_list = [film.find('span', attrs={'class': "stareval-note"}).text.strip() for film in films_allocine]
note_spectateur_list = [film.find('span', attrs={'class': "stareval-note"}).find_next('span').text.strip() for film in films_allocine]

   # creation d'un dictionnaire
data_allocine = {
    'Titre': titre_list,
    'Note presse': note_presse_list,
    'Note spectateur': note_spectateur_list,
}
 
   # Creation d'un DF
df_allocine = pd.DataFrame(data_allocine)
df_allocine.head(10)

################################################################################"""

#3.Comparaison

#a)Mettre en majuscule les colonnes titre des deux DataFrames

df_imdb['Titre'] = df_imdb['Titre'].str.upper()
df_allocine['Titre'] = df_allocine['Titre'].str.upper()

df_imdb.head()
df_allocine.head()

#b) Merger les deux DataFrames en se basant sur la colonne 'Titre' en gardant uniquement les films en commun
df = pd.merge(df_imdb, df_allocine, on='Titre', how='inner')
df.head(10)

#C) 
# Le site avec les meilleurs notes
# selon les colonnes Note et Note spectateurs nous remarquons que c'est la colonne Note qui a des plus grandes valeurs
# ce qui fait que le site 1 a de plus grandes valeurs que le site 2.

