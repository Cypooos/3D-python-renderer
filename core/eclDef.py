class eclVector3():
  def __init__(self,x,y,z):
    self.x,self.y,self.z = x,y,z
  def __setitem__(self, numb, data):
    if numb == 0: self.x = data
    elif numb == 1: self.y = data
    elif numb == 2: self.z = data
  def __getitem__(self, numb):
    if numb == 0: return self.x
    elif numb == 1: return self.y
    elif numb == 2: return self.z

class Transform():
  def __init__(self,position,rotation):
    if isinstance(position, eclVector3): self.position = position
    else:self.position = eclVector3(position[0],position[1],position[2])
    if isinstance(rotation, eclVector3): self.rotation = rotation
    else:self.rotation = eclVector3(rotation[0],rotation[1],rotation[2])

  def __add__(a,b):
    return Transform(
      eclVector3(a.position.x + b.position.x,a.position.y + b.position.y,a.position.z + b.position.z),
      eclVector3(a.rotation.x + b.rotation.x,a.rotation.y + b.rotation.y,a.rotation.z + b.rotation.z))


class elcTriangle():
  def __init__(self,ptA=eclVector3(0,0,0),ptB=eclVector3(0,0,0),ptC=eclVector3(0,0,0)):
    self.points = [ptA,ptB,ptC]
  def calculateNormal(self):
    return NotImplemented
  def __setitem__(self, numb, data):
    self.points[numb] = data
  def __getitem__(self, numb):
    return self.points[numb]

class elcMesh():
  def __init__(self,triList,isDoubleSided=False):
    self.tri = [elcTriangle(eclVector3(*x[0]),eclVector3(*x[1]),eclVector3(*x[2])) for x in triList]
    self.isDoubleSided = isDoubleSided
  def __setitem__(self, numb, data):
    self.tri[numb] = data
  def __getitem__(self, numb):
    return self.tri[numb]

def setMeshByPoints(points,triangles):
  end = []
  for x in triangles:
    for count in range(1,len(x)-1):
      end.append([
        points[x[0]],
        points[x[count]],
        points[x[count+1]]])
  print(end)
  return end


def XbyXmatrix(size,init_number=0):
  return [[init_number for _ in range(size)] for _ in range(size)]

def multiplyMatrixVector3(elcVector3,matrix,out=None):
  if out == None:o = eclVector3(0,0,0)
  else: o = out
  o.x = elcVector3.x * matrix[0][0] + elcVector3.y * matrix[1][0] + elcVector3.z * matrix[2][0] + matrix[3][0]
  o.y = elcVector3.x * matrix[0][1] + elcVector3.y * matrix[1][1] + elcVector3.z * matrix[2][1] + matrix[3][1]
  o.z = elcVector3.x * matrix[0][2] + elcVector3.y * matrix[1][2] + elcVector3.z * matrix[2][2] + matrix[3][2]
  
  w = elcVector3.x * matrix[0][3] + elcVector3.y * matrix[1][3] + elcVector3.z * matrix[2][3] + matrix[3][3]
  if w != 0.0:o.x /= w; o.y /= w; o.z /= w;
  return o

if __name__ == "__main__":
  setMeshByPoints(
    [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)],
    [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)])