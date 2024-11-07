import pygame
import random
import math
from pygame import mixer



# Inicializar a Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption('Space Invaders')
icono = pygame.image.load('ovni.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')

# Agregar Musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Variables Jugador
img_jugador = pygame.image.load('cohete-espacial.png')
jugador_x = 364
jugador_y = 500
jugador_x_cambio = 0
jugador_y_cambio = 0

# Variable enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('monstruo.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.7)
    enemigo_y_cambio.append(50)

# Variable bala
balas = []
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# Variable puntaje
puntaje = 0
fuente = pygame.font.SysFont('Arial', 32)
texto_x = 10
texto_y = 10

# Texto final del juego
fuente_final = pygame.font.SysFont('Arial', 40)

# Funcion texto final
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (200, 250))

# Funcion Mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# Funcion para detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # Imagen de  Pantalla
    pantalla.blit(fondo, (0, 0))

    # Iterar evento
    for event in pygame.event.get():

        # Evento Cerrar
        if event.type == pygame.QUIT:
            se_ejecuta = False

        # Evento Presionar teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if event.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if event.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                nueva_bala = {'x': jugador_x, 'y': jugador_y, 'velocidad': -5}
                balas.append(nueva_bala)

        # Evento soltar flechas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    # mantener dentro de bordes
    if jugador_x < 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]

    # mantener dentro de bordes
        if enemigo_x[e] < 0:
            enemigo_x_cambio[e] = 0.7
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.7
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        for bala in balas:
            colision = hay_colision(enemigo_x[e], enemigo_y[e], bala['x'], bala['y'])
            if colision:
                sonido_colision = mixer.Sound('golpe.mp3')
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento bala
    for bala in balas:
        bala['y'] += bala['velocidad']
        pantalla.blit(img_bala, (bala['x'] + 16, bala['y'] + 10))
        if bala['y'] < 0:
            balas.remove(bala)

    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    # Actualizar
    pygame.display.update()

