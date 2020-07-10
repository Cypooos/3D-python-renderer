

class EuclidianPosition():

  def __init__(self,pos,rot):
    self.pos = pos
    self.rot = rot

  def __add__(self,other):# TO DO: Proper Relative to rotation add
    return EuclidianPosition([self.pos[x]+other.pos[x] for x in range(3)],[self.rot[x]+other.rot[x] for x in range(2)])

  def __sub__(self,other): # TO DO: Relative to rotation sub
    return EuclidianPosition([self.pos[x]-other.pos[x] for x in range(3)],[self.rot[x]-other.rot[x] for x in range(2)])