import pygame
import math

# Inicialización de Pygame
pygame.init()

# Configurar modo de pantalla completa
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = window.get_size()  # Obtener dimensiones de la pantalla completa
pygame.display.set_caption('Visor de Fotos 360')

# Cargar imágenes 360 y ángulos
images = [
    ('imagen1.jpg', 25),
    ('imagen2.jpg', 28),
    ('imagen3.jpg', 31),
    ('imagen4.jpg', 34),
    ('imagen5.jpg', 37),
    ('imagen6.jpg', 40),
    ('imagen7.jpg', 43)
]
image_index = 0
image, angle = images[image_index]
loaded_image = pygame.image.load(image)
image_width, image_height = loaded_image.get_size()

# Variables de desplazamiento
x_offset = 0
y_offset = 0
scroll_speed = 5

# Rango máximo para desplazamiento
max_x_offset = image_width - WIDTH
max_y_offset = image_height - HEIGHT

# Variables para el manejo del mouse
mouse_down = False
last_mouse_pos = None

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Fuente para el ángulo y texto de los botones
font = pygame.font.SysFont(None, 40)

# Función para dibujar botones con ajuste automático al texto
def draw_button(text, x, y, color, action=None):
    # Renderizar el texto para obtener su tamaño
    button_text = font.render(text, True, WHITE)
    text_width = button_text.get_width()
    text_height = button_text.get_height()
    
    # Calcular tamaño del botón basado en el tamaño del texto con márgenes
    button_width = text_width + 20
    button_height = text_height + 10
    
    # Dibujar botón
    pygame.draw.rect(window, color, (x, y, button_width, button_height))
    
    # Dibujar texto en el botón
    window.blit(button_text, (x + 10, y + 5))
    
    return pygame.Rect(x, y, button_width, button_height)  # Retornar rectángulo del botón para verificar clics

# Bucle principal
running = True
while running:
    window.fill(BLACK)
    
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Manejar clic del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            last_mouse_pos = pygame.mouse.get_pos()
            x, y = last_mouse_pos
            
            # Verificar si se hizo clic en los botones
            if retro_button.collidepoint(x, y):  # Botón Retroceder
                if image_index > 0:
                    image_index -= 1
                    image, angle = images[image_index]
                    loaded_image = pygame.image.load(image)
                    image_width, image_height = loaded_image.get_size()
                    x_offset, y_offset = 0, 0  # Reset desplazamiento
            elif avance_button.collidepoint(x, y):  # Botón Avanzar
                if image_index < len(images) - 1:
                    image_index += 1
                    image, angle = images[image_index]
                    loaded_image = pygame.image.load(image)
                    image_width, image_height = loaded_image.get_size()
                    x_offset, y_offset = 0, 0  # Reset desplazamiento

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

    # Movimiento con el mouse
    if mouse_down:
        current_mouse_pos = pygame.mouse.get_pos()
        if last_mouse_pos:
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            x_offset -= dx
            y_offset -= dy
            last_mouse_pos = current_mouse_pos

    # Limitar desplazamiento al tamaño de la imagen
    x_offset = max(0, min(x_offset, max_x_offset))
    y_offset = max(0, min(y_offset, max_y_offset))

    # Dibujar la parte visible de la imagen
    window.blit(loaded_image, (-x_offset, -y_offset))

    # Dibujar botones
    retro_button = draw_button("Retroceder", 100, 10, GRAY)
    avance_button = draw_button("Avanzar", WIDTH - 200, 10, GRAY)

    # Mostrar ángulo en la parte superior
    angle_text = font.render(f"Temperatura: {angle}°", True, WHITE)
    window.blit(angle_text, (WIDTH // 2 - 100, 20))

    # Actualizar la pantalla
    pygame.display.update()

# Finalizar Pygame
pygame.quit()

