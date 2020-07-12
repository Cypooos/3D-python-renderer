from core.eclRenderer import MatrixEuclidianRenderer, OldEuclidianRenderer, EuclidianRenderer
from core.scene import Scene

from core.eclShapes import Cube
from core.eclDef import Transform

import asyncio
import pygame 

from core.eclCameras import FlyAbsoluteCamera

screen = pygame.display.set_mode([800,800])

pygame.event.get(); pygame.mouse.get_rel()
pygame.mouse.set_visible(0); pygame.event.set_grab(1)

sc = Scene()


cam = FlyAbsoluteCamera()
sc.addObject(cam)
renderer = EuclidianRenderer('EUCLID',cam)
sc.addObject(renderer)

sc.addObject(Cube((0,0,0)),["EUCLID"])
sc.addObject(Cube((0,0,1)),["EUCLID"])
sc.addObject(Cube((0,0,-1)),["EUCLID"])
sc.addObject(Cube(Transform([0,2,0],[0,0,0])),["EUCLID"])

loop = asyncio.get_event_loop()
loop.run_until_complete(sc.load(screen))
loop.run_until_complete(sc.loop())
loop.close()