import sys
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

LARGURA_JANELA = 1200
ALTURA_JANELA = 800

texturas = {}
# arquivo_textura, raio, distancia_do_sol, velocidade em torno do sol
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

RAIO_SCALE = 0.16     # raios dos planetas
DIST_SCALE = 3.0      # multiplica as distâncias

rotacao_planetas = [0.0 for _ in range(len(PLANETAS))]

# estado da animação
velocidade_tempo = 0.2
angulos = [0.0 for _ in range(len(PLANETAS))]
angulo_lua = 0.0
pausado = False

# CONTROLE DE CÂMERA
# None = Livre, -1 = Sol, 0...N = Índice do planeta
foco_camera = None 

def carregar_textura(arquivo):
    try:
        img = Image.open(arquivo)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGBA").tobytes()
        largura, altura = img.size
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return tex_id
    except:
        print(f"Erro ao carregar textura: {arquivo}")
        return 0

def inicializar_texturas():
    global texturas
    arquivos = [p[0] for p in PLANETAS]
    arquivos += ["sol.png", "lua.png", "anelSaturno.png", "estrelas.png"]    
    for f in arquivos:
        if f in texturas:
            continue
        texturas[f] = carregar_textura(f)
    print("Texturas carregadas.")

def posicionar_luz_no_sistema():
    pos_luz = [0.0, 0.0, 0.0, 1.0]
    INTENSIDADE_SOL = 1.5

    difuso   = [1.0 * INTENSIDADE_SOL] * 3 + [1.0]
    especular = [1.0 * INTENSIDADE_SOL] * 3 + [1.0]
    ambiente = [0.05 * INTENSIDADE_SOL] * 3 + [1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, pos_luz)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, difuso)
    glLightfv(GL_LIGHT0, GL_SPECULAR, especular)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambiente)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def desenhar_esfera_texturizada(tex_id, raio, horizontal=32, vertical=32):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, raio, horizontal, vertical)
    glDisable(GL_TEXTURE_2D)

# MOUSE
angulo_x = 20.0
angulo_y = 0.0
zoom = -60.0
mouse_x = 0
mouse_y = 0
botao_mouse_pressionado = False

def inicializar_camera():
    global angulo_x, angulo_y, zoom
    angulo_x = 20.0
    angulo_y = 40.0
    zoom = -60.0

def aplicar_camera():
    global foco_camera

    # Modo Livre
    if foco_camera is None:
        glTranslatef(0.0, 0.0, zoom)
        glRotatef(angulo_x, 1.0, 0.0, 0.0)
        glRotatef(angulo_y, 0.0, 1.0, 0.0)
        return

    # Modo Primeira Pessoa (fixo em objeto)
    glRotatef(angulo_x, 1.0, 0.0, 0.0) # pescoço
    glRotatef(angulo_y, 0.0, 1.0, 0.0)

    if foco_camera == -1:
        # Move para a superfície do sol
        glTranslatef(0.0, 0.0, -5.0) 
    else: # Move pros planetas
        i = foco_camera
        p = PLANETAS[i]
        raio = p[1] * RAIO_SCALE
        dist = p[2] * DIST_SCALE
        
        # Matemática Inversa para grudar no planeta
        # Afasta para a superfície
        glTranslatef(0.0, 0.0, -raio - 0.5) 
        # Desfaz rotação do planeta (para girar junto)
        glRotatef(-rotacao_planetas[i], 0.0, 1.0, 0.0)
        # Desfaz translação da órbita
        glTranslatef(-dist, 0.0, 0.0)
        # Desfaz rotação da órbita
        glRotatef(-angulos[i], 0.0, 1.0, 0.0)

def evento_mouse(botao, estado, x, y):
    global botao_mouse_pressionado, mouse_x, mouse_y, zoom
    if botao == GLUT_LEFT_BUTTON:
        if estado == GLUT_DOWN:
            botao_mouse_pressionado = True
            mouse_x = x
            mouse_y = y
        else:
            botao_mouse_pressionado = False
    
    # Zoom só funciona no modo livre
    if foco_camera is None:
        if botao == 3:
            zoom += 3.0
            glutPostRedisplay()
        elif botao == 4:
            zoom -= 3.0
            glutPostRedisplay()

def evento_mouse_movimento(x, y):
    global mouse_x, mouse_y, angulo_x, angulo_y, botao_mouse_pressionado
    if botao_mouse_pressionado:
        dx = x - mouse_x
        dy = y - mouse_y
        angulo_y += dx * 0.2
        angulo_x += dy * 0.2
        
        if angulo_x > 89: angulo_x = 89
        if angulo_x < -89: angulo_x = -89
        
        mouse_x = x
        mouse_y = y
        glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Desenha o céu (Estrelas)
    glPushMatrix()
    # No céu, aplicamos apenas a rotação da câmera, sem translação
    glRotatef(angulo_x, 1.0, 0.0, 0.0)
    glRotatef(angulo_y, 0.0, 1.0, 0.0)
    
    desenhar_ceu()
    glPopMatrix()

    # Aplica a câmera fora
    glLoadIdentity()
    aplicar_camera()

    posicionar_luz_no_sistema()

    # SOL
    glPushMatrix()
    glDisable(GL_LIGHTING)
    if texturas.get('sol.png', 0):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texturas['sol.png']) 
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, 3.8, 32, 32)
        gluDeleteQuadric(quad)
        glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # PLANETAS
    for i, p in enumerate(PLANETAS): 
        arquivo, raio_raw, dist_raw, velocidade, = p 
        raio = raio_raw * RAIO_SCALE
        dist = dist_raw * DIST_SCALE

        glPushMatrix()
        
        # Orbita
        glRotatef(angulos[i], 0.0, 1.0, 0.0)
        glTranslatef(dist, 0.0, 0.0)
        
        # Rotação própria
        glRotatef(rotacao_planetas[i], 0.0, 1.0, 0.0)
        
        if i == INDICE_TERRA:
            desenhar_esfera_texturizada(texturas.get('terra.jpg', 0), raio)
            # Lua
            glPushMatrix()
            glRotatef(angulo_lua, 0.0, 1.0, 0.0)
            glTranslatef((1 + raio_raw) * RAIO_SCALE + raio, 0.0, 0.0)
            desenhar_esfera_texturizada(texturas.get('lua.png', 0), 0.27 * RAIO_SCALE)
            glPopMatrix()
            
        elif i == INDICE_SATURNO:
            desenhar_esfera_texturizada(texturas.get(arquivo, 0), raio)
            glPushMatrix()
            glRotatef(80.0, 1.0, 0.0, 0.0) 
            glDisable(GL_LIGHTING)
            glDisable(GL_CULL_FACE) 
            glEnable(GL_TEXTURE_2D)
            tex_anel = texturas.get('anelSaturno.png', 0)
            if tex_anel:
                glBindTexture(GL_TEXTURE_2D, tex_anel)
            disk = gluNewQuadric()
            gluQuadricTexture(disk, GL_TRUE)
            gluDisk(disk, raio * 1.2, raio * 2.2, 64, 1)
            gluDeleteQuadric(disk)
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_LIGHTING)
            glPopMatrix()
        else:
            desenhar_esfera_texturizada(texturas.get(arquivo, 0), raio)

        glPopMatrix()

    glutSwapBuffers()
    
def desenhar_ceu():
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glDisable(GL_CULL_FACE)
    glDepthMask(GL_FALSE)
    glEnable(GL_TEXTURE_2D)
    tex_id = texturas.get('estrelas.png', 0)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, 100.0, 34, 34) 
    gluDeleteQuadric(quad)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glDepthMask(GL_TRUE)
    glPopMatrix()

def idle():
    global angulos, angulo_lua, rotacao_planetas
    if not pausado:
        for i, p in enumerate(PLANETAS):
            velocidade = p[3]
            angulos[i] = (angulos[i] + velocidade * velocidade_tempo) % 360.0
            # Rotação do planeta no próprio eixo
            rotacao_planetas[i] = (rotacao_planetas[i] + 1.2 * velocidade_tempo) % 360.0

        angulo_lua = (angulo_lua + 5.0 * velocidade_tempo) % 360.0
        glutPostRedisplay()

def teclado(tecla, x, y):
    global pausado, velocidade_tempo, foco_camera
    k = tecla.decode('utf-8')
    
    if k == '\x1b':  # ESC
        sys.exit(0)
    elif k == 'r':
        resetar()
    elif k == '+':
        velocidade_tempo *= 1.5
    elif k == '-':
        velocidade_tempo /= 1.5
    elif k == 'p':
        pausado = not pausado
        
    # SELEÇÃO DE CÂMERA
    elif k == '0': # Livre
        foco_camera = None
        print("Câmera Livre")
    elif k == '1': # Sol
        foco_camera = -1
        print("Câmera Sol")
    elif k in [str(n) for n in range(2, 10)]: # Planetas 2-9
        idx = int(k) - 2
        if idx < len(PLANETAS):
            foco_camera = idx
            print(f"Câmera: {PLANETAS[idx][0]}")

def resetar():
    global angulos, angulo_lua, velocidade_tempo, pausado, foco_camera
    angulos = [0.0 for _ in range(len(PLANETAS))]
    angulo_lua = 0.0
    velocidade_tempo = 0.2
    pausado = False
    foco_camera = None
    inicializar_camera()

def reshape(largura, altura):
    if altura == 0:
        altura = 1
    glViewport(0, 0, largura, altura)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(largura)/float(altura), 0.1, 2000.0)
    glMatrixMode(GL_MODELVIEW)

def init_gl():
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    
    mat_diffuse = [1.0, 1.0, 1.0, 1.0]
    mat_specular = [0.2, 0.2, 0.2, 1.0]
    mat_shininess = [10.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(LARGURA_JANELA, ALTURA_JANELA)
    glutCreateWindow(b"Sistema Solar Primeira Pessoa")

    init_gl()
    inicializar_texturas()
    inicializar_camera()
    
    glutDisplayFunc(display) 
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado)
    glutMouseFunc(evento_mouse)
    glutMotionFunc(evento_mouse_movimento)

    glutMainLoop()

if __name__ == '__main__':
    main()