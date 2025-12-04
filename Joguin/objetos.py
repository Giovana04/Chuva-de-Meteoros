import math
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import regras
import random

class objeto:
    def __init__(self, x, y ,z, xTamMax, yTamMax, zTamMax, xTamMin, yTamMin, zTamMin):
        self.posicao = [x,y,z]
        self.tamMax = [xTamMax,yTamMax,zTamMax]
        self.tamMin = [xTamMin, yTamMin, zTamMin]
    def movimentar(self, x,y,z):
        self.posicao[0] += x
        self.posicao[1] += y
        self.posicao[2] += z
        
class SistemaSolar:
    def __init__(self):
        # Configurações
        self.PLANETAS = [
            ("mercurio.jpg", 1, 2.0, 4),
            ("venus.jpg",    3, 3.0, 1.5),
            ("terra.jpg",    7, 4.5, 1),
            ("marte.jpg",    1, 6.0, 0.5),
            ("jupiter.png",  20, 10.0, 0.2),
            ("saturno.png",  17, 14.0, 0.15),
            ("urano.png",    10, 18.0, 0.1),
            ("netuno.png",   10, 22.0, 0.08),
        ]
        self.RAIO_SCALE = 0.16 
        self.DIST_SCALE = 3.0
        
        # Estado do Sistema
        self.rotacao_planetas = [0.0] * len(self.PLANETAS)
        self.angulos = [0.0] * len(self.PLANETAS)
        self.angulo_lua = 0.0
        self.velocidade_tempo = 0.2
        self.texturas = {}
        
        # Estado do Jogo/Câmera
        self.foco_camera = None
        self.cam_pitch = 0.0
        self.cam_yaw = 0.0
        self.zoom = -60.0
        
        self.colisao = False        
        # Estado da Nave
        self.nave_x = 0.0
        self.nave_y = 0.0
        self.nave_roll = 0.0
        self.texturas_carregadas = False
        
        self.meteoros = [0] * 10
        self.meteorosObjetos = []
        self.meteoroInicializado = False
        self.qntd = 2 
        
        self.timer_spawn = 0
        self.tempo_espera_max = 40 
        self.esperando_reset = False
        
        tamanho_hitbox = 0.15
        for i in range(10):
            if(i < 5):
                y_random = random.uniform(-1.2, 1.2)
                self.meteorosObjetos.append(objeto(-4, y_random, 0, tamanho_hitbox, tamanho_hitbox, 0, -tamanho_hitbox, -tamanho_hitbox, 0))
            else:
                y_random = random.uniform(-1.2, 1.2)
                self.meteorosObjetos.append(objeto(4, y_random, 0, tamanho_hitbox, tamanho_hitbox, 0, -tamanho_hitbox, -tamanho_hitbox, 0))
                
    def verificaInicializado(self):
        if(self.meteoroInicializado):
            return True
        else:
            self.meteoroInicializado = True
            return False

    def carregar_textura(self, arquivo):
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
            print(f"ERRO: Textura {arquivo} nao encontrada.")
            return 0

    def inicializarMeteoros(self):
        self.meteorosObjetos.clear()
        tamanho_hitbox = 0.15 
        
        for i in range (0, 10):
            if(i < 5):
                self.meteorosObjetos.append(objeto(-4, -0.5+i*0.6, 0, tamanho_hitbox, tamanho_hitbox, 0, -tamanho_hitbox, -tamanho_hitbox, 0))
            else:
                self.meteorosObjetos.append(objeto(4, -0.5+(i-5)*0.6, 0, tamanho_hitbox, tamanho_hitbox, 0, -tamanho_hitbox, -tamanho_hitbox, 0))
        self.meteoros = regras.aleatorizar(self.meteoros, self.qntd)
        
    def inicializar_texturas(self):
        if self.texturas_carregadas: return
        arquivos = [p[0] for p in self.PLANETAS] + ["sol.png", "lua.png", "anelSaturno.png", "estrelas.png", "asteroid.jpg"]    
        for f in arquivos:
            if f not in self.texturas: self.texturas[f] = self.carregar_textura(f)
        self.texturas_carregadas = True

    def desenhar_esfera(self, tex_id, raio):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glColor3f(1.0, 1.0, 1.0) 
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, raio, 32, 32)
        glDisable(GL_TEXTURE_2D)

    def desenhar_ceu(self): 
        glDisable(GL_LIGHTING)
        glDepthMask(GL_FALSE)
        glEnable(GL_TEXTURE_2D)
        tex_id = self.texturas.get('estrelas.png', 0)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glColor3f(1.0, 1.0, 1.0)
        q = gluNewQuadric()
        gluQuadricTexture(q, True)
        gluSphere(q, 150.0, 20, 20)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glDepthMask(GL_TRUE)

    def aplicar_camera(self): 
        if self.foco_camera is None: 
            glTranslatef(0.0, 0.0, self.zoom)
            glRotatef(self.cam_pitch + 20, 1.0, 0.0, 0.0)
            glRotatef(self.cam_yaw, 0.0, 1.0, 0.0)
            return

        idx = self.foco_camera
        p = self.PLANETAS[idx]
        dist = p[2] * self.DIST_SCALE
        ang = self.angulos[idx]
        raio = p[1] * self.RAIO_SCALE

        # aplica rotações da câmera (pitch/yaw)
        glRotatef(-self.cam_pitch, 1.0, 0.0, 0.0)
        glRotatef(self.cam_yaw, 0.0, 1.0, 0.0)

        # gira o sistema para alinhar com a órbita do planeta escolhido
        glRotatef(-ang - 90, 0.0, 1.0, 0.0)

        # move a cena para posicionar a câmera sobre o planeta
        glTranslatef(-dist, 0.0, 0.0)
        glTranslatef(0.0, -raio - 1.5, 0.0)

        if self.foco_camera is None:
            glTranslatef(0.0, 0.0, self.zoom)
        else:
        # Um pequeno ajuste fixo pra não entrar dentro da textura do chão
            glTranslatef(0.0, 0.0, -2.0)

    def desenhar_hud_nave(self):
        if self.foco_camera is None: return

        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -4.0) 
        glRotatef(self.nave_roll, 0.0, 0.0, 1.0)
        self.nave_roll *= 0.9

        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.4, 0.8, 1.0, 0.15) 
        glLineWidth(1.0)

        offset_z = (self.angulo_lua * 0.1) % 1.0 
        LARGURA_GRID, ALTURA_GRID = 3.0, 1.5
        glColor3f(1,1,1)
        glBegin(GL_LINES)
        for i in range(-3, 4): 
            glVertex3f(i, -ALTURA_GRID, -10.0); glVertex3f(i, -ALTURA_GRID,  2.0)
            glVertex3f(i,  ALTURA_GRID, -10.0); glVertex3f(i,  ALTURA_GRID,  2.0)
        for k in range(10): # linha horizontal
            z = -k + offset_z
            glVertex3f(-LARGURA_GRID, -ALTURA_GRID, z); glVertex3f( LARGURA_GRID, -ALTURA_GRID, z)
            glVertex3f(-LARGURA_GRID,  ALTURA_GRID, z); glVertex3f( LARGURA_GRID,  ALTURA_GRID, z)
        glEnd()
        
        if not self.esperando_reset:
            for i in range(0,len(self.meteoros)):
                if(self.meteoros[i] == 1):
                    self.desenharAsteroide(i)
        
        glPushMatrix()
        glTranslatef(self.nave_x, self.nave_y, 0.0)
        self.desenharNave()
        glPopMatrix()

        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glPopMatrix()

    def desenhar_cenario(self):
        self.desenhar_hud_nave()
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()
        glPushMatrix()
        glRotate(self.cam_pitch, 1,0,0) 
        glRotate(self.cam_yaw, 0,1,0)
        self.desenhar_ceu() 
        glPopMatrix()
        self.aplicar_camera()
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.5, 1.5, 1.5, 1.0])
        glEnable(GL_LIGHTING); glEnable(GL_LIGHT0)
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0) 
        
        if self.texturas.get('sol.png'):
            glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, self.texturas['sol.png'])
            q = gluNewQuadric(); gluQuadricTexture(q, True); gluSphere(q, 3.8, 32, 32) 
            glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glPopMatrix()
        glPushMatrix()
        glPopMatrix()
        
        for i, p in enumerate(self.PLANETAS):
            glPushMatrix()
            glRotatef(self.angulos[i], 0.0, 1.0, 0.0)
            glTranslatef(p[2] * self.DIST_SCALE, 0.0, 0.0)
            glRotatef(self.rotacao_planetas[i], 0.0, 1.0, 0.0)
            if self.foco_camera == i: glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
            glColor3f(1.0, 1.0, 1.0) 
            if i == 5: # Saturno
                self.desenhar_esfera(self.texturas.get(p[0], 0), p[1] * self.RAIO_SCALE)
                glPushMatrix()
                glRotatef(80, 1,0,0); glDisable(GL_LIGHTING); glEnable(GL_TEXTURE_2D)
                glColor3f(1,1,1)
                if 'anelSaturno.png' in self.texturas: glBindTexture(GL_TEXTURE_2D, self.texturas['anelSaturno.png'])
                d = gluNewQuadric(); gluQuadricTexture(d, True); gluDisk(d, p[1]*self.RAIO_SCALE*1.2, p[1]*self.RAIO_SCALE*2.2, 64, 1) # 
                glDisable(GL_TEXTURE_2D); glEnable(GL_LIGHTING)
                glPopMatrix()
            elif i == 2: # Terra
                self.desenhar_esfera(self.texturas.get(p[0], 0), p[1] * self.RAIO_SCALE)
                glPushMatrix()
                glRotatef(self.angulo_lua, 0, 1, 0)
                glTranslatef((1+p[1])*self.RAIO_SCALE + 1.0, 0, 0)
                self.desenhar_esfera(self.texturas.get('lua.png',0), 0.27*self.RAIO_SCALE)
                glPopMatrix()
            else:
                self.desenhar_esfera(self.texturas.get(p[0], 0), p[1] * self.RAIO_SCALE)
            if self.foco_camera == i: glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
            glPopMatrix()
        glPopMatrix()
    
    def atualizar(self):
        vel = 0.01
        for i, p in enumerate(self.PLANETAS):
            self.angulos[i] = (self.angulos[i] + p[3] * self.velocidade_tempo) % 360.0
            self.rotacao_planetas[i] = (self.rotacao_planetas[i] + 1.2 * self.velocidade_tempo) % 360.0
        self.angulo_lua = (self.angulo_lua + 5.0 * self.velocidade_tempo) % 360.0
        
        if self.esperando_reset:
            self.timer_spawn += 1
            if self.timer_spawn > self.tempo_espera_max:
                self.esperando_reset = False
                self.timer_spawn = 0
                for j in range(len(self.meteorosObjetos)):
                    if j < 5: self.meteorosObjetos[j].posicao[0] = -4
                    else:     self.meteorosObjetos[j].posicao[0] = 4
                self.meteoros = regras.aleatorizar(self.meteoros, self.qntd)
            return 

        wave_out = True  # verifica se todos os meteoros saíram da tela
        for i in range(0, len(self.meteoros)):
            # trava de segurança para não crashar se as listas desincronizarem 
            if i >= len(self.meteorosObjetos): 
                continue

            if(self.meteoros[i] == 1):
                if(i < 5):
                    self.meteorosObjetos[i].posicao[0] += vel
                    if self.meteorosObjetos[i].posicao[0] < 1.8: wave_out = False
                else:
                    self.meteorosObjetos[i].posicao[0] -= vel
                    if self.meteorosObjetos[i].posicao[0] > -1.8: wave_out = False

                self.colisao = regras.checarColisaoNave(
                    self.meteorosObjetos[i], 
                    objeto(self.nave_x, self.nave_y, 0, 0.15, 0.15, 0.15, -0.15, -0.15, -0.15)
                )
                if self.colisao:
                    self.meteoroInicializado = False
                    break
        
        if wave_out and not self.colisao:
            self.esperando_reset = True
                
    def getColisao(self):
        return self.colisao
    
    def inverteColisao(self):
        self.colisao = False
        
    def quantidadeCometas(self, fase_str):
        fase = int(fase_str)
        self.qntd = min(fase + 1, 9)
        self.meteoros = regras.aleatorizar(self.meteoros, self.qntd)
        
    def input_nave(self, k):
        vel = 0.2; limit_x = 1.8; limit_y = 1.2
        if k == 'w' and self.nave_y < limit_y: self.nave_y += vel
        elif k == 's' and self.nave_y > -limit_y: self.nave_y -= vel
        elif k == 'a' and self.nave_x > -limit_x: self.nave_x -= vel; self.nave_roll = 25.0
        elif k == 'd' and self.nave_x < limit_x: self.nave_x += vel; self.nave_roll = -25.0
        
    def desenharAsteroide(self, i):
        val1 = 0.105
        val2 = 0.211
        val3 = 0.529
        val4 = 0.487
        val5 = 0.2648
        
        glPushMatrix()
        glTranslatef(self.meteorosObjetos[i].posicao[0], self.meteorosObjetos[i].posicao[1], self.meteorosObjetos[i].posicao[2])
        glScalef(0.6, 0.6, 0.6)
        
        glRotatef(90,0,0,1)
        if(i >= 5):
            glRotatef(180,0,0,1)

        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        if 'asteroid.jpg' in self.texturas:
             glBindTexture(GL_TEXTURE_2D, self.texturas['asteroid.jpg'])
        glColor3d(1,0.3,0)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, val5, 32, 32) 
        gluDeleteQuadric(quad)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        glTranslate(0.0,0.0,0)
        glRotate(-15,0,0,1)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1,1,0); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(1,0,0); glVertex3f(-val2,-val1, val1);  
        glColor3f(1,0,0); glVertex3f( val2,-val1, val2);   
        glColor3f(1,0,0); glVertex3f( val2,-val1,-val2);  
        glColor3f(1,0,0); glVertex3f(-val2,-val1,-val1);   
        glColor3f(1,0,0); glVertex3f(-val2,-val1,val1);   
        glEnd()
        glTranslate(-0.1,0,0)
        glRotatef(5,0,0,1)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1,0.6,0); glVertex3f( 0.0, val4, 0.0);   
        glColor3f(1,0,0); glVertex3f(-val1,-val1, val1);  
        glColor3f(1,0,0); glVertex3f( val1,-val1, val1);   
        glColor3f(1,0,0); glVertex3f( val1,-val1,-val1);  
        glColor3f(1,0,0); glVertex3f(-val1,-val1,-val1);   
        glColor3f(1,0,0); glVertex3f(-val1,-val1, val1);   
        glEnd()
        glTranslate(-0.05,0,0)
        glRotatef(5,0,0,1)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1,0.6,0); glVertex3f( 0.0, val2, 0.0);   
        glColor3f(1,0,0); glVertex3f(-val1,-val1, val1);  
        glColor3f(1,0,0); glVertex3f( val1,-val1, val1);   
        glColor3f(1,0,0); glVertex3f( val1,-val1,-val1);  
        glColor3f(1,0,0); glVertex3f(-val1,-val1,-val1);   
        glColor3f(1,0,0); glVertex3f(-val1,-val1, val1);   
        glEnd()
        glPopMatrix()

    def desenharNave(self):
        val1 = 0.0833
        val2 = 0.1666
        val3 = 0.0416
        val4 = 0.0333
        val5 = 0.0166
        val6 = 0.025
      
        glRotate(270,0,1,0)
        glBegin(GL_QUADS)
        glColor3f(0.5,0.5,0.5);glVertex3f( val1, val2, val1);  
        glColor3f(0.5,0.5,0.5);glVertex3f( val1,-val1, val1);   
        glColor3f(0.5,0.5,0.5);glVertex3f( val1,-val1,-val1);   
        glColor3f(0.5,0.5,0.5);glVertex3f( val1, val2,-val1);
        glColor3f(0.5,0.5,0.5);glVertex3f( val1, val2,-val1);   
        glColor3f(0.5,0.5,0.5);glVertex3f( val1,-val1,-val1);   
        glColor3f(0.5,0.5,0.5); glVertex3f(-val1,-val1,-val1);   
        glColor3f(0.5,0.5,0.5);glVertex3f(-val1, val2,-val1);   
        glVertex3f(-val1, val2,-val1);   
        glVertex3f(-val1,-val1,-val1);   
        glVertex3f(-val1,-val1, val1);  
        glVertex3f(-val1, val2, val1);   
        glVertex3f(-val1, val2, val1);   
        glVertex3f(-val1,-val1, val1);   
        glVertex3f( val1,-val1, val1);   
        glVertex3f( val1, val2, val1);   
        glVertex3f(-val1, val2,-val1);   
        glVertex3f(-val1, val2, val1);   
        glVertex3f( val1, val2, val1);   
        glVertex3f( val1, val2,-val1);  
        glVertex3f(-val1,-val1, val1)
        glVertex3f(-val1,-val1,-val1)
        glVertex3f( val1,-val1,-val1)
        glVertex3f( val1,-val1, val1)
        glEnd()
        glTranslatef(0,0.25,0)
        glBegin(GL_TRIANGLES)
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val1, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val1,-val1, val1);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val1,-val1, val1);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val1, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val1,-val1, val1);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val1,-val1,-val1);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val1, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val1,-val1,-val1);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val1,-val1,-val1);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val1, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val1,-val1,-val1);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val1,-val1, val1);   
        glEnd()
        glTranslatef(0.166,-0.166,0)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluQuadricNormals(quad, GLU_SMOOTH)
        glColor3f(0,0, 0.4)
        gluSphere(quad, val3, 10, 10)
        glTranslatef(-0.166,-0.166,0.05)
        glBegin(GL_TRIANGLES)
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val3,-val3, val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val3,-val3, val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val3,-val3, val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val3,-val3,-val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val3,-val3,-val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val3,-val3,-val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val3,-val3,-val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val3,-val3, val3);   
        glEnd();
        glTranslatef(0,0,-0.1)
        glBegin(GL_TRIANGLES)
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val3,-val3, val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val3,-val3, val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val3,-val3, val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val3,-val3,-val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f( val3,-val3,-val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val3,-val3,-val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f( 0.0, val3, 0.0);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val3,-val3,-val3);   
        glColor3f(0.3,0.3,0.3); glVertex3f(-val3,-val3, val3);   
        glEnd()
        glTranslatef(-0.1666,-0.0833, 0)
        glRotatef(180,0,0,1)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1,1,0); glVertex3f( 0.0, val4, 0.0);   
        glColor3f(1,0,0); glVertex3f(-val6,-val4, val5);  
        glColor3f(1,0,0); glVertex3f( val6,-val4, val5);   
        glColor3f(1,0,0); glVertex3f( val6,-val4,-val5);  
        glColor3f(1,0,0); glVertex3f(-val6,-val4,-val5);   
        glColor3f(1,0,0); glVertex3f(-val6,-val4, val5);   
        glEnd()
        glRotate(-180,0,0,1)
        glTranslatef(0,0,0.1)
        glRotate(180,0,0,1) 
        glBegin(GL_TRIANGLE_FAN);
        glColor3f(1,1,0); glVertex3f( 0.0, val4, 0.0);   
        glColor3f(1,0,0); glVertex3f(-val6,-val4, val5);  
        glColor3f(1,0,0); glVertex3f( val6,-val4, val5);   
        glColor3f(1,0,0); glVertex3f( val6,-val4,-val5);  
        glColor3f(1,0,0); glVertex3f(-val6,-val4,-val5);   
        glColor3f(1,0,0); glVertex3f(-val6,-val4, val5); 
        glEnd()
        glTranslate(-0,-0.2,-0.05)
        glRotate(-270,0,1,0)