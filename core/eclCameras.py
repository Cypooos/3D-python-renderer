from core.eclDef import eclVector3, Transform
import math
import pygame

class FlyAbsoluteCamera():

  def __init__(self):
    self.transform = Transform([0,0,0],[0,0,0])
    self.fov = 100
    self.movement_speed = 3
    self.sensitive = 30

  def onKey(self,key):
    s=self.scene.deltaTime*self.movement_speed
    if key[pygame.K_q]: self.transform.position.y -=s
    if key[pygame.K_e]: self.transform.position.y +=s
    if key[pygame.K_w]: self.transform.position.x +=s
    if key[pygame.K_s]: self.transform.position.x -=s
    if key[pygame.K_a]: self.transform.position.z +=s
    if key[pygame.K_d]: self.transform.position.z -=s
    """
    x,z = s*math.sin(self.transform.rotation.x),s*math.cos(self.transform.rotation.z)

    if key[pygame.K_w]: self.transform.position.x +=x;self.transform.position.z +=z
    if key[pygame.K_s]: self.transform.position.x -=x;self.transform.position.z -=z
    if key[pygame.K_a]: self.transform.position.x -=z;self.transform.position.z +=x
    if key[pygame.K_d]: self.transform.position.x +=z;self.transform.position.z -=x"""


  def onMouseMove(self,move):
    x,z = move
    x/=self.sensitive; z/=self.sensitive
    self.transform.rotation.z-=z;self.transform.rotation.x+=x
    if self.transform.rotation.z > math.pi/4:self.transform.rotation.z = math.pi/4
    if self.transform.rotation.z < -math.pi/4:self.transform.rotation.z = -math.pi/4