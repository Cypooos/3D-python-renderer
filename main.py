from core.eclRenderer import MatrixEuclidianRenderer, OldEuclidianRenderer, EuclidianRenderer
from core.scene import Scene

from core.eclShapes import elcCube, elcEmpty
from core.eclDef import Transform

import pygame 

from core.eclCameras import FlyAbsoluteCamera

screen = pygame.display.set_mode([800,800])

pygame.event.get(); pygame.mouse.get_rel()
pygame.mouse.set_visible(0); pygame.event.set_grab(1)


sc = Scene()


cam = FlyAbsoluteCamera(); sc.addObject(cam)
sc.addObject(EuclidianRenderer('EUCLID',cam,lightTag="Light"))

sc.addObject(elcEmpty(Transform([0,-0.5,-0.8],[0,0,0])),['Light'])

sc.addObject(elcCube((0,0,0)),["EUCLID"])
sc.addObject(elcCube((0,0,1)),["EUCLID"])
sc.addObject(elcCube((0,0,-1)),["EUCLID"])
sc.addObject(elcCube(Transform([0,2,0],[0,0,0])),["EUCLID"])

sc.load(screen)
sc.loop()