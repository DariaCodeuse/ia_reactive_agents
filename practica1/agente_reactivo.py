import pygame
import random

# Configuración de la pantalla
ANCHO, ALTO = 500, 500
COLOR_FONDO = (30, 30, 30)

# Configuración del agente
TAMANIO_AGENTE = 20
VELOCIDAD_AGENTE = 2
DISTANCIA_SEGURIDAD = 20  # Ajustado para asegurar una distancia segura
COLORES_AGENTES = [(0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 0, 255)]
NUMERO_AGENTES = 15

# Configuración del agente controlado por el usuario
COLOR_AGENTE_USUARIO = (255, 255, 255)
VELOCIDAD_USUARIO = 4

# Configuración de los obstáculos
COLOR_OBSTACULO = (255, 0, 0)
NUMERO_OBSTACULOS = 10
TAMANIO_OBSTACULO = 40

# Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Agente Reactivo")

# Generar obstáculos en posiciones aleatorias
obstaculos = []
for _ in range(NUMERO_OBSTACULOS):
    while True:
        obs_x = random.randint(0, ANCHO - TAMANIO_OBSTACULO)
        obs_y = random.randint(0, ALTO - TAMANIO_OBSTACULO)
        nuevo_obstaculo = pygame.Rect(obs_x, obs_y, TAMANIO_OBSTACULO, TAMANIO_OBSTACULO)
        if not any(nuevo_obstaculo.colliderect(o.inflate(DISTANCIA_SEGURIDAD, DISTANCIA_SEGURIDAD)) for o in obstaculos):
            obstaculos.append(nuevo_obstaculo)
            break

# Generar agentes en posiciones aleatorias sin colisiones
agentes = []
for _ in range(NUMERO_AGENTES):
    while True:
        agente_x = random.randint(DISTANCIA_SEGURIDAD, ANCHO - TAMANIO_AGENTE - DISTANCIA_SEGURIDAD)
        agente_y = random.randint(DISTANCIA_SEGURIDAD, ALTO - TAMANIO_AGENTE - DISTANCIA_SEGURIDAD)
        nuevo_agente = pygame.Rect(agente_x, agente_y, TAMANIO_AGENTE, TAMANIO_AGENTE)
        if not any(nuevo_agente.colliderect(o.inflate(DISTANCIA_SEGURIDAD, DISTANCIA_SEGURIDAD)) for o in obstaculos) and not any(nuevo_agente.colliderect(a["rect"].inflate(DISTANCIA_SEGURIDAD, DISTANCIA_SEGURIDAD)) for a in agentes):
            break
    color = random.choice(COLORES_AGENTES)
    agentes.append({"rect": nuevo_agente, "color": color, "dx": random.choice([-VELOCIDAD_AGENTE, VELOCIDAD_AGENTE]), "dy": random.choice([-VELOCIDAD_AGENTE, VELOCIDAD_AGENTE])})

# Agregar agente controlado por el usuario
def posicion_valida(rect):
    return not any(rect.colliderect(o.inflate(DISTANCIA_SEGURIDAD, DISTANCIA_SEGURIDAD)) for o in obstaculos) and not any(rect.colliderect(a["rect"].inflate(DISTANCIA_SEGURIDAD, DISTANCIA_SEGURIDAD)) for a in agentes)

while True:
    user_x = random.randint(DISTANCIA_SEGURIDAD, ANCHO - TAMANIO_AGENTE - DISTANCIA_SEGURIDAD)
    user_y = random.randint(DISTANCIA_SEGURIDAD, ALTO - TAMANIO_AGENTE - DISTANCIA_SEGURIDAD)
    agente_usuario = pygame.Rect(user_x, user_y, TAMANIO_AGENTE, TAMANIO_AGENTE)
    if posicion_valida(agente_usuario):
        break

# Función para verificar colisión o proximidad
def verificar_colision(nuevo_rect, agente_actual):
    if nuevo_rect.left < DISTANCIA_SEGURIDAD or nuevo_rect.right > ANCHO - DISTANCIA_SEGURIDAD or nuevo_rect.top < DISTANCIA_SEGURIDAD or nuevo_rect.bottom > ALTO - DISTANCIA_SEGURIDAD:
        return True  # Evitar salir de los bordes
    for obs in obstaculos:
        if nuevo_rect.colliderect(obs.inflate(DISTANCIA_SEGURIDAD, DISTANCIA_SEGURIDAD)):
            return True  # Evitar colisión con obstáculos
    for otro in agentes:
        if otro != agente_actual and nuevo_rect.colliderect(otro["rect"].inflate(DISTANCIA_SEGURIDAD, DISTANCIA_SEGURIDAD)):
            return True  # Evitar colisión con otros agentes
    if nuevo_rect.colliderect(agente_usuario.inflate(DISTANCIA_SEGURIDAD, DISTANCIA_SEGURIDAD)) and agente_actual is not None:
        return True  # Evitar que los agentes atraviesen al usuario
    return False

# Función para cambiar dirección evitando colisiones
def cambiar_direccion(agente):
    direcciones = [(-VELOCIDAD_AGENTE, 0), (VELOCIDAD_AGENTE, 0), (0, -VELOCIDAD_AGENTE), (0, VELOCIDAD_AGENTE)]
    random.shuffle(direcciones)
    for dx, dy in direcciones:
        temp_rect = agente["rect"].move(dx, dy)
        if not verificar_colision(temp_rect, agente):
            agente["dx"], agente["dy"] = dx, dy
            return

# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(20)
    teclas = pygame.key.get_pressed()
    movimiento_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * VELOCIDAD_USUARIO
    movimiento_y = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * VELOCIDAD_USUARIO
    nuevo_rect_usuario = agente_usuario.move(movimiento_x, movimiento_y)
    if not verificar_colision(nuevo_rect_usuario, None):
        agente_usuario = nuevo_rect_usuario

    # Verificar eventos (cierre de ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Mover los agentes
    for agente in agentes:
        nuevo_rect = agente["rect"].move(agente["dx"], agente["dy"])
        if verificar_colision(nuevo_rect, agente):
            cambiar_direccion(agente)
        else:
            agente["rect"] = nuevo_rect

    # Dibujar el entorno
    pantalla.fill(COLOR_FONDO)
    pygame.draw.rect(pantalla, COLOR_AGENTE_USUARIO, agente_usuario)
    for agente in agentes:
        pygame.draw.rect(pantalla, agente["color"], agente["rect"])
    for obs in obstaculos:
        pygame.draw.rect(pantalla, COLOR_OBSTACULO, obs)
    pygame.display.update()

# Cerrar Pygame
pygame.quit()