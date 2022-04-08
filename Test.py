from selenium import webdriver
from googleapiclient.discovery import build
from google.oauth2 import service_account

driver = webdriver.Chrome(executable_path="chromedriver.exe")

######
### DEFINITION DE FONCTION
######

def recup_info(name_player,last_game):
    driver.get(f"https://euw.op.gg/summoners/euw/{name_player}")
    update_last_game_sur_excel = True
    #print(name_player)
    # ATTETION si il y a moins de *20* games enregistrees sur OPGG le code bug parce que la liste n'est pas asser grande
    for i in range(10):
        #print(driver.find_elements_by_class_name('time-stamp')[i].text)        # date de la game
        #if driver.find_elements_by_class_name('time-stamp')[i].text == "a day ago":    # si la game s'est deroulee il y a un jour
        # des que l'on trouve la game qui correspond a la last_game de l'excel alors on brise la boucle et passe au joueur suivant
        if driver.find_elements_by_class_name('participants')[i].text.split() == last_game:
            break
        # Si la last_game notee dans l'excel est differente de celle trouvee sur le site alors on la mets dans la liste des game a updater
        else:
            # si la last_game n'a pas ete update alors on l'update
            if update_last_game_sur_excel:
                update_last_game_sur_excel = False
                # on ecrit dans l'excel la nouvelle game, le programme li en 1er les game plus recentes
                reactualise_laste_game([name_player, driver.find_elements_by_class_name('participants')[i].text.split()])
            nb_died_player = driver.find_elements_by_class_name('d')            # nombre de mort
            #print(nb_died_player[i].text
            ten_joueur = driver.find_elements_by_class_name('participants')     # nom des teamates
            #print(ten_joueur[i].text.split())
            liste_de_toute_les_game_dhier.append([name_player, int(nb_died_player[i].text), ten_joueur[i].text.split()])

def game_dans_liste(game, liste):
    compteur = 0
    for game_liste in liste:
        if game[2] == game_liste[2]:
            return True, compteur
        compteur += 1
    return False, compteur

def affiche_liste_game(liste):
    for i in liste:
        print(i)

def combien_on_incremente_mort(liste_de_game_unique):
    liste_joueur = []
    mort_associe = []
    for game in liste_de_game_unique:
        liste_auteur = game[0].split("-")
        for player in liste_auteur:
            if player not in liste_joueur:
                liste_joueur.append(player)
                mort_associe.append(game[1])
            else:
                mort_associe[liste_joueur.index(player)] += game[1]
    # affichage
    for i in range(0, len(liste_joueur)):
        print(f"Plus {str(mort_associe[i])} mort pour {liste_joueur[i]}")
    return liste_joueur, mort_associe

def reactualise_laste_game(game_a_update):
    phrase = ""
    for mot in game_a_update[1]:
        phrase += "'" + mot + "', "
    phrase = phrase[:-2]    # j'enleve les deux derniers caracteres qui correspond au ", "
    text = [[phrase]]
    if game_a_update[0] == "IArchyI":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L2", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

    elif game_a_update[0] == "Kyrillooss":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L3", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

    elif game_a_update[0] == "Lionely":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L4", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

    elif game_a_update[0] == "TirEuR De LitReS":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L5", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

    elif game_a_update[0] == "imperator120":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L6", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

    elif game_a_update[0] == "CHA ShaarLunn":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L7", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

    elif game_a_update[0] == "Akutari":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L8", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

    elif game_a_update[0] == "trerare":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L9", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

    elif game_a_update[0] == "Keepcalmbestrong":
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!L10", valueInputOption="USER_ENTERED",
                              body={"values":text}).execute()

######
### MAIN
######
player_list = "Lionely", "Kyrillooss", "IArchyI", "TirEuR De LitReS", "CHA ShaarLunn", "imperator120", "Akutari", "trerare", "Keepcalmbestrong"

### Capture d'info Google_shit
SERVICE_ACCOUNT_FILE = "key_REM_LOL.json"   # la clef d'acces pour acceder au googlesheet
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]   # l'acces a api de google

#creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ID de la google_sheet
id_googlesheet = "1GSFVRdKKlngaEL9oZ9V3qHwmw3fv6LOwtbDsnmFdAgo"

service = build("sheets", "v4", credentials=creds)

# On appel la googlesheet
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=id_googlesheet, range="Test_LOL!A1:L10").execute()
values = result.get("values", [])   # On recupere les valeurs de chaque case

# On affiche toutes les valeurs
#print(values)

liste_last_game = []
for player in player_list:
    for ligne in values:
        if player == ligne[0]:
            liste_last_game.append([ligne[11]])
#print(liste_last_game)

### Traitement
liste_de_toute_les_game_dhier = []

# on recupere toute les games de la veille
for player in player_list:
    last_game_av_traitement = liste_last_game[player_list.index(player)][0]
    last_game = ""
    for lettre in last_game_av_traitement:
        if lettre not in [",", "'"]:
            last_game += lettre
    recup_info(player, last_game.split())

#print(liste_de_toute_les_game_dhier)
affiche_liste_game(liste_de_toute_les_game_dhier)
print(f"Il y a eu {len(liste_de_toute_les_game_dhier)} nouvelles game")

# on check les games deux a deux pour regarder s'il y a des doublons (selon la liste des joueurs)
liste_partie_unique = []
initialisation_ok = False
# pour chaque game que l'on a fait hier
for game_check in liste_de_toute_les_game_dhier:
    # on la compare a chaque game que l'on considere unique (au debut il n'y en a aucune, donc on ajoute la 1ere game)
    if initialisation_ok:
        reponse = game_dans_liste(game_check, liste_partie_unique)  # permet de savoir si la game est deja dans la liste de game "unique"
        if reponse[0]:  # si oui
            # on ajoute le nom et le nb de mort, sans ajoute de game
            liste_partie_unique[reponse[1]][0] = liste_partie_unique[reponse[1]][0]+"-"+game_check[0]
            liste_partie_unique[reponse[1]][1] = liste_partie_unique[reponse[1]][1]+game_check[1]
        else: # si non
            # on ajoute la game a la liste de game unique
            liste_partie_unique.append(game_check)
    else:
        # on ajoute la 1ere game a la liste de game unique
        liste_partie_unique.append(game_check)
        initialisation_ok = True

affiche_liste_game(liste_partie_unique)
print(f"Il y a eu {len(liste_partie_unique)} nouvelles game unique")
liste_joueur, mort_associe = combien_on_incremente_mort(liste_partie_unique)

######
### MODIFICATION DU GOOGLE_SHEET
######

# liste des joueurs et case associe
# "IArchyI" C2, "Kyrillooss" C3, "Lionely" C4, "TirEuR De LitReS" C5, "imperator120" C6, "CHA ShaarLunn" C7, "Akutari" C8, "trerare" C9, "Keepcalmbestrong" C10
compteur_player = -1
for player in liste_joueur:
    compteur_player += 1
    if player == "IArchyI":
        text = [[mort_associe[compteur_player] + int(values[1][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C2", valueInputOption="USER_ENTERED", body={"values":text}).execute()
    
    elif player == "Kyrillooss":
        text = [[mort_associe[compteur_player] + int(values[2][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C3", valueInputOption="USER_ENTERED", body={"values":text}).execute()
    
    elif player == "Lionely":
        text = [[mort_associe[compteur_player] + int(values[3][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C4", valueInputOption="USER_ENTERED", body={"values":text}).execute()
    
    elif player == "TirEuR De LitReS":
        text = [[mort_associe[compteur_player] + int(values[4][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C5", valueInputOption="USER_ENTERED", body={"values":text}).execute()
    
    elif player == "imperator120":
        text = [[mort_associe[compteur_player] + int(values[5][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C6", valueInputOption="USER_ENTERED", body={"values":text}).execute()
    
    elif player == "CHA ShaarLunn":
        text = [[mort_associe[compteur_player] + int(values[6][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C7", valueInputOption="USER_ENTERED", body={"values":text}).execute()
    
    elif player == "Akutari":
        text = [[mort_associe[compteur_player] + int(values[7][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C8", valueInputOption="USER_ENTERED", body={"values":text}).execute()
    
    elif player == "trerare":
        text = [[mort_associe[compteur_player] + int(values[8][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C9", valueInputOption="USER_ENTERED", body={"values":text}).execute()

    elif player == "Keepcalmbestrong":
        text = [[mort_associe[compteur_player] + int(values[9][2])]]
        sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!C10", valueInputOption="USER_ENTERED",
                              body={"values": text}).execute()
