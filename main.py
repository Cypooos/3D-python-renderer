from core.eclRenderer import EuclidianRenderer, OldEuclidianRenderer
from core.scene import Scene

from core.eclShapes import Cube

import asyncio
import pygame 

from core.eclCameras import FlyCamera

screen = pygame.display.set_mode([800,800])

pygame.event.get(); pygame.mouse.get_rel()
pygame.mouse.set_visible(0); pygame.event.set_grab(1)

sc = Scene()


cam = FlyCamera()
sc.addObject(cam)
renderer = EuclidianRenderer('EUCLID',cam)
sc.addObject(renderer)

cu = Cube((0,0,0))
sc.addObject(cu,["EUCLID"])
cu2 = Cube((3,0,0))
sc.addObject(cu2,["EUCLID"])

loop = asyncio.get_event_loop()
loop.run_until_complete(sc.load(screen))
loop.run_until_complete(sc.loop())
loop.close()