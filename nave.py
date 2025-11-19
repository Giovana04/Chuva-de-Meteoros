import sys
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

LARGURA_JANELA = 1200
ALTURA_JANELA = 800

movimentacao = [0,0,0]
# MOUSE
angulo_x = 20.0
angulo_y = 0.0
zoom = -90.0
mouse_x = 0
mouse_y = 0
botao_mouse_pressionado = False

def inicializar_camera():
    global angulo_x, angulo_y, zoom
    angulo_x = 20.0
    angulo_y = 40.0
    zoom = -60.0

def aplicar_camera():
    glTranslatef(0.0, 0.0, zoom)
    glRotatef(angulo_x, 1.0, 0.0, 0.0)
    glRotatef(angulo_y, 0.0, 1.0, 0.0)
    
def desenharNave():
    glBegin(GL_QUADS);
#   //Quad 1
    glColor3f(0.5,0.5,0.5);glVertex3f( 1.0, 2.0, 1.0);  
    glColor3f(0.5,0.5,0.5);glVertex3f( 1.0,-1.0, 1.0);   
    glColor3f(0.5,0.5,0.5);glVertex3f( 1.0,-1.0,-1.0);   
    glColor3f(0.5,0.5,0.5);glVertex3f( 1.0, 2.0,-1.0);
    #   //Quad 2
    glColor3f(0.5,0.5,0.5);glVertex3f( 1.0, 2.0,-1.0);   
    glColor3f(0.5,0.5,0.5);glVertex3f( 1.0,-1.0,-1.0);   
    glColor3f(0.5,0.5,0.5); glVertex3f(-1.0,-1.0,-1.0);   
    glColor3f(0.5,0.5,0.5);glVertex3f(-1.0, 2.0,-1.0);   
    
    glVertex3f(-1.0, 2.0,-1.0);   
    glVertex3f(-1.0,-1.0,-1.0);   
    glVertex3f(-1.0,-1.0, 1.0);  
    glVertex3f(-1.0, 2.0, 1.0);   
#   //Quad 4
    glVertex3f(-1.0, 2.0, 1.0);   
    glVertex3f(-1.0,-1.0, 1.0);   
    glVertex3f( 1.0,-1.0, 1.0);   
    glVertex3f( 1.0, 2.0, 1.0);   
  
  #Quad 5
    glVertex3f(-1.0, 2.0,-1.0);   
    glVertex3f(-1.0, 2.0, 1.0);   
    glVertex3f( 1.0, 2.0, 1.0);   
    glVertex3f( 1.0, 2.0,-1.0);  
   #Quad 6
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glEnd()
    glTranslatef(0,3,0)
    glBegin(GL_TRIANGLES);
#   //Triangle 1
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 1.0, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-1.0,-1.0, 1.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 1.0,-1.0, 1.0);   
#   //Triangle 2
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 1.0, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 1.0,-1.0, 1.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 1.0,-1.0,-1.0);   
#   //Triangle 3
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 1.0, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 1.0,-1.0,-1.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-1.0,-1.0,-1.0);   
#   //Triangle 4
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 1.0, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-1.0,-1.0,-1.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-1.0,-1.0, 1.0);   
    glEnd();
    
    glTranslatef(1,-2,0)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricNormals(quad, GLU_SMOOTH)
    glColor3f(0,0, 0.4)
    gluSphere(quad, 0.5, 10, 10)
    glTranslatef(-1,-1.5,1)
    glBegin(GL_TRIANGLES)
#   //Triangle 1
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 0.5, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-0.5,-0.5, 0.5);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.5,-0.5, 0.5);   
#   //Triangle 2
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 0.5, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.5,-0.5, 0.5);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.5,-0.5,-0.5);   
#   //Triangle 3
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 0.5, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.5,-0.5,-0.5);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-0.5,-0.5,-0.5);   
#   //Triangle 4
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 0.5, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-0.5,-0.5,-0.5);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-0.5,-0.5, 0.5);   
    glEnd();
    glTranslatef(0,0,-2)
    glBegin(GL_TRIANGLES)
#   //Triangle 1
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 0.5, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-0.5,-0.5, 0.5);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.5,-0.5, 0.5);   
#   //Triangle 2
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 0.5, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.5,-0.5, 0.5);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.5,-0.5,-0.5);   
#   //Triangle 3
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 0.5, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.5,-0.5,-0.5);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-0.5,-0.5,-0.5);   
#   //Triangle 4
    glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, 0.5, 0.0);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-0.5,-0.5,-0.5);   
    glColor3f(0.3,0.3,0.3); glVertex3f(-0.5,-0.5, 0.5);   
    glEnd();
    
    glTranslatef(0,-1,-0.3)
    glRotatef(180,0,0,1)
    glBegin(GL_TRIANGLE_FAN);
    glColor3f(1,1,0); glVertex3f( 0.0, 0.4, 0.0);   
    glColor3f(1,0,0); glVertex3f(-0.3,-0.4, 0.2);  
    glColor3f(1,0,0); glVertex3f( 0.3,-0.4, 0.2);   
    glColor3f(1,0,0); glVertex3f( 0.3,-0.4,-0.2);  
    glColor3f(1,0,0); glVertex3f(-0.3,-0.4,-0.2);   
    glColor3f(1,0,0); glVertex3f(-0.3,-0.4, 0.2);   
    glEnd()
    glTranslatef(0,0,2.4)
    
    glBegin(GL_TRIANGLE_FAN);
    glColor3f(1,1,0); glVertex3f( 0.0, 0.4, 0.0);   
    glColor3f(1,0,0); glVertex3f(-0.3,-0.4, 0.2);  
    glColor3f(1,0,0); glVertex3f( 0.3,-0.4, 0.2);   
    glColor3f(1,0,0); glVertex3f( 0.3,-0.4,-0.2);  
    glColor3f(1,0,0); glVertex3f(-0.3,-0.4,-0.2);   
    glColor3f(1,0,0); glVertex3f(-0.3,-0.4, 0.2);   
    glEnd()

# ---------- Renderização ----------
def display():
    global movimentacao
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #reset e aplica câmera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(movimentacao[0], movimentacao[1], movimentacao[2])
    aplicar_camera()
    glPushMatrix()
    desenharNave()
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
        mouse_x = x
        mouse_y = y
        glutPostRedisplay()
        
def teclado(tecla, x, y):
    print('AQ')
    print(tecla)
    global pausado, velocidade_tempo, movimentacao
    k = tecla.decode('utf-8') if isinstance(tecla, bytes) else tecla
    # print(k)
    if k == '\x1b':  # ESC
        sys.exit(0)
    elif k == 'w':
        movimentacao[2] += 0.2
        glutPostRedisplay()
    elif k == 's':
        movimentacao[2] -= 0.2
        glutPostRedisplay()
    elif k == 'a':
        movimentacao[0] += 0.2
        glutPostRedisplay()
    elif k == 'd':
        movimentacao[0] -= 0.2
        glutPostRedisplay()
    elif k == ' ':
        movimentacao[1] += 0.2
        glutPostRedisplay()
    elif k == '-':
        movimentacao[1] -= 0.2
        glutPostRedisplay()
        
    # elif k == 'r':
    #     resetar()W
    # elif k == '+':
    #     velocidade_tempo *= 1.5
    # elif k == '-':
    #     velocidade_tempo /= 1.5
    elif k == 'p':
        pausado = not pausado
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(LARGURA_JANELA, ALTURA_JANELA)
    glutCreateWindow(b"Sistema Solar")

    init_gl()
    inicializar_camera()
    # funções de evento
    glutDisplayFunc(display) 
    # glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado)

    glutMouseFunc(evento_mouse)
    glutMotionFunc(evento_mouse_movimento)

    glutMainLoop()

if __name__ == '__main__':
    main()
