from core.positions import EuclidianPosition
import math
import pygame

class FlyCamera():

  def __init__(self):
    self.position = EuclidianPosition([0,0,0],[0,0])
    self.fov = 100
    self.parent = None
    self.movement_speed = 3
    self.sensitive = 30

  def onKey(self,key):
    s=self.scene.deltaTime*self.movement_speed
    if key[pygame.K_q]: self.position.pos[1] -=s
    if key[pygame.K_e]: self.position.pos[1] +=s

    x,y = s*math.sin(self.position.rot[1]),s*math.cos(self.position.rot[1])

    if key[pygame.K_w]: self.position.pos[0] +=x;self.position.pos[2] +=y;
    if key[pygame.K_s]: self.position.pos[0] -=x;self.position.pos[2] -=y;
    if key[pygame.K_a]: self.position.pos[0] -=y;self.position.pos[2] +=x;
    if key[pygame.K_d]: self.position.pos[0] +=y;self.position.pos[2] -=x;

  def onMouseMove(self,move):
    x,y = move
    x/=self.sensitive; y/=self.sensitive
    self.position.rot[0]+=y;self.position.rot[1]+=x
    if self.position.rot[0] > math.pi:self.position.rot[0] = math.pi
    if self.position.rot[0] < -math.pi:self.position.rot[0] = -math.pi