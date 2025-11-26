import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from suporteObjetos import *
import random


meteoros = [0,0,0,0,0,0,0,0]
meteorosObjetos = []
for i in range (0,8):
    meteorosObjetos.append(objeto(0,20,-8 + i*5,3,9,3,-3,-3,-3))
LARGURA_JANELA = 1200
ALTURA_JANELA = 800
nave = objeto(0,0,0, 1.8, 3.9, 1.5, -1, -2, -1.5)
velocidade_tempo = 0.02

# MOUSE
angulo_x = 20.0
angulo_y = 0.0
zoom = -90.0
mouse_x = 0
mouse_y = 0
botao_mouse_pressionado = False

def aleatorizar():
    global meteoros
    qntd = 2
    for i in range(0,len(meteoros)):
        meteoros[i] = 0
    for i in range(0 ,qntd):
        val = random.randint(0,7)
        if(meteoros[val] == 0):
            meteoros[val] = 1
        else:
            for j in range(0,8):
                if(meteoros[j] == 0):
                    meteoros[j] = 1
                    break
def idle():
    global angulos, angulo_lua, velocidade_tempo
    global meteorosObjetos
    for i in range(0,8):
        if(meteoros[i] == 1):
            meteorosObjetos[i].posicao[1] -= 0.1*velocidade_tempo
            if(checarColisaoNave(meteorosObjetos[i])):
                glutLeaveMainLoop()
            if(meteorosObjetos[i].posicao[1] <= -6.48):
                meteoros[i] = 0
                meteorosObjetos[i] = objeto(0,20,-8 + i*5,3,9,3,-3,-3,-3)
                aleatorizar()
    glutPostRedisplay()


def inicializar_camera():
    global angulo_x, angulo_y, zoom
    angulo_x = 20.0
    angulo_y = 40.0
    zoom = -60.0

def aplicar_camera():
    glTranslatef(0.0, 0.0, zoom)
    glRotatef(angulo_x, 1.0, 0.0, 0.0)
    glRotatef(angulo_y, 0.0, 1.0, 0.0)
def checarColisaoNave(meteoro):
    global nave
    if nave.posicao[0] + nave.tamMin[0] > meteoro.posicao[0] + meteoro.tamMin[0] and nave.posicao[0] + nave.tamMax[0] < meteoro.posicao[0] + meteoro.tamMax[0]:
        if nave.posicao[1] + nave.tamMin[1] > meteoro.posicao[1] + meteoro.tamMin[1] and nave.posicao[1] + nave.tamMax[1] < meteoro.posicao[1] + meteoro.tamMax[1]:
            if nave.posicao[2] + nave.tamMin[2] > meteoro.posicao[2] + meteoro.tamMin[2] and nave.posicao[2] + nave.tamMax[2] < meteoro.posicao[2] + meteoro.tamMax[2]:
                return True
    return False


# ---------- Renderização ----------
def display():
    global angulo_x, angulo_y, nave, meteorosObjetos
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #reset e aplica câmera
    glMatrixMode(GL_MODELVIEW)
    
    glLoadIdentity()

    aplicar_camera()

    glTranslatef(nave.posicao[0], nave.posicao[1], nave.posicao[2])
    glPushMatrix()
    desenharNave()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-nave.posicao[0],-nave.posicao[1],-nave.posicao[2])
    for i in range(0,8):
        if(meteoros[i] == 1):
            desenharAsteroide(i, meteorosObjetos)
    glPopMatrix()
    glutSwapBuffers()


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

def evento_mouse(botao, estado, x, y):
    global botao_mouse_pressionado, mouse_x, mouse_y, zoom
    if botao == GLUT_LEFT_BUTTON:
        if estado == GLUT_DOWN:
            botao_mouse_pressionado = True
            mouse_x = x
            mouse_y = y
        else:
            botao_mouse_pressionado = False
    # scroll 3 cima, 4 baixo
    if botao == 3:
        zoom += 3.0
        glutPostRedisplay() # faz a tela redesenhar
    elif botao == 4:
        zoom -= 3.0
        glutPostRedisplay()

def evento_mouse_movimento(x, y):
    global mouse_x, mouse_y, angulo_x, angulo_y, botao_mouse_pressionado
    if botao_mouse_pressionado:
        dx = x - mouse_x
        dy = y - mouse_y
        angulo_y += dx * 0.2 # sensibilide, pega o dx para angulo_y porque gira em torno do eixo y
        angulo_x += dy * 0.2
        # limita ângulos pra não virar tudo de ponta cabeça
        if angulo_x > 89: angulo_x = 89
        if angulo_x < -89: angulo_x = -89
        if angulo_y > 359 : angulo_y=0
        if angulo_y < -359 : angulo_y=0
        mouse_x = x
        mouse_y = y
        glutPostRedisplay()
        
def teclado(tecla, x, y):
    global pausado, velocidade_tempo, nave
    k = tecla.decode('utf-8') if isinstance(tecla, bytes) else tecla
    if k == '\x1b':  # ESC
        sys.exit(0)
    elif k == 'a':
        nave.posicao[2] += 0.2
        glutPostRedisplay()
    elif k == 'd':
        nave.posicao[2] -= 0.2
        glutPostRedisplay()
    elif k == 'w':
        nave.posicao[0] += 0.2
        glutPostRedisplay()
    elif k == 's':
        nave.posicao[0] -= 0.2
        glutPostRedisplay()
    elif k == ' ':
        nave.posicao[1] += 0.2
        glutPostRedisplay()
    elif k == '-':
        nave.posicao[1] -= 0.2
        glutPostRedisplay()
    elif k == 'p':
        pausado = not pausado
def main():
    glutInit(sys.argv)
    aleatorizar()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(LARGURA_JANELA, ALTURA_JANELA)
    glutCreateWindow(b"Sistema Solar")
    init_gl()
    inicializar_texturas()
    inicializar_camera()
    # funções de evento
    glutDisplayFunc(display) 
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado)
    glutMouseFunc(evento_mouse)
    glutMotionFunc(evento_mouse_movimento)

    glutMainLoop()

if __name__ == '__main__':
    main()
