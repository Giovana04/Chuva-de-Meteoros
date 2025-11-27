import sys
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

LARGURA_JANELA = 1200
ALTURA_JANELA = 800

texturas = {}
# (Arquivo, Raio, Distancia, Velocidade)
PLANETAS = [
    ("mercurio.jpg", 1, 2.0, 4),
    ("venus.jpg",    3, 3.0, 1.5),
    ("terra.jpg",    7, 4.5, 1),
    ("marte.jpg",    1, 6.0, 0.5),
    ("jupiter.png",  20, 10.0, 0.2),
    ("saturno.png",  17, 14.0, 0.15),
    ("urano.png",    10, 18.0, 0.1),
    ("netuno.png",   10, 22.0, 0.08),
]

INDICE_TERRA = 2
INDICE_SATURNO = 5
RAIO_SCALE = 0.16 
DIST_SCALE = 3.0

rotacao_planetas = [0.0 for _ in range(len(PLANETAS))]
angulos = [0.0 for _ in range(len(PLANETAS))]
angulo_lua = 0.0
velocidade_tempo = 0.08
pausado = False
foco_camera = None 

nave_x = 0.0
nave_y = 0.0
nave_roll = 0.0 

def carregar_textura(arquivo):
    try:
        img = Image.open(arquivo)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGBA").tobytes()
        w, h = img.size
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return tex_id
    except:
        return 0

def inicializar_texturas():
    global texturas
    arquivos = [p[0] for p in PLANETAS] + ["sol.png", "lua.png", "anelSaturno.png", "estrelas.png", "image.png"]    
    for f in arquivos:
        if f not in texturas: texturas[f] = carregar_textura(f)

def posicionar_luz():
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.5, 1.5, 1.5, 1.0])
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def desenhar_esfera(tex_id, raio):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, raio, 32, 32)
    glDisable(GL_TEXTURE_2D)

# CONTROLE CÂMERA
cam_pitch = 0.0
cam_yaw = 0.0
zoom = -60.0
mouse_x, mouse_y = 0, 0
mouse_down = False

def aplicar_camera():
    global foco_camera
    if foco_camera is None:
        glTranslatef(0.0, 0.0, zoom)
        glRotatef(cam_pitch + 20, 1.0, 0.0, 0.0)
        glRotatef(cam_yaw, 0.0, 1.0, 0.0)
        return

    idx = foco_camera
    p = PLANETAS[idx]
    dist_orbita = p[2] * DIST_SCALE
    angulo_orbita = angulos[idx]
    raio_planeta = p[1] * RAIO_SCALE

    glRotatef(-cam_pitch, 1.0, 0.0, 0.0)
    glRotatef(-angulo_orbita - 90, 0.0, 1.0, 0.0) 
    glTranslatef(-dist_orbita, 0.0, 0.0)
    glTranslatef(0.0, -raio_planeta - 1.5, 0.0) 

def desenhar_hud_nave():
    global nave_x, nave_y, nave_roll
    
    if foco_camera is None or foco_camera < 0: return

    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -4.0) 
    
    glRotatef(nave_roll, 0.0, 0.0, 1.0)
    nave_roll *= 0.9

    # GRID
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glColor4f(0.4, 0.8, 1.0, 0.15) 
    glLineWidth(1.0)

    offset_z = (angulo_lua * 0.1) % 1.0 
    
    LARGURA_GRID = 3.0
    ALTURA_GRID = 1.5

    glBegin(GL_LINES)
    # Linhas de profundidade
    for i in range(-3, 4): 
        # Piso
        glVertex3f(i, -ALTURA_GRID, -10.0)
        glVertex3f(i, -ALTURA_GRID,  2.0)
        # Teto
        glVertex3f(i,  ALTURA_GRID, -10.0)
        glVertex3f(i,  ALTURA_GRID,  2.0)
    
    # Linhas movimento (ela inclina)
    for k in range(10):
        z = -k + offset_z
        # Piso
        glVertex3f(-LARGURA_GRID, -ALTURA_GRID, z)
        glVertex3f( LARGURA_GRID, -ALTURA_GRID, z)
        # Teto
        glVertex3f(-LARGURA_GRID,  ALTURA_GRID, z)
        glVertex3f( LARGURA_GRID,  ALTURA_GRID, z)
    glEnd()

    # aqui é onde vai ficar a nave
    glPushMatrix()
    glTranslatef(nave_x, nave_y, 0.0)
    glColor3f(0.0, 1.0, 1.0) 
    glLineWidth(2.0)
    
    glBegin(GL_LINE_LOOP) 
    glVertex3f(-0.15,  0.15, 0.0) # Sup Esq
    glVertex3f( 0.15,  0.15, 0.0) # Sup Dir
    glVertex3f( 0.15, -0.15, 0.0) # Inf Dir
    glVertex3f(-0.15, -0.15, 0.0) # Inf Esq
    glEnd()

    glPopMatrix()
    
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    desenhar_hud_nave()
    
    glColor3f(1.0, 1.0, 1.0)
    
    glPushMatrix()
    glPushMatrix()
    glRotate(cam_pitch, 1,0,0) 
    glRotate(cam_yaw, 0,1,0)
    desenhar_ceu()
    glPopMatrix()

    aplicar_camera()
    posicionar_luz()

    # SOL
    glPushMatrix()
    glDisable(GL_LIGHTING)
    if texturas.get('sol.png'):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texturas['sol.png']) 
        quad = gluNewQuadric(); gluQuadricTexture(quad, True)
        gluSphere(quad, 3.8, 32, 32)
        glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # PLANETAS
    for i, p in enumerate(PLANETAS):
        glPushMatrix()
        glRotatef(angulos[i], 0.0, 1.0, 0.0)
        glTranslatef(p[2] * DIST_SCALE, 0.0, 0.0)
        glRotatef(rotacao_planetas[i], 0.0, 1.0, 0.0)

        if i == INDICE_SATURNO:
            desenhar_esfera(texturas.get(p[0], 0), p[1] * RAIO_SCALE)
            glPushMatrix()
            glRotatef(80, 1,0,0)
            glDisable(GL_LIGHTING)
            glEnable(GL_TEXTURE_2D)
            if 'anelSaturno.png' in texturas: glBindTexture(GL_TEXTURE_2D, texturas['anelSaturno.png'])
            d = gluNewQuadric(); gluQuadricTexture(d, True)
            gluDisk(d, p[1]*RAIO_SCALE*1.2, p[1]*RAIO_SCALE*2.2, 64, 1)
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_LIGHTING)
            glPopMatrix()
        elif i == INDICE_TERRA:
            desenhar_esfera(texturas.get(p[0], 0), p[1] * RAIO_SCALE)
            glPushMatrix()
            glRotatef(angulo_lua, 0, 1, 0)
            glTranslatef((1+p[1])*RAIO_SCALE + 1.0, 0, 0)
            desenhar_esfera(texturas.get('lua.png',0), 0.27*RAIO_SCALE)
            glPopMatrix()
        else:
            desenhar_esfera(texturas.get(p[0], 0), p[1] * RAIO_SCALE)
            
        if foco_camera == i:
             glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glPopMatrix()

    glPopMatrix()
    glutSwapBuffers()

def desenhar_ceu():
    glDisable(GL_LIGHTING)
    glDepthMask(GL_FALSE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texturas.get('estrelas.png', 0))
    q = gluNewQuadric(); gluQuadricTexture(q, True)
    gluSphere(q, 150.0, 20, 20)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glDepthMask(GL_TRUE)

def idle():
    global angulos, angulo_lua, rotacao_planetas
    if not pausado:
        for i, p in enumerate(PLANETAS):
            angulos[i] = (angulos[i] + p[3] * velocidade_tempo) % 360.0
            rotacao_planetas[i] = (rotacao_planetas[i] + 1.2 * velocidade_tempo) % 360.0
        angulo_lua = (angulo_lua + 5.0 * velocidade_tempo) % 360.0
        glutPostRedisplay()

def teclado(key, x, y):
    global pausado, velocidade_tempo, foco_camera, nave_x, nave_y, nave_roll
    k = key.decode('utf-8').lower()
    if k == '\x1b': sys.exit(0)
    
    VEL_NAVE = 0.2
    # Limite pra a nave nao sair da tela
    LIMIT_X = 1.8 
    LIMIT_Y = 1.2

    if foco_camera is not None and foco_camera >= 0:
        if k == 'w' and nave_y < LIMIT_Y: nave_y += VEL_NAVE
        if k == 's' and nave_y > -LIMIT_Y: nave_y -= VEL_NAVE
        if k == 'a' and nave_x > -LIMIT_X: 
            nave_x -= VEL_NAVE; nave_roll = 25.0
        if k == 'd' and nave_x < LIMIT_X: 
            nave_x += VEL_NAVE; nave_roll = -25.0
        if k in 'wasd': return

    if k == 'p': pausado = not pausado
    elif k == '0': foco_camera = None; print("Livre")
    elif k in [str(i) for i in range(1, 10)]:
        idx = int(k) - 1
        if idx < len(PLANETAS):
            foco_camera = idx
            nave_x, nave_y = 0, 0
            print(f"Entrando em órbita de {PLANETAS[idx][0]}")

def mouse_click(btn, state, x, y):
    global mouse_down, mouse_x, mouse_y, zoom
    if btn == GLUT_LEFT_BUTTON:
        mouse_down = (state == GLUT_DOWN)
        mouse_x, mouse_y = x, y
    if foco_camera is None:
        if btn == 3: zoom += 2
        if btn == 4: zoom -= 2

def mouse_move(x, y):
    global cam_pitch, cam_yaw, mouse_x, mouse_y
    if mouse_down:
        dx = x - mouse_x
        dy = y - mouse_y
        cam_yaw += dx * 0.2
        cam_pitch += dy * 0.2
        mouse_x, mouse_y = x, y
        glutPostRedisplay()

def reshape(w, h):
    glViewport(0, 0, w, h or 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/(h or 1), 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(LARGURA_JANELA, ALTURA_JANELA)
    glutCreateWindow(b"Joguin")
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    inicializar_texturas()
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado)
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_move)
    glutMainLoop()

if __name__ == '__main__':
    main()