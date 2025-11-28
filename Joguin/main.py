# main.py
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from objetos import *
# from regras import *

MENU = 0
REGRAS = 1
JOGO = 2
EXPLORAR = 3

estado_atual = MENU
sistema = SistemaSolar()

LARGURA = 1200
ALTURA = 800

# Variáveis globais de mouse
mouse_down = False
last_x, last_y = 0, 0

def desenhar_texto(x, y, texto, tamanho=GLUT_BITMAP_HELVETICA_18):
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST) 
    glDisable(GL_TEXTURE_2D)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, LARGURA, 0, ALTURA)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x, y)
    
    for char in texto:
        glutBitmapCharacter(tamanho, ord(char))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)

def desenhar_texto_centralizado(y, texto, fonte, cor):
    largura_texto = 0
    for char in texto:
        largura_texto += glutBitmapWidth(fonte, ord(char))
    
    x = (LARGURA - largura_texto) / 2
    
    glColor3f(*cor)
    glRasterPos2f(x, y)
    for char in texto:
        glutBitmapCharacter(fonte, ord(char))

def desenhar_linha(y, espessura=1.0):
    glLineWidth(espessura)
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(LARGURA/2 - 200, y)
    glVertex2f(LARGURA/2 + 200, y)
    glEnd()

def desenhar_caixa(): # apanhei nessa ta kkkkkkk
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glColor4f(0.0, 0.1, 0.2, 0.9) 
    glBegin(GL_QUADS)
    glVertex2f(0, 0); glVertex2f(LARGURA, 0)
    glVertex2f(LARGURA, 80); glVertex2f(0, 80) 
    glEnd()
    
    glColor3f(0.0, 1.0, 1.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(0, 80); glVertex2f(LARGURA, 80)
    glEnd()
    glDisable(GL_BLEND)


def display():
    global estado_atual
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    sistema.desenhar_cenario()
    
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    gluOrtho2D(0, LARGURA, 0, ALTURA)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)
    
    # Pra ficar mais escuro o fundo no menu e regras
    if estado_atual == MENU or estado_atual == REGRAS:
        glDisable(GL_LIGHTING); glDisable(GL_DEPTH_TEST); glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glBegin(GL_QUADS)
        glColor4f(0.05, 0.05, 0.1, 0.95) 
        glVertex2f(0, 0); glVertex2f(LARGURA, 0)
        glColor4f(0.0, 0.0, 0.0, 0.85)
        glVertex2f(LARGURA, ALTURA); glVertex2f(0, ALTURA)
        glEnd()
        glDisable(GL_BLEND)


    FONTE_TITULO = GLUT_BITMAP_TIMES_ROMAN_24
    FONTE_TEXTO = GLUT_BITMAP_HELVETICA_18

    if estado_atual == MENU:
        desenhar_texto_centralizado(ALTURA/2 + 80, "Joguin", FONTE_TITULO, (0.0, 1.0, 1.0)) # Ciano
        desenhar_texto_centralizado(ALTURA/2 + 50, "Feito por: Ana Beatriz B. S. Henrique e Giovana F. Nascimento", FONTE_TEXTO, (0.7, 0.7, 0.7)) # Cinza
        
        desenhar_linha(ALTURA/2 + 30)
        
        y_base = ALTURA/2 - 20
        desenhar_texto_centralizado(y_base, "ENTER", FONTE_TEXTO, (1.0, 1.0, 0.0)) # Amarelo
        desenhar_texto_centralizado(y_base - 25, "Jogo", FONTE_TEXTO, (1.0, 1.0, 1.0))
        
        desenhar_texto_centralizado(y_base - 70, "i", FONTE_TEXTO, (1.0, 1.0, 0.0))
        desenhar_texto_centralizado(y_base - 95, "Controles", FONTE_TEXTO, (1.0, 1.0, 1.0))
        
        desenhar_texto_centralizado(y_base - 140, "E", FONTE_TEXTO, (1.0, 1.0, 0.0))
        desenhar_texto_centralizado(y_base - 165, "Modo Livre", FONTE_TEXTO, (1.0, 1.0, 1.0))

    elif estado_atual == REGRAS:
        y_cursor = ALTURA - 100 
        
        desenhar_texto_centralizado(y_cursor, "Controles", FONTE_TITULO, (1.0, 0.5, 0.0)) # Laranja
        desenhar_linha(y_cursor - 20)
        
        margem_esq = LARGURA/2 - 300 
        y_cursor -= 60 
        
        textos_controles = [
            "- Use [W, A, S, D] para pilotar e desviar no modo jogo.",
            "- Apenas mover o mouse já moverá a câmera no modo jogo.",
            "- No modo exploração é necessário clicar e segurar para mover.",
            "- No modo exploração é possível dar zoom com o scroll.",
            "- No modo exploração use [- / +] para a velocidade."
        ]

        glColor3f(0.9, 0.9, 0.9) 
        
        for frase in textos_controles:
            glRasterPos2f(margem_esq, y_cursor) 
            for c in frase:
                glutBitmapCharacter(FONTE_TEXTO, ord(c)) 
            y_cursor -= 30

        y_cursor -= 40
        
        desenhar_texto_centralizado(y_cursor, "Regras do Jogo", FONTE_TITULO, (1.0, 0.5, 0.0)) 
        desenhar_linha(y_cursor - 20)
        
        y_cursor -= 60 
        
        textos_regras = [
            "- Desvie dos meteoros! Se for atingido, voltará a primeira fase.",
            "- Termine 3 voltas no planeta para passar de fase."
        ]
        glColor3f(0.9, 0.9, 0.9) 
        
        for frase in textos_regras:
            glRasterPos2f(margem_esq, y_cursor)
            for c in frase:
                glutBitmapCharacter(FONTE_TEXTO, ord(c))
            y_cursor -= 30

        desenhar_texto_centralizado(50, "Pressione ESC para voltar", FONTE_TEXTO, (1.0, 1.0, 0.0)) 

    elif estado_atual == JOGO:
        desenhar_caixa()
        if(not sistema.verificaInicializado()):
            sistema.inicializarMeteoros()
       
        # Info do Planeta (Esquerda)
        planeta = sistema.PLANETAS[sistema.foco_camera][0].replace('.jpg','').replace('.png','').upper()
        glColor3f(0.0, 1.0, 1.0) # Título Ciano
        glRasterPos2f(30, 50)
        for c in "Planeta atual:": glutBitmapCharacter(FONTE_TEXTO, ord(c))
        
        glColor3f(1.0, 1.0, 1.0) # Nome Branco
        glRasterPos2f(30, 25)
        for c in planeta: glutBitmapCharacter(FONTE_TITULO, ord(c))
        # Controles (Direita)
        msg = "ESC: Menu  |  Mova o mouse: Câmera  |  +/- : Velocidade do tempo | Escolher fase: 1 - 8"
        largura = 0
        for c in msg: largura += glutBitmapWidth(FONTE_TEXTO, ord(c))
        
        glColor3f(0.7, 0.7, 0.7)
        glRasterPos2f(LARGURA - largura - 30, 35)
        for c in msg: glutBitmapCharacter(FONTE_TEXTO, ord(c))
        
        if(sistema.getColisao()):
            print("AQUI???????????????")
            estado_atual = MENU
            sistema.foco_camera = None 
            sistema.zoom = -60
            sistema.cam_pitch = 20
            sistema.cam_yaw = 0
            sistema.inverteColisao()

    elif estado_atual == EXPLORAR:
        desenhar_caixa()
        
        glColor3f(0.0, 1.0, 0.0) # Verde Matrix
        glRasterPos2f(30, 40)
        for c in "MODO LIVRE": glutBitmapCharacter(FONTE_TITULO, ord(c))
        
        msg = "Clique+Arraste: Girar | Scroll: Zoom | ESC: Volta | +/- : Velocidade do giro"
        largura = 0
        for c in msg: largura += glutBitmapWidth(FONTE_TEXTO, ord(c))
        glColor3f(0.7, 0.7, 0.7)
        glRasterPos2f(LARGURA - largura - 30, 35)
        for c in msg: glutBitmapCharacter(FONTE_TEXTO, ord(c))

    glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING); glEnable(GL_DEPTH_TEST)

    glutSwapBuffers()

def idle():
    sistema.atualizar() 
    glutPostRedisplay()

def reshape(w, h):
    global LARGURA, ALTURA
    LARGURA, ALTURA = w, h or 1
    glViewport(0, 0, w, h or 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/(h or 1), 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(LARGURA, ALTURA)
    glutCreateWindow(b"Joguin")
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    
    sistema.inicializar_texturas()
    
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado)
    
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_move)
    glutPassiveMotionFunc(mouse_passivo)
    
    glutMainLoop()
    
    

def teclado(key, x, y):
    global estado_atual
    k = key.decode('utf-8').lower()
    # Controles que funcionam sempre
    if k == '\x1b': # ESC
        if estado_atual == MENU:
            sys.exit(0)
        else:
            estado_atual = MENU
            sistema.foco_camera = None 
            sistema.zoom = -60
            sistema.cam_pitch = 20
            sistema.cam_yaw = 0
            
    elif k == '+' or k == '=':
        sistema.velocidade_tempo *= 1.5
    elif k == '-' or k == '_':
        sistema.velocidade_tempo /= 1.5

    if estado_atual == MENU:
        if k == '\r' or k == '\n': 
            estado_atual = JOGO
            sistema.foco_camera = 0 
            sistema.nave_x, sistema.nave_y = 0, 0
            sistema.cam_pitch, sistema.cam_yaw = 0, 0
        elif k == 'i': estado_atual = REGRAS
        elif k == 'e':
            estado_atual = EXPLORAR
            sistema.foco_camera = None
            sistema.zoom = -60

    elif estado_atual == JOGO:
        sistema.input_nave(k)
        if k in [str(i) for i in range(1, 9)]:
            idx = int(k) - 1
            sistema.foco_camera = idx
            sistema.nave_x, sistema.nave_y = 0, 0
            sistema.quantidadeCometas(k)

    glutPostRedisplay()

def mouse_click(btn, state, x, y):
    global mouse_down, last_x, last_y
    if estado_atual == EXPLORAR:
        if btn == GLUT_LEFT_BUTTON:
            mouse_down = (state == GLUT_DOWN)
            last_x, last_y = x, y
        elif btn == 3: sistema.zoom += 2
        elif btn == 4: sistema.zoom -= 2
        glutPostRedisplay()

def mouse_move(x, y): #esse precisa clicar pra mover (pra explorar)
    global last_x, last_y
    if estado_atual == EXPLORAR and mouse_down:
        dx = x - last_x
        dy = y - last_y
        sistema.cam_yaw += dx * 0.2
        sistema.cam_pitch -= dy * 0.2 
        last_x, last_y = x, y
        glutPostRedisplay()

def mouse_passivo(x, y): # não sei se essa é a palavra mas move o mouse sem precisar clicar kkkkkk
    global last_x, last_y
    if estado_atual == JOGO:
        dx = x - last_x
        dy = y - last_y
        
        if abs(dx) < 50 and abs(dy) < 50:
            sistema.cam_yaw += dx * 0.2
            sistema.cam_pitch -= dy * 0.2
            
        glutPostRedisplay()
    last_x, last_y = x, y

if __name__ == '__main__':
    main()