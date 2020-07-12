from core.eclDef import elcMesh, Transform, setMeshByPoints
class Cube():

  def __init__(self,transform,parent = None):
    if isinstance(transform,Transform):self.transform = transform
    else: self.transform = Transform(transform,[0,0,0])
    self.parent = parent
    self.mesh = elcMesh( [
      [ [0,0,0], [0,1,0], [1,1,0]],
      [ [0,0,0], [1,1,0], [1,0,0]],
      [ [1,0,0], [1,1,0], [1,1,1]],
      [ [1,0,0], [1,1,1], [1,0,1]],
      [ [1,0,1], [1,1,1], [0,1,1]],
      [ [1,0,1], [0,1,1], [0,0,1]],
      [ [0,0,1], [0,1,1], [0,1,0]],
      [ [0,0,1], [0,1,0], [0,0,0]],
      [ [0,1,0], [0,1,1], [1,1,1]],
      [ [0,1,0], [1,1,1], [1,1,0]],
      [ [1,0,1], [0,0,1], [0,0,0]],
      [ [1,0,1], [0,0,0], [1,0,0]],
    ])
    """
    self.mesh = elcMesh(setMeshByPoints(
      [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)],
      [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)]
    ))"""