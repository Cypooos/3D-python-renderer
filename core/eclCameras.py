from core.eclDef import eclVector3, Transform
import math
import pygame

class FlyCamera():

  def __init__(self):
    self.transform = Transform([0,0,0],[0,0,0])
    self.fov = 100
    self.parent = None
    self.movement_speed = 3
    self.sensitive = 30

  def onKey(self,key):
    s=self.scene.deltaTime*self.movement_speed
    if key[pygame.K_q]: self.transform.position.y -=s
    if key[pygame.K_e]: self.transform.position.y +=s

    x,y = s*math.sin(self.transform.rotation.y),s*math.cos(self.transform.rotation.y)

    if key[pygame.K_w]: self.transform.position.x +=x;self.transform.position.z +=y;
    if key[pygame.K_s]: self.transform.position.x  -=x;self.transform.position.z -=y;
    if key[pygame.K_a]: self.transform.position.x  -=y;self.transform.position.z +=x;
    if key[pygame.K_d]: self.transform.position.x  +=y;self.transform.position.z -=x;

  def onMouseMove(self,move):
    x,y = move
    x/=self.sensitive; y/=self.sensitive
    self.transform.rotation.x+=y;self.transform.rotation.y+=x
    if self.transform.rotation.x > math.pi:self.transform.rotation.x = math.pi
    if self.transform.rotation.x < -math.pi:self.transform.rotation.x = -math.pi