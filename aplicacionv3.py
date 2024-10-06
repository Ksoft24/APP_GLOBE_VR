import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from PIL import Image

# Inicializar pygame
pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size, DOUBLEBUF | OPENGL)

# Configurar proyección
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (window_size[0] / window_size[1]), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Variables de control de la cámara
camera_pos = [0.0, 0.0, 0.0]  # Posición de la cámara
camera_angle_y = 0.0  # Ángulo de rotación de la cámara en Y
mouse_down = False
last_mouse_pos = None

# Cargar imagen 360 como textura
def load_texture(image_path):
    img = Image.open(image_path)
    img_data = img.tobytes("raw", "RGB", 0, -1)
    width, height = img.size

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id

# Crear esfera para la imagen 360 (invertida para ver desde adentro)
def draw_sphere_inverted(radius, slices, stacks):
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + float(i) / stacks)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * float(j) / slices
            x = math.cos(lng)
            y = math.sin(lng)

            # Normales invertidas
            glNormal3f(-x * zr0, -y * zr0, -z0)
            glTexCoord2f(float(j) / slices, float(i) / stacks)
            glVertex3f(x * zr0, y * zr0, z0)

            glNormal3f(-x * zr1, -y * zr1, -z1)
            glTexCoord2f(float(j) / slices, float(i + 1) / stacks)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

# Mover la cámara según el mouse y teclas
def update_camera():
    glLoadIdentity()
    # Aplicar la posición de la cámara
    glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])  
    glRotatef(camera_angle_y, 0, 1, 0)  # Solo rotación alrededor del eje Y

# Bucle principal
def main():
    global camera_pos, camera_angle_y, mouse_down, last_mouse_pos

    # Cargar textura 360
    texture_id = load_texture("imagen1.jpg")  # Reemplaza con la ruta de tu imagen

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == pygame.MOUSEMOTION and mouse_down:
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]
                camera_angle_y += dx * 0.1  # Solo cambiar la rotación alrededor del eje Y
                last_mouse_pos = current_mouse_pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    camera_pos[0] -= 0.1  # Mover hacia la izquierda
                elif event.key == pygame.K_RIGHT:
                    camera_pos[0] += 0.1  # Mover hacia la derecha
                elif event.key == pygame.K_UP:
                    camera_pos[1] += 0.1  # Mover hacia arriba
                elif event.key == pygame.K_DOWN:
                    camera_pos[1] -= 0.1  # Mover hacia abajo

        # Limpiar pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        update_camera()

        # Dibujar la esfera invertida con la textura
        glBindTexture(GL_TEXTURE_2D, texture_id)
        draw_sphere_inverted(5, 50, 50)  # El radio puede ajustarse para un mejor efecto

        # Actualizar pantalla
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
