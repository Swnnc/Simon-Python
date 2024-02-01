import pygame
import sys

pygame.init()

largeur, hauteur = 950, 550
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("|| ==================================== Game Over ==================================== ||")

fond_image = pygame.image.load("images/GameOver.png")
fond_image = pygame.transform.scale(fond_image, (largeur, hauteur))

# Boucle principale du menu
while True:
    ecran.blit(fond_image, (0, 0))
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Vérifie si un bouton de la souris est enfoncé
            pygame.quit()
            sys.exit()

    pygame.display.flip()
