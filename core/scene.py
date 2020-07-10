import pygame
import asyncio
import random

class Scene():

  def __init__(self):
    self._objs = {}
    self.working = False
  
  def addObject(self,obj,tags=None):
    if tags != None: obj.tags = tags
    name = "obj-"+str(obj.__class__.__name__)+"-"+str(random.randint(1000,9999))
    val = 0
    while name+str(val) in self._objs.values():val += 1
    self._objs[name+str(val)] = obj
    obj.scene = self
    obj.id_ = name+str(val)
    return name+str(val)

  def getByTag(self,tag):
    return [x for x in self._objs.values() if getattr(x, 'tags', None)!=None and tag in x.tags]
  def getByID(self,id_):
    if id_ in self._objs.keys():return self._objs[id_]
    return None

  def getAbsolutePos(self,obj):
    if obj.parent == None: return obj.transform
    Ppos = self.getAbsolutePos(obj.parent)
    return Ppos+obj.transform

  def call(self,methodName,*arg,**kwargs):
    for x in self._objs.values():
      meth = getattr(x, methodName, None)
      if callable(meth):meth(*arg,**kwargs)
  
  async def load(self,screen):
    self.deltaTime = 0.0
    self.clock = None
    self.screen = screen
    self.call("onAwake")
    print("Objets :"+str("\n".join([x+str(': ')+str(y) for x,y in self._objs.items()])))

  async def loop(self):
    pygame.init()
    clock = pygame.time.Clock()
    self.working = True
    self.call("onStart")
    while self.working:
      self.deltaTime = clock.tick()/1000
      key = pygame.key.get_pressed()
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          self.call("onQuit");self.working = False
        if event.type == pygame.MOUSEMOTION:
          self.call("onMouseMove",event.rel)
      if key[pygame.K_ESCAPE]:
        self.call("onQuit");self.working = False
      self.call("onKey",key)
      
      
      self.call("onRender")
      self.call("onPostProcessing")
      pygame.display.flip()


