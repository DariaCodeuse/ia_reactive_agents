import pygame
import random
import time

# Configuración de la pantalla
ANCHO, ALTO = 500, 550  # Se aumenta para la barra de progreso
TAMANIO_CELDA = 50
FILAS, COLUMNAS = ANCHO // TAMANIO_CELDA, (ALTO - 50) // TAMANIO_CELDA

# Colores
COLOR_FONDO = (30, 30, 30)
COLOR_LIMPIO = (17, 86, 50)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Zombiess Comecerebros")

# Cargar imágenes y ajustar proporciones
imagen_zombie = pygame.image.load("./img/zombie.png")
imagen_zombie = pygame.transform.scale(imagen_zombie, (40, 60))

imagen_cerebro = pygame.image.load("./img/brain.png")
imagen_cerebro = pygame.transform.scale(imagen_cerebro, (40, 40))

# Pantalla inicial
fuente = pygame.font.Font(None, 35)

# Cargar la imagen de fondo
imagen_fondo = pygame.image.load("./img/fondo_inicio.jpg")  # Reemplaza con el nombre de tu imagen
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))  # Ajustar al tamaño de la pantalla

# Cargar la imagen del título
imagen_titulo = pygame.image.load("./img/titulo.png")  # Reemplaza con el nombre de tu imagen
imagen_titulo = pygame.transform.scale(imagen_titulo, (300, 240))  # Ajusta el tamaño si es necesario

# Función para cambiar la música
def cambiar_musica(archivo, bucle=True, volumen=0.5):
    pygame.mixer.music.stop()  # Detener la música actual
    pygame.mixer.music.load(archivo)  # Cargar el archivo de música
    pygame.mixer.music.set_volume(volumen)  # Ajustar el volumen
    if bucle:
        pygame.mixer.music.play(-1)  # Reproduce en bucle
    else:
        pygame.mixer.music.play(0)  # Reproduce una vez

# Cargar la música de fondo
cambiar_musica("./mp3/musica_inicio.mp3", bucle=True)

# Pantalla de inicio
def pantalla_inicio():
    seleccionando = True
    zombies = 1
    
    pygame.mixer.music.play(-1)  # Reproduce la música en bucle

    while seleccionando:
        pantalla.blit(imagen_fondo, (0, 0))  # Dibujar la imagen de fondo

        # Centrar el título
        titulo_x = (ANCHO - imagen_titulo.get_width()) // 2
        titulo_y = (ALTO // 10)  # Lo subimos más
        pantalla.blit(imagen_titulo, (titulo_x, titulo_y))

        # Espaciado entre los elementos
        separacion = 60  

        # Texto para indicar la selección de zombies
        texto_indicacion = fuente.render("Número de zombies:", True, (255, 255, 255))
        pantalla.blit(texto_indicacion, ((ANCHO - texto_indicacion.get_width()) // 2, titulo_y + imagen_titulo.get_height() + 10))

        # Contenedor del número de zombies
        rect_x = (ANCHO - 100) // 2
        rect_y = titulo_y + imagen_titulo.get_height() + 50  
        pygame.draw.rect(pantalla, (200, 200, 200), (rect_x, rect_y, 100, 60), border_radius=10)
        
        texto_zombies = fuente.render(f"{zombies}", True, (0, 0, 0))
        pantalla.blit(texto_zombies, (rect_x + 35, rect_y + 15))

        # Botones de selección (+ y -) alineados horizontalmente debajo del contador
        boton_mas = pygame.Rect(rect_x + 120, rect_y, 50, 50)
        boton_menos = pygame.Rect(rect_x - 70, rect_y, 50, 50)

        pygame.draw.rect(pantalla, (43, 87, 47), boton_mas, border_radius=10)
        pygame.draw.rect(pantalla, (43, 87, 47), boton_menos, border_radius=10)

        pantalla.blit(fuente.render("+", True, (255, 255, 255)), (boton_mas.x + 18, boton_mas.y + 10))
        pantalla.blit(fuente.render("-", True, (255, 255, 255)), (boton_menos.x + 18, boton_menos.y + 10))

        # Botón PLAY centrado más abajo
        boton_play = pygame.Rect((ANCHO - 150) // 2, rect_y + separacion + 30, 150, 60)
        pygame.draw.rect(pantalla, (142, 15, 36 ), boton_play, border_radius=15)
        pantalla.blit(fuente.render("PLAY", True, (255, 255, 255)), (boton_play.x + 45, boton_play.y + 18))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_mas.collidepoint(evento.pos) and zombies < 5:
                    zombies += 1
                elif boton_menos.collidepoint(evento.pos) and zombies > 1:
                    zombies -= 1
                elif boton_play.collidepoint(evento.pos):
                    pygame.mixer.music.stop()  # Detener la música al iniciar el juego
                    return zombies

    seleccionando = True
    zombies = 1

    while seleccionando:
        # Dibujar la imagen de fondo
        pantalla.blit(imagen_fondo, (0, 0))

        # Coordenada base para organizar todo en columna
        centro_x = ANCHO // 2
        inicio_y = ALTO // 4  # Punto de inicio para la columna

        # Mostrar la imagen del título en la parte superior
        pantalla.blit(imagen_titulo, (centro_x - imagen_titulo.get_width() // 2, inicio_y))

        # Espaciado entre elementos
        separacion = 80

        # Contenedor del número de zombies
        rect_x = centro_x - 50
        rect_y = inicio_y + separacion
        pygame.draw.rect(pantalla, (200, 200, 200), (rect_x, rect_y, 110, 60), border_radius=10)
        texto_zombies = fuente.render(f"{zombies}", True, (0, 0, 0))
        pantalla.blit(texto_zombies, (rect_x + 35, rect_y + 15))

        # Botones de selección (+ y -) alineados en una fila
        boton_mas = pygame.Rect(centro_x + 70, rect_y, 50, 50)
        boton_menos = pygame.Rect(centro_x - 120, rect_y, 50, 50)

        pygame.draw.rect(pantalla, (0, 150, 0), boton_mas, border_radius=10)
        pygame.draw.rect(pantalla, (150, 0, 0), boton_menos, border_radius=10)

        pantalla.blit(fuente.render("+", True, (255, 255, 255)), (boton_mas.x + 15, boton_mas.y + 10))
        pantalla.blit(fuente.render("-", True, (255, 255, 255)), (boton_menos.x + 15, boton_menos.y + 10))

        # Botón PLAY centrado debajo de los controles
        boton_play = pygame.Rect(centro_x - 75, rect_y + separacion + 30, 150, 60)
        pygame.draw.rect(pantalla, (0, 0, 200), boton_play, border_radius=15)
        pantalla.blit(fuente.render("PLAY", True, (255, 255, 255)), (boton_play.x + 40, boton_play.y + 15))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_mas.collidepoint(evento.pos) and zombies < 10:
                    zombies += 1
                elif boton_menos.collidepoint(evento.pos) and zombies > 1:
                    zombies -= 1
                elif boton_play.collidepoint(evento.pos):
                    return zombies

# Obtener cantidad de zombies
num_zombies = pantalla_inicio()

# Generar el entorno con suciedad aleatoria
entorno = [[random.choice([0, 1]) for _ in range(COLUMNAS)]
                          for _ in range(FILAS)]

# Crear zombies en posiciones aleatorias
zombies = [(random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1))
            for _ in range(num_zombies)]

# Contar el total de celdas sucias al inicio
total_sucias = sum(sum(fila) for fila in entorno)
movimientos = 0
inicio_tiempo = time.time()

# Cargar la música de fondo
cambiar_musica("./mp3/musica_juego.mp3", bucle=True)

# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(200)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    objetivos_reclamados = set()  # Almacenar celdas ya seleccionadas

    for i in range(num_zombies):
        x, y = zombies[i]

        if entorno[x][y] == 1:
            entorno[x][y] = 0
        else:
            # Obtener todas las posiciones sucias disponibles
            posiciones_sucias = [(i, j) for i in range(FILAS) for j in range(COLUMNAS) if entorno[i][j] == 1 and (i, j) not in objetivos_reclamados]

            if posiciones_sucias:
                # Buscar la más cercana que no esté reclamada
                objetivo = min(posiciones_sucias, key=lambda pos: abs(
                    pos[0] - x) + abs(pos[1] - y))
                # Marcar la celda como reclamada
                objetivos_reclamados.add(objetivo)

                dx = 1 if objetivo[0] > x else -1 if objetivo[0] < x else 0
                dy = 1 if objetivo[1] > y else -1 if objetivo[1] < y else 0
                zombies[i] = (x + dx, y + dy)
                movimientos += 1

    sucias_restantes = sum(sum(fila) for fila in entorno)
    porcentaje_limpieza = (1 - sucias_restantes / total_sucias) * 100 if total_sucias > 0 else 100
    
    pantalla.fill(COLOR_FONDO)
    for i in range(FILAS):
        for j in range(COLUMNAS):
            pygame.draw.rect(pantalla, COLOR_LIMPIO, (j * TAMANIO_CELDA, i * TAMANIO_CELDA, TAMANIO_CELDA, TAMANIO_CELDA))
            if entorno[i][j] == 1:
                pantalla.blit(imagen_cerebro, (j * TAMANIO_CELDA, i * TAMANIO_CELDA))
    
    for x, y in zombies:
        pantalla.blit(imagen_zombie, (y * TAMANIO_CELDA, x * TAMANIO_CELDA))
    
    pygame.draw.rect(pantalla, (100, 100, 100), (50, ALTO - 40, 300, 20))
    pygame.draw.rect(pantalla, (0, 255, 0), (50, ALTO - 40, int(300 * (porcentaje_limpieza / 100)), 20))
    
    fuente_barra = pygame.font.Font(None, 24)
    texto = fuente_barra.render(f"{int(porcentaje_limpieza)}%", True, (255, 255, 255))
    pantalla.blit(texto, (180, ALTO - 38))
    
    pygame.display.update()
    if sucias_restantes == 0:
        ejecutando = False

# Pantalla final con solo el botón de salir
def pantalla_final(movimientos, tiempo_total):
    fuente_final = pygame.font.Font(None, 35)
    salir = False
    
    while not salir:
        pantalla.fill((0, 0, 0))
        
        # Mensajes finales
        pantalla.blit(fuente_final.render("Juego Terminado", True, (255, 255, 255)), (ANCHO // 2 - 100, 100))
        pantalla.blit(fuente_final.render(f"Movimientos: {movimientos}", True, (255, 255, 255)), (ANCHO // 2 - 100, 150))
        pantalla.blit(fuente_final.render(f"Tiempo: {tiempo_total}s", True, (255, 255, 255)), (ANCHO // 2 - 100, 200))
        
        # Botón Salir
        boton_salir = pygame.Rect(ANCHO // 2 - 50, 300, 100, 50)
        pygame.draw.rect(pantalla, (200, 0, 0), boton_salir, border_radius=10)
        pantalla.blit(fuente_final.render("Salir", True, (255, 255, 255)), (boton_salir.x + 25, boton_salir.y + 10))

        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

    return False  # Indica que no se reinicia el juego

# Llamar a la pantalla final y verificar si se reinicia el juego
while True:
    tiempo_total = round(time.time() - inicio_tiempo, 2)
    cambiar_musica("./mp3/musica_fin.mp3", bucle=True)
    
    if not pantalla_final(movimientos, tiempo_total):
        break  # Salir del bucle si el jugador no quiere reiniciar

pygame.quit()