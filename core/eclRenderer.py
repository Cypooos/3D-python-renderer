import math
import asyncio
import pygame

from core.eclDef import eclVector3, Transform, elcTriangle
from core.eclDef import XbyXmatrix, multiplyMatrixVector3
from core.eclDef import crossProduct, dotProduct, normalise

class OldEuclidianRenderer():

  def __init__(self,tagToRender,camera):
    self.scene = None
    self.tagToRender = tagToRender
    self.transform = camera.transform

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

class MatrixEuclidianRenderer():

  def __init__(self,tagToRender,camera,**kwargs):
    self.scene = None
    self.tagToRender = tagToRender
    self.transform = camera.transform
    self.projectionMatrix = XbyXmatrix(4,0)
    self.conf = kwargs

  def onAwake(self):
    self.screen = self.scene.screen
    self.w, self.h = self.screen.get_size()
    self.cx, self.cy = self.w //2,self.h //2
    near = self.conf.get("near",0.1)
    far = self.conf.get("far",1000)
    fov = self.conf.get("fov",90)
    fovRad = 1/math.tan((fov/2) / (180 * math.pi))

    self.projectionMatrix[0][0] = (self.h/self.w) * fovRad
    self.projectionMatrix[1][1] = fovRad
    self.projectionMatrix[2][2] = far / (far - near)
    self.projectionMatrix[3][2] = (-far * near) / (far - near)
    self.projectionMatrix[2][3] = 1
    self.projectionMatrix[3][3] = 0
    self.theta = 0


  def onRender(self):

    self.screen.fill((0,0,0))

    matRotZ = XbyXmatrix(4,0)
    matRotX = XbyXmatrix(4,0)
    self.theta += self.scene.deltaTime

    matRotZ[0][0] = math.cos(self.theta)
    matRotZ[0][1] = math.sin(self.theta)
    matRotZ[1][0] = -math.sin(self.theta)
    matRotZ[1][1] = math.cos(self.theta)
    matRotZ[2][2] = 1
    matRotZ[3][3] = 1

    matRotX[0][0] = 1
    matRotX[1][1] = math.cos(self.theta * 0.5)
    matRotX[1][2] = math.sin(self.theta * 0.5)
    matRotX[2][1] = -math.sin(self.theta * 0.5)
    matRotX[2][2] = math.cos(self.theta * 0.5)
    matRotX[3][3] = 1

    objs = self.scene.getByTag(self.tagToRender)
    for x in objs:
      for tri_ in x.mesh.tri:
        
        triProjected = elcTriangle()
        triTranslated = elcTriangle()
        triRotatedZ = elcTriangle()
        triRotatedZX = elcTriangle()
        tri = elcTriangle()

        tri[0] = tri_[0] + self.scene.getAbsolutePos(x).position
        tri[1] = tri_[1] + self.scene.getAbsolutePos(x).position
        tri[2] = tri_[2] + self.scene.getAbsolutePos(x).position
        print(tri[0][0], tri_[0][0], self.scene.getAbsolutePos(x).position[0])

        # Rotate in Z-Axis
        multiplyMatrixVector3(tri[0], matRotZ, triRotatedZ[0])
        multiplyMatrixVector3(tri[1], matRotZ, triRotatedZ[1])
        multiplyMatrixVector3(tri[2], matRotZ, triRotatedZ[2])

        # Rotate in X-Axis
        multiplyMatrixVector3(triRotatedZ[0], matRotX, triRotatedZX[0])
        multiplyMatrixVector3(triRotatedZ[1], matRotX, triRotatedZX[1])
        multiplyMatrixVector3(triRotatedZ[2], matRotX, triRotatedZX[2])

        # Offset into the screen
        triTranslated = triRotatedZX
        triTranslated[0].z = triRotatedZX[0].z + 3
        triTranslated[1].z = triRotatedZX[1].z + 3
        triTranslated[2].z = triRotatedZX[2].z + 3

        # Project triangles from 3D --> 2D
        multiplyMatrixVector3(triTranslated[0], self.projectionMatrix, triProjected[0])
        multiplyMatrixVector3(triTranslated[1], self.projectionMatrix, triProjected[1])
        multiplyMatrixVector3(triTranslated[2], self.projectionMatrix, triProjected[2])

        # Scale into view
        triProjected[0].x += 1; triProjected[0].y += 1
        triProjected[1].x += 1; triProjected[1].y += 1
        triProjected[2].x += 1; triProjected[2].y += 1
        triProjected[0].x *= 0.5 * self.w
        triProjected[0].y *= 0.5 * self.h
        triProjected[1].x *= 0.5 * self.w
        triProjected[1].y *= 0.5 * self.h
        triProjected[2].x *= 0.5 * self.w
        triProjected[2].y *= 0.5 * self.h

        # Draw triangle
        pygame.draw.polygon(self.screen, (100,10,255), [(triProjected[0].x, triProjected[0].y),(triProjected[1].x, triProjected[1].y),(triProjected[2].x, triProjected[2].y),(triProjected[0].x, triProjected[0].y)], 3)




class EuclidianRenderer():

  def __init__(self,tagToRender,camera,**kwargs):
    self.scene = None
    self.tagToRender = tagToRender
    self.transform = camera.transform
    self.conf = kwargs

  def onAwake(self):
    self.screen = self.scene.screen
    self.w, self.h = self.screen.get_size()
    self.cx, self.cy = self.w //2,self.h //2
    self.near = self.conf.get("near",0.1)
    self.far = self.conf.get("far",1000)
    self.fov = self.conf.get("fov",90)
    self.far_length = math.tan(self.fov/2)*self.far
    self.lights = self.scene.getByTag(self.conf.get("lightTag",""))
    if len(self.lights) == 0:self.light = Transform([0,0,0],[0,45,0]);self.lights = [self.light]
    else:self.light = self.lights[0]

  @staticmethod
  def rotate2d(pos,rad): x,y = pos;  s,c = math.sin(rad),math.cos(rad); return x*c-y*s,y*c+x*s # wtf 

  def _projection(self,vect3:eclVector3):
    try:
      X = vect3.x/((vect3.z*self.far_length)/self.far)
      Y = vect3.y/((vect3.z*self.far_length)/self.far)
      Z = (vect3.z-self.near)/(self.far-self.near)
      return eclVector3(X,Y,Z) # -1_1 -1_1 0_1
    except ZeroDivisionError:
      return eclVector3(0,0,0)

  def draw(self,triangle:elcTriangle,color=None):
    try:
      if color == None:
        pygame.draw.polygon(self.screen, (100,10,255),
          [ (triangle[0].x, triangle[0].y),
            (triangle[1].x, triangle[1].y),
            (triangle[2].x, triangle[2].y),
            (triangle[0].x, triangle[0].y)
          ], 2)
      else:
        pygame.draw.polygon(self.screen, color,
          [ (triangle[0].x, triangle[0].y),
            (triangle[1].x, triangle[1].y),
            (triangle[2].x, triangle[2].y),
            (triangle[0].x, triangle[0].y)
          ])
    except TypeError:
      pass

  def onRender(self,*arg,**kwargs):

    self.screen.fill((0,0,0))
    absPosSelf = self.transform.position
    absRotSelf = self.transform.rotation

    objs = self.scene.getByTag(self.tagToRender)

    tris_sorted = []

    for obj in objs:
      absPosObj = obj.transform.position
      absRotObj = obj.transform.rotation
      for tri_ in obj.mesh.tri:
        
        triProj = elcTriangle()
        triRoted = elcTriangle()
        triPosed = elcTriangle()
        for x in range(3):
          triPosed[x] = tri_[x]+absPosObj+absPosSelf
          posTemp = eclVector3(triPosed[x].x,triPosed[x].y,triPosed[x].z) # copy
          posTemp.x, posTemp.z = self.rotate2d((posTemp.x,posTemp.z),absRotObj.x+absRotSelf.x)
          posTemp.y, posTemp.x = self.rotate2d((posTemp.y,posTemp.x),absRotObj.y+absRotSelf.y)
          posTemp.z, posTemp.y = self.rotate2d((posTemp.z,posTemp.y),absRotObj.z+absRotSelf.z)
          triRoted[x] = posTemp
        
        for x in range(3):
          #posTemp.z, posTemp.x = self.rotate2d((posTemp.z,posTemp.x),absRotObj.y+absRotSelf.y)
          triProj[x] = self._projection(triRoted[x])

        shouldDraw = False
        normal_proj = triProj.calculateNormal()
        normal_posed = triPosed.calculateNormal()
        normal_roted = triRoted.calculateNormal()
        if (dotProduct(normal_proj,triProj[0] - self.transform.position) > 0):shouldDraw = True
        shouldDraw = True
        
        def rescale(x,min_,max_):return (x/2+0.5)*(max_+min_)

        if shouldDraw:
          color = rescale(dotProduct(normal_posed,self.light.transform.position),0,255)
          print(color)
          white = int(color)
          tris_sorted.append([triProj,[white,white,white],sum(sum(abs(triPosed[j][i]) for j in range(3)) for i in range(3))])
    
    tris_sorted = sorted(tris_sorted,key=lambda x:x[2],reverse=True)
    for tri,color,_ in tris_sorted:
      self.draw(elcTriangle(
        eclVector3(rescale(tri[0].x,0,self.w),rescale(tri[0].y,0,self.h),0),
        eclVector3(rescale(tri[1].x,0,self.w),rescale(tri[1].y,0,self.h),0),
        eclVector3(rescale(tri[2].x,0,self.w),rescale(tri[2].y,0,self.h),0)
      ),color)
      """self.draw(elcTriangle(
        eclVector3(rescale(tri[0].x,0,self.w),rescale(tri[0].y,0,self.h),0),
        eclVector3(rescale(tri[1].x,0,self.w),rescale(tri[1].y,0,self.h),0),
        eclVector3(rescale(tri[2].x,0,self.w),rescale(tri[2].y,0,self.h),0)
      ))"""
