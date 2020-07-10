import math
import asyncio
import pygame

from core.positions import EuclidianPosition

class OldEuclidianRenderer():

  def __init__(self,tagToRender,camera):
    self.scene = None
    self.tagToRender = tagToRender
    self.parent = camera
    self.transform = EuclidianPosition([0,0,0],[0,0])

  @staticmethod # nerd shit
  def rotate2d(pos,rad): x,y = pos;  s,c = math.sin(rad),math.cos(rad); return x*c-y*s,y*c+x*s

  def _calculatePoints(self,obj):
    # cam.fov cam.rot cam.pos cam
    for x,y,z in obj.verts:
      transform = self.scene.getAbsolutePos(self)
      x -= transform.pos[0];y -=transform.pos[1];z -=transform.pos[2]
      x,z = self.rotate2d((x,z),transform.rot[1]);y,z = self.rotate2d((y,z),transform.rot[0])
      self.calc_vertList += [(x,y,z)]
      f=self.parent.fov/z
      x,y = x*f,y*f
      self.calc_screenCoords.append((self.cx+int(x),self.cy+int(y)))
      pygame.draw.circle(self.screen,(0,0,0),(self.cx+int(x),self.cy+int(y)),5)

  def _calculateFaces(self,obj):
    for f in range(len(obj.faces)):
      face = obj.faces[f]
      on_screen = False
      for i in face:
        if self.calc_vertList[i][2]>0:
          on_screen=True; break
      if on_screen:
        coords = [self.calc_screenCoords[i] for i in face]
        self.calc_facesList += [coords]
        self.calc_facesColor += [obj.colors[f]]
        self.calc_depth += [sum(sum(self.calc_vertList[j][i] for j in face)**2 for i in range(3))]

  def onAwake(self):
    self.screen = self.scene.screen
    self.w, self.h = self.screen.get_size()
    self.cx, self.cy = self.w //2,self.h //2
  
  def onRender(self):

    self.screen.fill((100,10,255))

    self.calc_vertList = []
    self.calc_screenCoords = []
    self.calc_facesList = [];self.calc_facesColor = [];self.calc_depth = []

    for obj in self.scene.getByTag(self.tagToRender):
      self._calculatePoints(obj)
      self._calculateFaces(obj)

    faces_drawOrder = sorted(range(len(self.calc_facesList)),key = lambda i:self.calc_depth[i],reverse=True)

    for i in faces_drawOrder:pygame.draw.polygon(self.screen,self.calc_facesColor[i],self.calc_facesList[i])

class EuclidianRenderer():

  def __init__(self,tagToRender,camera):
    self.scene = None
    self.tagToRender = tagToRender
    self.parent = camera
    self.transform = EuclidianPosition([0,0,0],[0,0])