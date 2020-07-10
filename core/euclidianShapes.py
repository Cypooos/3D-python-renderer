from core.positions import EuclidianPosition

class Cube():

  def __init__(self,pos,parent = None):
    self.transform = EuclidianPosition(pos,[0,0])
    self.parent = parent
    self.verts = [(-1,-1,-1),(1.5,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
    self.faces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)]
    self.colors = [(255,0,0),(255,128,0),(255,255,0),(255,255,255),(0,0,255),(0,255,0)]