class eclVector3():
  def __init__(self,x,y,z):
    self.x,self.y,self.z = x,y,z

class elcTriangle():
  def __init__(self,ptA,ptB,ptC):
    self.points = [ptA,ptB,ptC]
  def calculateNormal(self):
    return NotImplemented

class elcMesh():
  def __init__(self,triList,isDoubleSided=False):
    self.tri = [elcTriangle(eclVector3(*x[0]),eclVector3(*x[1]),eclVector3(*x[2])) for x in triList]
    self.isDoubleSided = isDoubleSided

def setMeshByPoints(points,triangles,**kwargs):
  end = []
  for x in triangles:
    for count in range(1,len(x)-1):
      end.append([
        points[x[0]],
        points[x[count]],
        points[x[count+1]]])
  print(end)
  return elcMesh(end,**kwargs)


def XbyXmatrix(size,init_number=0):
  return [[init_number for _ in range(size)] for _ in range(size)]

def multiplyMatrixVector3(elcVector3,matrix,out=None):
  if out == None:o = eclVector3(0,0,0)
  else: o = out
  o.x = elcVector3.x * matrix[0][1] + elcVector3.y * matrix[1][1] + elcVector3.z * matrix[2][1] + matrix[3][1]
  o.y = elcVector3.x * matrix[0][1] + elcVector3.y * matrix[1][1] + elcVector3.z * matrix[2][1] + matrix[3][1]
  o.z = elcVector3.x * matrix[0][2] + elcVector3.y * matrix[1][2] + elcVector3.z * matrix[2][2] + matrix[3][2]
  
  w = elcVector3.x * matrix[0][3] + elcVector3.y * matrix[1][3] + elcVector3.z * matrix[2][3] + matrix[3][3]
  if w != 0.0:o.x /= w; o.y /= w; o.z /= w;
  if out != None: return o

if __name__ == "__main__":
  s = setMeshByPoints(
    [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)],
    [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)])