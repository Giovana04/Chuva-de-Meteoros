from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from suporteObjetos import *

class objeto:

    def __init__(self, x, y ,z, xTamMax, yTamMax, zTamMax, xTamMin, yTamMin, zTamMin):
        self.posicao = [x,y,z]
        self.tamMax = [xTamMax,yTamMax,zTamMax]
        self.tamMin = [xTamMin, yTamMin, zTamMin]
    def movimentar(self, x,y,z):
        self.posicao[0] += x
        self.posicao[1] += y
        self.posicao[2] += z
texturas = {}
def carregar_textura(arquivo):
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

def inicializar_texturas():
    global texturas
    arquivos = ["asteroid.jpg"]
    for f in arquivos:
        if f in texturas:
            continue
        texturas[f] = carregar_textura(f)
    print("texturas carregadas:", list(texturas.items()))
    
    


def desenharAsteroide(i, meteorosObjetos):
    glTranslatef(meteorosObjetos[i].posicao[0],meteorosObjetos[i].posicao[1],meteorosObjetos[i].posicao[2])
    glPushMatrix()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texturas['asteroid.jpg']) 
    glColor3d(1,0.3,0)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 2.5, 32, 32) 
    gluDeleteQuadric(quad)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glTranslate(1, 2,0)
    glRotate(-15,0,0,1)
    glBegin(GL_TRIANGLE_FAN);
    glColor3f(1,1,0); glVertex3f( 0.0, 8, 0.0);   
    glColor3f(1,0,0); glVertex3f(-2,-1, 1);  
    glColor3f(1,0,0); glVertex3f( 2,-1, 1);   
    glColor3f(1,0,0); glVertex3f( 2,-1,-1);  
    glColor3f(1,0,0); glVertex3f(-2,-1,-1);   
    glColor3f(1,0,0); glVertex3f(-2,-1, 1);   
    glEnd()
    glTranslate(-1,0,0)
    glRotatef(5,0,0,1)
    glBegin(GL_TRIANGLE_FAN);
    glColor3f(1,0.6,0); glVertex3f( 0.0, 6, 0.0);   
    glColor3f(1,0,0); glVertex3f(-1,-1, 1);  
    glColor3f(1,0,0); glVertex3f( 1,-1, 1);   
    glColor3f(1,0,0); glVertex3f( 1,-1,-1);  
    glColor3f(1,0,0); glVertex3f(-1,-1,-1);   
    glColor3f(1,0,0); glVertex3f(-1,-1, 1);   
    
    glEnd()
    glTranslate(-1,0,0)
    glRotatef(5,0,0,1)
    glBegin(GL_TRIANGLE_FAN);
    glColor3f(1,0.6,0); glVertex3f( 0.0, 4, 0.0);   
    glColor3f(1,0,0); glVertex3f(-1,-1, 1);  
    glColor3f(1,0,0); glVertex3f( 1,-1, 1);   
    glColor3f(1,0,0); glVertex3f( 1,-1,-1);  
    glColor3f(1,0,0); glVertex3f(-1,-1,-1);   
    glColor3f(1,0,0); glVertex3f(-1,-1, 1);   
    glEnd()
    glTranslatef(meteorosObjetos[i].posicao[0]*-1, meteorosObjetos[i].posicao[1]*-1,meteorosObjetos[i].posicao[2]*-1)
   
def desenharNave():
    global nave
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