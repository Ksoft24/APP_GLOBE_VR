import pygame
import math
from moviepy.editor import VideoFileClip

# Inicialización de Pygame
pygame.init()

# Configurar modo de pantalla completa
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = window.get_size()  # Obtener dimensiones de la pantalla completa
pygame.display.set_caption('Visor de Fotos 360')

# Cargar el video para el fondo del menú
video_clip = VideoFileClip("fondo.mp4").resize((WIDTH, HEIGHT))
video_surface = pygame.Surface((WIDTH, HEIGHT))

# Crear un generador de frames del video
video_generator = video_clip.iter_frames(fps=30, dtype="uint8")

# Cargar imágenes 360 y ángulos para cada página
page_images = {
    'Atmosphere': [('imagen1.jpg', "Paisaje 1"), ('imagen2.jpg', "Paisaje 2"), ('imagen3.jpg', ""), ('imagen4.jpg', ""), ('imagen5.jpg', ""), ('imagen6.jpg', ""), ('imagen7.jpg', "")],
     'Hydrology': [('imagen1.jpg', "Paisaje 1"), ('imagen2.jpg', "Paisaje 2"), ('imagen3.jpg', ""), ('imagen4.jpg', ""), ('imagen5.jpg', ""), ('imagen6.jpg', ""), ('imagen7.jpg', "")],
      'Phenology': [('imagen1.jpg', "Paisaje 1"), ('imagen2.jpg', "Paisaje 2"), ('imagen3.jpg', ""), ('imagen4.jpg', ""), ('imagen5.jpg', ""), ('imagen6.jpg', ""), ('imagen7.jpg', "")],
       'Soil': [('imagen1.jpg', "Paisaje 1"), ('imagen2.jpg', "Paisaje 2"), ('imagen3.jpg', ""), ('imagen4.jpg', ""), ('imagen5.jpg', ""), ('imagen6.jpg', ""), ('imagen7.jpg', "")],
        'Land Cover': [('imagen1.jpg', "Paisaje 1"), ('imagen2.jpg', "Paisaje 2"), ('imagen3.jpg', ""), ('imagen4.jpg', ""), ('imagen5.jpg', ""), ('imagen6.jpg', ""), ('imagen7.jpg', "")],
         'Biology': [('imagen1.jpg', "Paisaje 1"), ('imagen2.jpg', "Paisaje 2"), ('imagen3.jpg', ""), ('imagen4.jpg', ""), ('imagen5.jpg', ""), ('imagen6.jpg', ""), ('imagen7.jpg', "")]
}

# Variables iniciales
current_page = None
image_index = 0
x_offset = 0
y_offset = 0
mouse_down = False
last_mouse_pos = None

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Fuente
font = pygame.font.SysFont(None, 40)
title_font = pygame.font.SysFont(None, 80)

# Función para dibujar botones
def draw_button(text, x, y, color, action=None):
    button_text = font.render(text, True, WHITE)
    text_width = button_text.get_width()
    text_height = button_text.get_height()
    button_width = text_width + 20
    button_height = text_height + 10
    pygame.draw.rect(window, color, (x, y, button_width, button_height))
    window.blit(button_text, (x + 10, y + 5))
    return pygame.Rect(x, y, button_width, button_height)

# Función para mostrar el menú principal
def show_main_menu():
    global video_generator  # Hacer la variable global para poder usarla en esta función

    # Reproducir el video como fondo
    try:
        frame = next(video_generator)
    except StopIteration:
        # Si el video llega al final, reiniciar el generador
        video_generator = video_clip.iter_frames(fps=30, dtype="uint8")
        frame = next(video_generator)

    pygame.surfarray.blit_array(video_surface, frame.swapaxes(0, 1))
    window.blit(video_surface, (0, 0))

    # Título "GLOBE VR"
    title_text = title_font.render("GLOBE VR", True, WHITE)
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Crear botones de menú
    button_positions = [
        (WIDTH // 4 - 100, HEIGHT // 2 - 150),
        (WIDTH * 3 // 4 - 100, HEIGHT // 2 - 150),
        (WIDTH // 4 - 100, HEIGHT // 2 + 50),
        (WIDTH * 3 // 4 - 100, HEIGHT // 2 + 50),
        (WIDTH // 4 - 100, HEIGHT // 2 + 250),
        (WIDTH * 3 // 4 - 100, HEIGHT // 2 + 250),
    ]

    page_buttons = []
    for i, page in enumerate(['Atmosphere', 'Hydrology', 'Soil', 'Phenology', 'Land Cover', 'Biology']):
        x, y = button_positions[i]
        page_button = draw_button(page, x, y, GRAY)
        page_buttons.append((page_button, page))

    return page_buttons

# Función para mostrar una página
def show_page():
    global x_offset, y_offset, last_mouse_pos
    window.fill(BLACK)

    

    # Mostrar la imagen actual
    image, angle = page_images[current_page][image_index]
    loaded_image = pygame.image.load(image)
    image_width, image_height = loaded_image.get_size()

    if mouse_down:
        current_mouse_pos = pygame.mouse.get_pos()
        if last_mouse_pos:
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            x_offset -= dx
            y_offset -= dy
        last_mouse_pos = current_mouse_pos

    x_offset = max(0, min(x_offset, image_width - WIDTH))
    y_offset = max(0, min(y_offset, image_height - HEIGHT))

    window.blit(loaded_image, (-x_offset, -y_offset))
# Botones de retroceso y avance
    retro_button = draw_button("Retroceder", 100, 10, GRAY)
    avance_button = draw_button("Avanzar", WIDTH - 200, 10, GRAY)

    # Botón para regresar al menú principal
    menu_button = draw_button("Menú", WIDTH - 200, HEIGHT - 60, GRAY)
   # Dibujar botones

    # Mostrar ángulo en la parte superior
    angle_text = font.render(angle, True, WHITE)
    window.blit(angle_text, (WIDTH // 2 - 100, 20))

    return retro_button, avance_button, menu_button

# Bucle principal
running = True
main_menu = True
page_buttons = show_main_menu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if main_menu and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for page_button, page in page_buttons:
                if page_button.collidepoint(x, y):
                    current_page = page
                    main_menu = False
                    image_index = 0
                    x_offset = 0
                    y_offset = 0

        if not main_menu and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            last_mouse_pos = pygame.mouse.get_pos()
            x, y = last_mouse_pos

            retro_button, avance_button, menu_button = show_page()

            if retro_button.collidepoint(x, y):
                if image_index > 0:
                    image_index -= 1
                    x_offset = 0
                    y_offset = 0
            elif avance_button.collidepoint(x, y):
                if image_index < len(page_images[current_page]) - 1:
                    image_index += 1
                    x_offset = 0
                    y_offset = 0
            elif menu_button.collidepoint(x, y):
                # Regresar al menú principal
                main_menu = True
                x_offset = 0
                y_offset = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            last_mouse_pos = None

    if main_menu:
        page_buttons = show_main_menu()
    else:
        retro_button, avance_button, menu_button = show_page()

    pygame.display.update()

pygame.quit()
