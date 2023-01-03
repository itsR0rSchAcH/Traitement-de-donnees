import math
from math import sin, cos, acos, sqrt

import branca
import folium
import numpy as np
from matplotlib import pyplot


def extraction_villes_csv(fichier):
    """
    @exercice : 1.3
    @fonction1: Extrait chaque ligne du fichier et les stoque dans une liste

    :param fichier: Nom du fichier dont on veux extraire les lignes         type: str
    :return: Chaque élément vaut une ligne du fichier                       type: list
    """
    fich = open(fichier, 'r')
    liste_villes = []
    ville = fich.readline()                                                                            # Lit la 1er ligne du fichier, et les item de cette ligne comme un élément de la liste
    while ville:                                                                                       # Tant que la ligne de ville contient quelquechose on effectue :
        liste_villes.append(ville.replace('"', "").replace("\n", "").replace("NULL", "0").split(','))  # On suppr les quot, saut de ligne; on replace NULL par 0 pour ne pas avoir de future out of range;; On ajoute cette liste(qui contient la premier ligne ici OZAN) comme un item a la liste globale
        ville = fich.readline()                                                                        # On remplace la ligne actuel par la suivante
    fich.close()
    return liste_villes

def extract_infos_villes(uneListe):
    """
    @exercice : 1.4
    @fonction1: Extraire les 12 information de liste globale

    :param uneListe: (liste globale) contient chaque ligne du fichierles villes (1.3 extraction_villes_csv(fichier))
    :type: list

    :return: liste avec seulement les 12 infos demander
    :type: list
    """
    listeinfo = []
    infos = []
    liste_index = [1, 3, 8, 14, 15, 16, 17, 18, 19, 20, 25, 26]             # Contient les indexs des 12 infos a recuperer
    for i in range(len(uneListe)):                                          # Pour chaque element de la liste globale
        infos = []                                                          # Réinitialise la liste a jouter pour chaque villes
        for j in range(len(liste_index)):                                   # La boucle permet de reccuperer les info sur chaque élément de la liste global
            if j > 6 and j < 10:
                infos.append(float(uneListe[i][liste_index[j]]))            # Ajoute le contenue de l'information correspondant a l'index a recup dans info suivant son type
            elif j > 2:
                infos.append(int(uneListe[i][liste_index[j]]))
            else:
                infos.append(str(uneListe[i][liste_index[j]]))
        listeinfo.append(infos)                                             # La sous-liste est traiter on ajoute son resultat sous la forme d'un element de la liste globale
    return listeinfo

def extract_villes_depart_indicatif(listeDept, listeInfo):
    """
    @exercice : 1.5
    @fonction1: Retourne le nombre de ville pour indicatif téléphonique 05
    @fonction2: Crée SO05.txt, qui contient "nom de la ville, numéro departement"

    :param listeDept: Liste des départements pour indicatif téléphonique 05
    :type : list

    :param listeInfo: Info des 12  informations retenues pour  chaque  ville. (1.4 extract_infos_villes(uneListe) )
    :type : list

    :return NbrDeVille: Le nombre de ville pour indicatif téléphonique 05
    :type : int
    """
    NbrDeVille = 0
    fich = open("SO05.txt", "w")
    for ville in listeInfo:                                # Pour chaque élément(ville) de la liste listeInfo
        if ville[0] in listeDept:                          # Si le numéro de département est contenue dans la liste des départements
            ajout = ville[1] + " (" + ville[0] + ")" + "\n"# Mise en forme de chaque ligne de S005.txt, NomDeLaVille(NumeroDuDepartement)
            fich.write(ajout)                              # Ecriture de ajout dans le fichier texte
            NbrDeVille += 1
    fich.close()
    return NbrDeVille

def extract_villes_NumDepart(numDept,  listeInfo):
    """
    @exercice : 2.1
    @fonction1: Retourne le nombre de ville du département 32 + la liste des infos pour ces villes
    @fonction2: Crée ville_32.txt, qui contient "nom de la ville, numéro departement"

    :param listeInfo: 12  informations retenues pour chaque ville. (1.4 extract_infos_vooilles(uneListe))
    :type: list

    :param numDépt: (MonDepartement) 32
    :type : int

    :return NbVille: Nombre de ville du departement 32
    :type: int

    :return listeinfo: Infos pour les villes du departement 32
    :type: list
    """
    nom = "ville_" + str(numDept) + ".txt"
    fich = open(nom, "w")
    NbVille = 0
    listeInfo32 = []
    for ville in listeInfo:                 # la boucle effectue 4 action :
        if ville[0] == str(numDept):        # 1) On vérifie si le numéro de département correspond a celui demandé
            NbVille += 1                    # 2) On incremente de 1 le compteur de villes du departement demandé
            fich.write(str(ville)+"\n")     # 3) On ajoute la sous-liste actuel (ville) au fichier avec un saut de ligne
            listeInfo32.append(ville)       # 4) On ajoute la ligne entiere si le departement correspond dans la liste a retourné
    fich.close()
    return NbVille, listeInfo32



def MinMax5Villes_Habitants(numDept, listeInfoDept):
    """
    !!! ATTENTION !!! Les villes LAURET et MONGET ont le meme nombre d'hab en 2010 pour le departement 40
    @exercice : 2.2 a)
    @fonction2: Crée Top5Villes_32.txt, qui contient les 5 villes et leur information ayant le plus dhabitant en 2010 du département 32
    @fonction2: Crée Min5Villes_32.txt, qui contient les 5 villes et leur information ayant le moins dhabitant en 2010 du département 32

    :param numDépt: (MonDepartement) 32
    :type : int

    :param listeInfoDept: Contient les 12 infos, des villes du fichier villefrance.csv (2.1 extract_ville_Depart(listeInfo, numDépt))
    :type listeInfoDept: list


    """
    Inutile, ListeDesInfoDuDepart = extract_villes_NumDepart(numDept,  listeInfoDept)

    echange = True                                                          # La variable echange permet de savoir si une permutation a eu lieux
    while echange:
        echange = False                                                     # Si aucun echange n'a lieux pendant 1 tour de la boucle la liste est trier
        for i in range(len(ListeDesInfoDuDepart) - 1):
            if ListeDesInfoDuDepart[i][3] < ListeDesInfoDuDepart[i + 1][3]: # Si le nombre d'habitant en 2010 de l'élément suivant est plus grand
                ListeDesInfoDuDepart[i], ListeDesInfoDuDepart[i + 1] = ListeDesInfoDuDepart[i + 1], ListeDesInfoDuDepart[i] # On intervertie les ligne de la liste
                echange = True                                              # Comme un echange a eu lieux alors on reparcout la liste

    fichMax = open(f"Top5Villes_{numDept}.txt", "w", encoding="utf8")
    fichMin = open(f"Min5Villes_{numDept}.txt", "w", encoding="utf8")

    for j in range(1, 6):
        taille = len(ListeDesInfoDuDepart)
        fichMax.write(f"{ListeDesInfoDuDepart[j - 1]}\n")                   # On ecrit les 5 premiere villes le fichier Top5Villes_32.txt en partant du debut
        fichMin.write(f"{ListeDesInfoDuDepart[taille - j]}\n")              # On ecrit les 5 derniere villes le fichier Min5Villes_32.txt en partant de la fin de la liste
    fichMax.close()
    fichMin.close()

def MinMax5Villes_Habitants_formater(numDept, listeInfoDept):
    """
    BONUS AVEC FORMATAGE DE TEXT MAIS INUTILISABLE POUR LA SUITE DE LA SAE

    """
    Inutile, ListeDesInfoDuDepart = extract_villes_NumDepart(numDept,  listeInfoDept)

    echange = True
    while echange:
        echange = False
        for i in range(len(ListeDesInfoDuDepart) - 1):
            if ListeDesInfoDuDepart[i][3] < ListeDesInfoDuDepart[i + 1][3]:
                ListeDesInfoDuDepart[i], ListeDesInfoDuDepart[i + 1] = ListeDesInfoDuDepart[i + 1], ListeDesInfoDuDepart[i]
                echange = True

    fichMax = open(f"Top5Villes_{numDept}_bonus.txt", "w", encoding="utf8")
    fichMin = open(f"Min5Villes_{numDept}_bonus.txt", "w", encoding="utf8")

    fichMin.write("{:<16} {:<16} {:<16} {:<16} {:<16}\n=====================================================================================".format('Position', 'Habitant', 'Ville', 'Superficie(km\u00b2)', 'Densité(hab/km\u00b2)'))
    fichMax.write("{:<16} {:<16} {:<16} {:<16} {:<16}\n=====================================================================================".format('Position', 'Habitant', 'Ville', 'Superficie(km\u00b2)', 'Densité(hab/km\u00b2)'))

    for j in range(1, 6):
        taille = len(ListeDesInfoDuDepart)
        fichMax.write("\n {:<16} {:<16} {:<16} {:<16} {:<16}".format(j, ListeDesInfoDuDepart[j-1][3], ListeDesInfoDuDepart[j-1][1], ListeDesInfoDuDepart[j-1][2], ListeDesInfoDuDepart[j-1][3]))
        fichMin.write("\n {:<16} {:<16} {:<16} {:<16} {:<16}".format(j, ListeDesInfoDuDepart[taille-j][3], ListeDesInfoDuDepart[taille-j][1], ListeDesInfoDuDepart[taille-j][2], ListeDesInfoDuDepart[taille-j][3]))
    fichMax.close()
    fichMin.close()



def mapTenVilles(nomFich1,nomFich2):
    """
    @exercice : 2.2 b)
    @fonction1: Place sur une carte les points des villes extraite dans les fichiers Top5Villes_32.txt et Min5Villes_32.txt
               avec un cercle propotionel a leur densité.
    @fonction2: Le cercle sera de couleur plus ou moins intense en fonction de la population

    :param nomFich1: nom du fichier contenant les 5 villes ayant le plus d'habitant en 2010 (2.2.a MinMax5Villes_Habitants(numDept, listeInfoDept) )
    :type: str

    :param nomFich2: nom du fichier contenant les 5 villes ayant le moins d'habitant en 2010 (2.2.a MinMax5Villes_Habitants(numDept, listeInfoDept) )
    :type: str
    """
    Top5Villes = open(nomFich1,'r')
    Min5Villes = open(nomFich2,'r')

    listeTop = Top5Villes.readlines()                                                                  # On extrait les inforamtions des fichier passé en param sous forme de liste
    listeMin = Min5Villes.readlines()

    Top5Villes.close()
    Min5Villes.close()

    for i in range(len(listeMin)):          # cette boucle formate la liste recupérer pour pouvoir rendre les donnée utilisable
        formatage = listeTop[i].replace("\"", "").replace("\'", "").replace("[", "").replace("]", "")  #Supprime élément inutile générer par readlines
        listeTop[i] = formatage.strip()                                                                #Supprime espace inutile au début et fin du readlines
        listeTop[i] = listeTop[i].split(",")                                                           #Separe chaque élément par une virgule

        formatage = listeMin[i].replace("\"", "").replace("\'", "").replace("[", "").replace("]", "")  #Supprime élément inutile générer par readlines
        listeMin[i] = formatage.strip()                                                                #Supprime espace inutile au début et fin du readlines
        listeMin[i] = listeMin[i].split(",")                                                           #Separe chaque élément par une virgule

    listeLong = []                                      # Initilisation des 3 listes (longitude, latitude et densité)
    listeDens = []
    listeLat = []
    listeHab = []

    for i in range(len(listeMin)):                      # Permet d'ajouter au liste les 3 information recuperer du fichier texte
        listeDens.append(float(listeMin[i][6]))
        listeLong.append(float(listeMin[i][8]))
        listeLat.append(float(listeMin[i][9]))
        listeHab.append(float(listeMin[i][5]))

        listeDens.append(float(listeTop[i][6]))
        listeLong.append(float(listeTop[i][8]))
        listeLat.append(float(listeTop[i][9]))
        listeHab.append(float(listeTop[i][5]))

    coords = (43.650000, 0.583333)
    map = folium.Map(location=coords,               # Correspond au point central de la carte lors de l'affichage
                     zoom_start=9)                  # Zoom du départ

    cm = branca.colormap.LinearColormap(['blue', 'red'],                     # Couleur du dégradé
                                        vmin=min(listeDens),                 # Minimum de la legende
                                        vmax=max(listeDens),                 # Maximum de la legende
                                        caption="Habitant en 2012")          # Description de la legende
    map.add_child(cm)

    for i in range(len(listeDens)):
        folium.CircleMarker(
            location=(listeLat[i], listeLong[i]),                           # Coordonné du point a placer
            radius=math.log(listeDens[i], 1.5),                                        # Cercle de rayon proportionnel a la densité
            color=cm(listeDens[i]),                                         # Couleur du contour du cercle
            fill=True,
            fill_color=cm(listeDens[i]),                                    # Couleur de l'interieur du cercle
            fill_opacity=0.6                                                # Oppacité de l'interieur du cercle
        ).add_to(map)                                                       # Ajoute le tout (cercle, point sur la carte) a l'élément parent
    map.save(outfile='mapTenVilles.html')                                   # Enregistre la carte dans le fichier


def MinMax10Accroissement(listeInfo, Departement):
    """
    @exercice : 2.2 c)
    @fonction1: Sauvegarder dans un fichier (TopAcc10Villes_32.txt et MinAcc10Villes_32.txt) les 10 villes qui ont eu le plus fort/ faible
                accroissement de population entre 1999 et 2012.

    :param listeInfo: Contient les 12 infos, des villes du fichier villefrance.csv (2.1 extract_ville_Depart(listeInfo, numDépt))
    :type: list

    :param Departement: Numéro du département souhaité (32)
    :type: int
    """
    infodudep = []
    for i in range(len(listeInfo)):
        if listeInfo[i][0] == str(Departement):                 # Verifie si le département correspond bien
            accroissement = listeInfo[i][5] - listeInfo[i][4]   # Calcule l'accroissement
            listeInfo[i].append(accroissement)                  # Ajoute l'accroissement en tant que 13 eme élément de la sous-liste
            infodudep.append(listeInfo[i])                      # Ajoute la ligne correspondant dans "infodudep" qui sera utilisé par la suite

    echange = True
    while echange:                                              # Permet trier le tableau en fonction de l'accroissment (décroissant)
        echange = False
        for i in range(len(infodudep) - 1):
            if infodudep[i][12] < infodudep[i + 1][12]:
                infodudep[i], infodudep[i + 1] = infodudep[i + 1], infodudep[i]
                echange = True

    fich=open(f"TopAcc10Villes_{Departement}.txt","w")
    for i in range(9,-1, -1):                                               # Inscrit les 10 villes avec le plus fort taux d'accroissement
        chaine= f"{infodudep[i][0]},{infodudep[i][1]},{infodudep[i][12]}\n"
        fich.write(chaine)
    fich.close()

    fich2=open(f"MinAcc10Villes_{Departement}.txt","w")
    for i in range(10, 0, -1):                                              # Inscrit les 10 villes avec le faible fort taux d'accroissement
        taille = len(infodudep)
        chaine = f"{infodudep[taille - i][0]},{infodudep[taille - i][1]},{infodudep[taille - i][12]}\n"
        fich2.write(chaine)
    fich2.close()


def traceHistoVilles(listeInfoDept):
    """
    @exercice : 3.1
    @fonction1: Crée un histogramme du nombre de villes en fonction du nombre d’habitants en 2010
    @fonction2: Affiche en console la moyenne d'habitant du departement
    @fonction3: Affiche en console l'ecart type du nombre d'habitant

    :param listeInfoDept:
    :type: list
    """
    listeDuNbrHab = []
    for i in range(len(listeInfoDept)):                                        # Permet d'extraire le nombre d'habitant en 2010 et le stoquer dans une liste (listeDuNbrHab)
        nbrhab = listeInfoDept[i][3]
        listeDuNbrHab.append(nbrhab)

    pyplot.hist(listeDuNbrHab,                                                 # Correspond au x, au donné qui vont etre repartie sur l'histograme
                   bins=100,                                                   # Nombre de classe en y
                   color='yellow',
                   edgecolor='red')
    pyplot.xlabel("Nombre de d'habitant")                                      # Legende
    pyplot.ylabel('Nombre de villes')
    pyplot.title(f'Département {MonDep} : Nombre de villes en fonction des Habitants') # Titre
    pyplot.show()                                                               # Affichage de l'histogramme

    print(f"La moyenne du département {MonDep} est de {sum(listeDuNbrHab)/len(listeDuNbrHab)} habitants par villes.")
    print(f"L'ecart type du departement est de {np.std(listeDuNbrHab)}\n")

def MinMax5Alt_Dept(listeInfoDept):
    """
    @exercice : 3.2
    @fonction1: Sauvegarde le département, le nom de la ville, la latitude, la longitude et la différence d’altitude
                des 5 villes qui ont la plus forte différence d’altitude dans Top5Alt_32.txt
    @fonction2: Sauvegarde le département, le nom de la ville, la latitude, la longitude, et la différence d’altitude
                des 5 villes qui ont la plus faible différence d’altitude dans Min5Alt_32.txt

    :param listeInfoDept: Contient la liste des 12 info pour mon departement. (32)
    :type: list

    sauvegarder le nom des 5 villes qui ont la plus forte(respectivement la plus faible) différence d’altitude
    """
    NewListe = []
    for ville in listeInfoDept:                                                                            # Ajoute la difference d'altitude en tant que 11eme élément de la liste
        if ville[0] == str(MonDep):
            ville[10] = ville[11] - ville[10]
            NewListe.append(ville)

    echange = True
    while echange:                                                                                         # Trie la liste en fonction de la difference d'altitude (décroissant)
        echange = False
        for i in range(len(NewListe) - 1):
            if NewListe[i][10] < NewListe[i + 1][10]:
                NewListe[i], NewListe[i + 1] = NewListe[i + 1], NewListe[i]
                echange = True

    fich = open(f"Top5Alt_{MonDep}.txt", "w")
    for i in range(4, -1, -1):                                                                              # Inscrit les 10 villes avec la plus forte difference d'altitude
        chaine = f"{NewListe[i][0]},{NewListe[i][1]},{NewListe[i][9]},{NewListe[i][8]},{NewListe[i][10]}\n"
        fich.write(chaine)
    fich.close()

    fich2 = open(f"Min5Alt_{MonDep}.txt", "w")
    for j in range(5, 0, -1):                                                                                  # Inscrit les 10 villes avec la plus faible difference d'altitude
        taille = len(NewListe)
        chaine = f"{NewListe[taille - j][0]},{NewListe[taille - j][1]},{NewListe[taille - j][9]},{NewListe[taille - j][8]},{NewListe[taille - j][10]}\n"
        fich2.write(chaine)
    fich2.close()

def mapTenAlt(nomfich3, nomfich4):
    """
    @exercice : 3.3
    @fonction1: Affiche les 10 villes des fichier TopAcc10Villes_32.txt et MinAcc10Villes_32.txt sur OpenStreetMap,
                avec des couleurs différentes en fonction de l’altitude.

    :param nomfich3: Correspond au nom du fichier crée lors de MinMax5Alt_Dept(listeInfoDept) Top5Alt_32.txt
    :type: str

    :param nomfich4: Correspond au nom du fichier crée lors de MinMax5Alt_Dept(listeInfoDept) Min5Alt_32.txt
    :type:str

    """
    Top5Villes = open(nomfich3,'r')
    Min5Villes = open(nomfich4,'r')

    listeTop = Top5Villes.readlines()                                                                  # On extrait les inforamtions des fichier passé en param sous forme de liste
    listeMin = Min5Villes.readlines()

    Top5Villes.close()
    Min5Villes.close()

    for i in range(len(listeMin)):          # cette boucle formate la liste recupérer pour pouvoir rendre les donnée utilisable
        formatage = listeTop[i].replace("\"", "").replace("\'", "").replace("[", "").replace("]", "")  #Supprime élément inutile générer par readlines
        listeTop[i] = formatage.strip()                                                                #Supprime espace inutile au début et fin du readlines
        listeTop[i] = listeTop[i].split(",")                                                           #Separe chaque élément par une virgule

        formatage = listeMin[i].replace("\"", "").replace("\'", "").replace("[", "").replace("]", "")  #Supprime élément inutile générer par readlines
        listeMin[i] = formatage.strip()                                                                #Supprime espace inutile au début et fin du readlines
        listeMin[i] = listeMin[i].split(",")                                                           #Separe chaque élément par une virgule

    listeLong = []                                      # Initilisation des 3 listes (longitude, latitude et densité)
    listeLat = []
    listeAlt = []

    for i in range(len(listeMin)):                      # Permet d'ajouter au liste les 3 information recuperer du fichier texte
        listeLong.append(float(listeMin[i][3]))
        listeLat.append(float(listeMin[i][2]))
        listeAlt.append(float(listeMin[i][4]))

        listeLong.append(float(listeTop[i][3]))
        listeLat.append(float(listeTop[i][2]))
        listeAlt.append(float(listeTop[i][4]))

    coords = (43.650000, 0.583333)
    m = folium.Map(location=coords,               # Correspond au point central de la carte lors de l'affichage
                   tiles='OpenStreetMap',
                   zoom_start=9)                  # Zoom du départ

    cm = branca.colormap.LinearColormap(['blue', 'red'],                     # Couleur du dégradé
                                        vmin=min(listeAlt),                  # Minimum de la legende
                                        vmax=max(listeAlt),                  # Maximum de la legende
                                        caption="Difference daltitude en metre")          # Description de la legende!!! Ne supporte par accent et quot!!!!
    m.add_child(cm)



    for i in range(len(listeAlt)):
        folium.CircleMarker(
            location=(listeLat[i], listeLong[i]),                           # Coordonné du point a placer
            radius=math.log(listeAlt[i], 1.5),                              # Rayon du cercle
            color=cm(listeAlt[i]),                                          # Couleur du contour du cercle
            fill=True,
            fill_color=cm(listeAlt[i]),                                     # Couleur de l'interieur du cercle
            fill_opacity=0.6                                                # Oppacité de l'interieur du cercle
        ).add_to(m)                                                         # Ajoute le tout (cercle, point sur la carte) a l'élément parent
    m.save(outfile='mapAltTenVilles.html')

def rechercheVille(ville1, listeInfo):
    """
    @exercice : 4.1
    @fonction1: 12 informations de la ville passée en paramètre

    :param ville1: Nom de la ville (non sensible a la casse)
    :type: str

    :param listeInfo: Contient les 12 infos, des villes du fichier villefrance.csv (2.1 extract_ville_Depart(listeInfo, numDépt))
    :type: list

    :return: 12 informations de la ville1 passée en paramètre
    :type: list
    """
    VilleMaj1 = ville1.upper()              # Permet de comparer avec le premier element de liste info
    i = 0

    Stop = False
    InfoVille1 = []

    while Stop == False:
        VilleActuel = listeInfo[i]
        if VilleActuel[1] == VilleMaj1:     # Si la ville correspond a celle demander
            InfoVille1 = (VilleActuel)      # On l'ajoute a la liste a renvoyer
        if InfoVille1 != [] or i == 36699:  # Si on trouver la ville demander ou que le nombre max de villes du fichier est atteint on sort du while
            Stop = True
        i += 1
    return InfoVille1

def dist_Euclidienne(ville1,  ville2):
    """
    http://www.movable-type.co.uk/scripts/latlong.html  (source de l'algo)
    @exercice : 4.2
    @fonction1: Donne la distance euclidienne entre les villes demandés

    :param ville1:
    :type: str

    :param ville2:
    :type: str

    :return: La distance euclidienne en km.
    :type: float
    """

    infoville1 = rechercheVille(ville1, ListeInfo)
    infoville2 = rechercheVille(ville2, ListeInfo)

    Lat1 = infoville1[9]*(math.pi / 180 )            # On convertie en radian la latitude et longitude donné en degrès
    Long1 = infoville1[8]*(math.pi / 180)            # Formule : radian = degres x (pi/180)

    Lat2 = infoville2[9]*(math.pi / 180)
    Long2 = infoville2[8]*(math.pi / 180)

    x = (Long2 - Long1) * cos((Lat1 + Lat2) / 2)
    y = (Lat2 - Lat1)
    RayonTerre = 6378.137                          # En km
    dist = sqrt(x**2 + y**2)                    # On mutiplie par le rayon de la terre
    return RayonTerre*dist


    # infoville1 = rechercheVille(ville1, ListeInfo) # On extrait les info des 2 villes demandé
    # infoville2 = rechercheVille(ville2, ListeInfo)
    #
    # Lat1 = infoville1[9]*(math.pi / 180 )            # On convertie en radian la latitude et longitude donné en degrès
    # Long1 = infoville1[8]*(math.pi / 180)            # Formule : radian = degres x (pi/180)
    #
    # Lat2 = infoville2[9]*(math.pi / 180)
    # Long2 = infoville2[8]*(math.pi / 180)
    #
    # coord1 = np.array((Lat1, Long1))               # On place les coordoné de latitude et longitude dans une liste copatible avec numphy pour la suite du calcule type: ndarray
    # coord2 = np.array((Lat2, Long2))
    # dist = np.sqrt(np.sum(np.square(coord2 - coord1))) # On applique la formule de la distance euclidienne
    # RayonTerre = 6378.137                          # En km
    # return dist*RayonTerre                         # On mutiplie par le rayon de la terre

# def dist_Geodesique2(ville1 , ville2):
#     """
#     http://www.movable-type.co.uk/scripts/latlong.html  (source de l'algo)
#     @exercice : 4.2 BONUS
#     @fonction1: Donne la distance euclidienne entre les villes demandés
#
#     :param ville1:
#     :type: str
#
#     :param ville2:
#     :type: str
#
#     :return: La distance euclidienne en km.
#     :type: float
#     """
#     city1 = rechercheVille(ville1,ListeInfo)
#     city2 = rechercheVille(ville2,ListeInfo)
#
#     Lat1 = city1[9] * math.pi / 180
#     Lat2 = city2[9] * math.pi / 180
#
#     Phi = (Lat2 - Lat1)
#     delt = (city2[8]-city1[8]) * math.pi / 180
#
#     a = sin(Phi / 2) * sin(Phi / 2) + cos(Lat1) * cos(Lat2) * sin(delt / 2) * sin(delt / 2)
#     dist = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#     RayonTerre = 6378.137                          # En km
#     return RayonTerre*dist


def dist_Geodesique(ville1 , ville2):
    """
    @exercice : 4.2
    @fonction1: Donne la distance euclidienne entre les villes demandés

    :param ville1:
    :type: str

    :param ville2:
    :type: str

    :return: La distance euclidienne en km.
    :type: float
    """
    city1 = rechercheVille(ville1, ListeInfo)
    city2 = rechercheVille(ville2, ListeInfo)

    Lat1 = city1[9]*(math.pi / 180)

    Lat2 = city2[9]*(math.pi / 180)

    RayonTerre = 6378.137
    Phi = acos(sin(Lat1) * sin(Lat2) + cos(Lat1) * cos(Lat2) * cos((city2[8] - city1[8])*(math.pi / 180)))

    return Phi * RayonTerre

#--------------------------------------------------------
# Procédure qui permet d'appeler la fonction
# qui permet d'extraire les informations sur les villes
#---------------------------------------------------------

def afficheMENU():
    print("\n================ MENU ==================")
    print("taper 1: Extraire des statistiques des Villes d'un département")
    print("taper 2: Distance Euclidienne et Géodésique entre 2 villes")
    print("taper 3: Plus court chemin entre 2 villes")
    print("F: pour finir")


def afficheSOUS_MENU_STATISTIQUE():
    print("\n================ SOUS MENU : STATISTIQUES ==================")
    print("taper 1: Lister les 5 Villes ayant le plus/ le moins d'habitants")
    print("taper 2: Afficher les 10 Villes en fonction de la DENSITE sur une carte")
    print("taper 3: Lister les 10 Villes ayant le plus fort/faible taux d'accroissement")
    print("taper 4: HISTOGRAMME des villes par habitants")
    print("taper 5: Lister les 5 Villes ayant la différence d'altitude max/min")
    print("taper 6: Afficher les 10 Villes en fonction de l'ALTITUDE sur une carte")
    print("Q: pour Quitter le sous-menu")

def afficheSOUS_SOUS_MENU_STATISTIQUE():
    print("\n================ SOUS MENU : STATISTIQUES/5 Villes ayant le plus/moins ==================")
    print("taper 1: Lister les 5 Villes ayant le plus/ le moins d'habitants")
    print("taper 2: Lister les 5 Villes ayant le plus/ le moins d'habitants avec formatage de texte")
    print("Q: pour Quitter le sous-sous-menu")


# Programme principal
# Appel de la procédure afficheMENU()
fini = False
MonDep = int(input("Entrer le departement que vous souhaitez (celui qui m'est attribué est le 32) : "))
print("\nExtraction des informations des Villes de France\n")
uneListe = extraction_villes_csv("villes_france.csv")
ListeInfo = extract_infos_villes(uneListe)

listeDepts = ['09', '12', '16', '17', '19', '23', '24', '31', '32', '33', '40', '46', '47', '64', '65',
              '79', '81', '82', '86', '87', '971', '972', '973', '975', '977', '978']
nbr = extract_villes_depart_indicatif(listeDepts, ListeInfo)
print("Retrouver la liste des villes de l'indicatif téléphonique 05 dans le fichier 'SO05.txt'")
print(f"l'indicatif téléphonique numéro 5 contient {nbr} villes\n")


NbVilleDep, ListeInfoDep = extract_villes_NumDepart(MonDep, ListeInfo)
print(f"Retrouver la liste des villes du departement {MonDep} dans 'villes_{MonDep}.txt'")
print(f"Le département numéro {MonDep} contient {NbVilleDep} villes\n")




while fini == False:
    afficheMENU()
    choix = input("votre choix: ")
    if choix == '1':
        finiBis = False
        while finiBis == False:
            afficheSOUS_MENU_STATISTIQUE()
            choixBis = input("votre choix: ")
            if choixBis == '1':
                finiBisBis = False
                while finiBisBis == False:
                    afficheSOUS_SOUS_MENU_STATISTIQUE()
                    choixBisBis = input("votre choix.: ")
                    if choixBisBis == '1':
                        MinMax5Villes_Habitants(MonDep, ListeInfo)
                        print(f"\nRetrouver les 5 Villes ayant le plus/ le moins d'habitants dans 'Top5Villes_{MonDep}.txt' et 'Min5Villes_{MonDep}.txt'\n")
                    elif choixBisBis == '2':
                        MinMax5Villes_Habitants_formater(MonDep, ListeInfo)
                        print(f"\nRetrouver les 5 Villes ayant le plus/ le moins d'habitants dans 'Top5Villes_{MonDep}+.txt' et 'Min5Villes_{MonDep}+.txt'\n")
                    elif choixBisBis == 'Q' or choixBisBis == 'q':
                        finiBisBis = True
            elif choixBis == '2':
                print("\nAffichage les 10 Villes en fonction de la DENSITE sur mapTenVilles.html\n")
                MinMax5Villes_Habitants(MonDep, ListeInfo)
                mapTenVilles(f'Top5Villes_{MonDep}.txt', f'Min5Villes_{MonDep}.txt')
            elif choixBis == '3':
                print(f"\nLister les 10 Villes ayant le plus fort/faible taux d'accroissement dans MinAcc10Villes_{MonDep}.txt et MinAcc10Villes_{MonDep}.txt\n")
                MinMax10Accroissement(ListeInfo, MonDep)
            elif choixBis == '4':
                traceHistoVilles(ListeInfoDep)
            elif choixBis == '5':
                MinMax5Alt_Dept(ListeInfo)
            elif choixBis == '6':
                MinMax5Alt_Dept(ListeInfo)
                mapTenAlt(f"Top5Alt_{MonDep}.txt", f"Min5Alt_{MonDep}.txt")
            elif choixBis == 'Q' or choixBis == 'q':
                finiBis = True

    elif choix == '2':
        v1 = input("Enter le nom de la 1er ville (Taper N : Pour Nantes) : ")
        if v1 == "N" or v1 == "n":
            v1 = "Nantes"
        v2 = input("Enter le nom de la 2eme ville (Taper N : Pour Nice) : ")
        if v2 == "N" or "n":
            v2 = "Nice"
        dist = dist_Euclidienne(v1, v2)
        dist2 = dist_Geodesique(v1, v2)
        print(f"La distance euclidienne entre {v1} et {v2} est de {round(dist, 2)}km.")
        print(f"La distance géodesique est de {round(dist2, 2)}km.")
    elif choix == '3':
        print('3')

    elif choix == 'F' or choix == 'f':
        fini = True

print("Fin du programme")