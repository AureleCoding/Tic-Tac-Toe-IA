import pygame
import random
# import time

pygame.init()

# Constantes
JOUEUR = 'x'
IA = 'o'

joueur_actuel = JOUEUR

lignes = [((200, 0), (200, 600)),
          ((400, 0), (400, 600)),
          ((0, 200), (600, 200)),
          ((0, 400), (600, 400))]

grille = [[None for x in range(3)] for y in range(3)]

# grille = [[None, 'o', 'x'],
#           [None, 'o', None],
#           ['o', None, 'x']]

# Initialisation de la fenêtre
fenetre = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Morpion IA')

font = pygame.font.Font(None, 80)

# Fonction pour afficher la grille
def afficher_grille():
    # Couleur du fond
    fenetre.fill((255, 255, 255))

    # Affichage des lignes de la grille
    for ligne in lignes:
        pygame.draw.line(fenetre, 'black', ligne[0], ligne[1], 3)

    # Affichage des coups joués sur la grille
    for y in range(0, len(grille)):
        for x in range(0, len(grille)):
            if grille[y][x] == JOUEUR:
                pygame.draw.line(fenetre, 'black', (x * 200 + 50, y *
                                 200 + 50), (150 + (x * 200), 150 + (y * 200)), 4)
                pygame.draw.line(fenetre, 'black', ((
                    x * 200) + 50, 150 + (y * 200)), (150 + (x * 200), (y * 200) + 50), 4)
            elif grille[y][x] == IA:
                pygame.draw.circle(
                    fenetre, 'black', (100 + (x * 200), 100 + (y * 200)), 50, 3)


def afficher_message(message):
    message_victoire = font.render(message, True, (255, 0, 0)) 
    text_message_victoire = message_victoire.get_rect(center=(fenetre.get_width() // 2, fenetre.get_height() // 2))
    fenetre.blit(message_victoire, text_message_victoire)

    message2 = 'Appuyer sur R \n pour relancer'
    ligne1, ligne2 = message2.split('\n')
    surface_ligne1 = font.render(ligne1, True, (255, 0, 0))
    surface_ligne2 = font.render(ligne2, True, (255, 0, 0))
    text_surface_ligne1 = surface_ligne1.get_rect(center=(fenetre.get_width() // 2, fenetre.get_height() // 1.3))
    text_surface_ligne2 = surface_ligne2.get_rect(center=(fenetre.get_width() // 2, fenetre.get_height() // 1.3+50))
    fenetre.blit(surface_ligne1, text_surface_ligne1)
    fenetre.blit(surface_ligne2, text_surface_ligne2)

# Fonction pour vérifier si la partie est terminée
def est_termine():
    # Vérifier les lignes
    for ligne in grille:
        if all(valeur == JOUEUR for valeur in ligne):
            return JOUEUR
        elif all(valeur == IA for valeur in ligne):
            return IA

    # Vérifier les colonnes
    for x in range(3):
        colonne = [grille[y][x] for y in range(3)]
        if all(valeur == JOUEUR for valeur in colonne):
            return JOUEUR
        elif all(valeur == IA for valeur in colonne):
            return IA

    # Vérifier les diagonales
    diagonale1 = [grille[i][i] for i in range(3)]
    diagonale2 = [grille[i][2-i] for i in range(3)]
    if all(valeur == JOUEUR for valeur in diagonale1) or all(valeur == JOUEUR for valeur in diagonale2):
        return JOUEUR
    elif all(valeur == IA for valeur in diagonale1) or all(valeur == IA for valeur in diagonale2):
        return IA

    # Vérifier si la grille est pleine
    if all(valeur != None for ligne in grille for valeur in ligne):
        return 0

    # Si aucun joueur n'a gagné et que la grille n'est pas pleine, le jeu continue
    return None


def minimax(grille, profondeur, joueur_max):
    # Si la profondeur de recherche est atteinte ou si le jeu est terminé, on retourne le score correspondant à l'état actuel de la grille
    if profondeur == 0 or est_termine() is not None:
        if est_termine() == IA:
            return 10
        elif est_termine() == JOUEUR:
            return -10
        else:
            return 0

    # On initialise le score optimal avec la plus petite valeur possible pour l'IA et la plus grande valeur possible pour le vrai joueur
    if joueur_max:
        meilleur_score = float('-inf')
    else:
        meilleur_score = float('inf')

    # On parcourt toutes les cases vides de la grille
    for y in range(3):
        for x in range(3):
            if grille[y][x] is None:
                # On joue un coup dans la case actuelle
                if joueur_max:
                    grille[y][x] = IA
                else:
                    grille[y][x] = JOUEUR
                # On appelle récursivement minimax() avec une profondeur réduite et en inversant le joueur actuel
                score = minimax(grille, profondeur-1, not joueur_max)
                # On annule le coup joué précédemment
                grille[y][x] = None

                # On met à jour le score optimal selon que l'on est en train de maximiser ou minimiser (max pour l'IA, min pour le vrai joueur)
                if joueur_max:
                    meilleur_score = max(meilleur_score, score)
                else:
                    meilleur_score = min(meilleur_score, score)
    # On retourne le score optimal trouvé
    return meilleur_score


def meilleurs_coups(grille):
    # Initialisation des variables
    meilleurs_coups = []  # liste des meilleurs coups
    meilleur_score = float('-inf')  # initialisation du meilleur score
    # Parcours de la grille
    for y in range(3):
        for x in range(3):
            # Si la case est vide
            if grille[y][x] is None:
                # On joue le coup
                grille[y][x] = IA
                # On évalue le score du coup avec l'algorithme minimax
                score = minimax(grille, 5, False)
                # On annule le coup
                grille[y][x] = None
                # Si le score est meilleur que le meilleur_score actuel
                if score > meilleur_score:
                    # On crée une nouvelle liste avec le nouveau meilleur score
                    meilleurs_coups = [(y, x)]
                    # On met à jour le meilleur score
                    meilleur_score = score
                # Si le score est égal au meilleur_score actuel
                elif score == meilleur_score:
                    # On ajoute le coup à la liste des meilleurs coups
                    meilleurs_coups.append((y, x))
    # On renvoie un des meilleurs coups au hasard
    return meilleurs_coups


# Boucle de jeu
est_lance = True

while est_lance:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            est_lance = False

        elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_r and est_termine() is not None:
            grille = [[None for x in range(3)] for y in range(3)]
            joueur_actuel = JOUEUR

        elif est_termine() is None:
            if evenement.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and joueur_actuel == JOUEUR:
                # Obtenir la position de la souris
                position = pygame.mouse.get_pos()
                X_POS, Y_POS = position[0]//200, position[1]//200

                # Implémenter le coup
                if grille[Y_POS][X_POS] == None:
                    grille[Y_POS][X_POS] = JOUEUR
                    # Passer le tour au joueur suivant
                    joueur_actuel = IA

            elif joueur_actuel == IA and meilleurs_coups(grille) and est_termine() is None:

                # t1_start = time.perf_counter()

                # L'IA joue
                Y_POS, X_POS = random.choice(meilleurs_coups(grille))

                # t1_stop = time.perf_counter()

                # print("Temps:", t1_stop-t1_start)

                # Implémenter le coup
                if grille[Y_POS][X_POS] == None:
                    grille[Y_POS][X_POS] = IA
                    # Passer le tour au joueur suivant
                    joueur_actuel = JOUEUR

    # Afficher la grille à chaque tour de boucle
    afficher_grille()

    # Vérifier si la partie est terminée
    resultat = est_termine()
    if resultat is not None:
        if resultat == JOUEUR:
            afficher_message("Le vrais joueur a gagné !")
        elif resultat == IA:
            afficher_message("L'IA a gagné !")
        else:
            afficher_message("Match nul !")

    # Actualise la fenettre
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
