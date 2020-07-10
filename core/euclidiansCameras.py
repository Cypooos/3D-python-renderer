from core.positions import EuclidianPosition
import math
import pygame

class FlyCamera():

  def __init__(self):
    self.transform = EuclidianPosition([0,0,0],[0,0])
    self.fov = 100
    self.parent = None
    self.movement_speed = 3
    self.sensitive = 30

  def onKey(self,key):
    s=self.scene.deltaTime*self.movement_speed
    if key[pygame.K_q]: self.transform.pos[1] -=s
    if key[pygame.K_e]: self.transform.pos[1] +=s

    x,y = s*math.sin(self.transform.rot[1]),s*math.cos(self.transform.rot[1])

    if key[pygame.K_w]: self.transform.pos[0] +=x;self.transform.pos[2] +=y;
    if key[pygame.K_s]: self.transform.pos[0] -=x;self.transform.pos[2] -=y;
    if key[pygame.K_a]: self.transform.pos[0] -=y;self.transform.pos[2] +=x;
    if key[pygame.K_d]: self.transform.pos[0] +=y;self.transform.pos[2] -=x;

  def onMouseMove(self,move):
    x,y = move
    x/=self.sensitive; y/=self.sensitive
    self.transform.rot[0]+=y;self.transform.rot[1]+=x
    if self.transform.rot[0] > math.pi:self.transform.rot[0] = math.pi
    if self.transform.rot[0] < -math.pi:self.transform.rot[0] = -math.pi