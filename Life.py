import pygame
import numpy as np
import time

pygame.init()

# Tamaño de pantalla
width, height = 1000, 1000
# Creación de la pantalla
screen = pygame.display.set_mode((height, width))
# Color de fondo
bg = 30, 30, 30
# Llenamos la pantalla con el color de fondo
screen.fill(bg)

celdasX, celdasY = 60, 60

dimCW = width / celdasX
dimCH = height / celdasY

# Estado de las celdas -> 1 = Viva, 0 = Muerta
gameStatus = np.zeros((celdasX, celdasY))

# Inicializamos autómatas
gameStatus[6, 3] = 1
gameStatus[6, 4] = 1
gameStatus[6, 5] = 1

gameStatus[33, 3] = 1
gameStatus[33, 4] = 1
gameStatus[33, 5] = 1
gameStatus[34, 3] = 1
gameStatus[35, 4] = 1
gameStatus[36, 5] = 1

gameStatus[53, 3] = 1
gameStatus[53, 4] = 1
gameStatus[53, 5] = 1
gameStatus[54, 3] = 1
gameStatus[55, 4] = 1
gameStatus[56, 5] = 1

gameStatus[14, 13] = 1
gameStatus[14, 12] = 1
gameStatus[13, 14] = 1
gameStatus[13, 13] = 1

gameStatus[4, 3] = 1
gameStatus[4, 2] = 1
gameStatus[3, 4] = 1
gameStatus[3, 3] = 1

gameStatus[21, 21] = 1
gameStatus[22, 22] = 1
gameStatus[22, 23] = 1
gameStatus[21, 23] = 1
gameStatus[20, 23] = 1

gameStatus[51, 51] = 1
gameStatus[52, 52] = 1
gameStatus[52, 53] = 1
gameStatus[51, 53] = 1
gameStatus[50, 53] = 1

gameStatus[57, 55] = 1
gameStatus[57, 56] = 1
gameStatus[57, 56] = 1
gameStatus[55, 54] = 1
gameStatus[55, 55] = 1

# Control de la ejecución del juego
pauseExec = False

# Ejecución indefinida
while not pauseExec:

    newGameStatus = np.copy(gameStatus)

    screen.fill(bg)
    time.sleep(0.1)

    # Registramos eventos de teclado y/o ratón
    event = pygame.event.get()

    for e in event:
        if e.type == pygame.KEYDOWN:
            pauseExec = not pauseExec
        # Qué tecla se está pulsando
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameStatus[celX, celY] = not mouseClick[2]

    for i in range(0, celdasX):
        for j in range(0, celdasY):
            if not pauseExec:
                # Calculamos los vecinos cercanos
                # Además, se implementa de forma toroidal
                n_neigh = gameStatus[(j - 1) % celdasX, (i - 1) % celdasY] + \
                          gameStatus[j % celdasX, (i - 1) % celdasY] + \
                          gameStatus[(j + 1) % celdasX, (i - 1) % celdasY] + \
                          gameStatus[(j - 1) % celdasX, i % celdasY] + \
                          gameStatus[(j + 1) % celdasX, i % celdasY] + \
                          gameStatus[(j - 1) % celdasX, (i + 1) % celdasY] + \
                          gameStatus[j % celdasX, (i + 1) % celdasY] + \
                          gameStatus[(j + 1) % celdasX, (i + 1) % celdasY]

                # ------Reglas de creación:-------

                # 1--- Una célula muerta con exactamente 3 vecinas vivas, REVIVE
                if gameStatus[j, i] == 0 and n_neigh == 3:
                    newGameStatus[j, i] = 1

                # 2--- Una célula viva con menos de 2 o más de 3 vecinas vivas, MUERE
                elif gameStatus[j, i] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameStatus[j, i] = 0

                # Creamos el poligono de cada celda que se dibuja
                poligono = [(j * dimCW, i * dimCH),
                            ((j + 1) * dimCW, i * dimCH),
                            ((j + 1) * dimCW, (i + 1) * dimCH),
                            (j * dimCW, (i + 1) * dimCH)]
                # Dibujamos la celda
                if newGameStatus[j, i] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poligono, 1)
                else:
                    pygame.draw.polygon(screen, (33, 255, 12), poligono, 0)

    # Actualizamos el estado
    gameStatus = np.copy(newGameStatus)
    # Actualizamos la pantalla
    pygame.display.flip()
