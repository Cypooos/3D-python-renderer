from core.eclRenderer import MatrixEuclidianRenderer, OldEuclidianRenderer, EuclidianRenderer
from core.scene import Scene

from core.eclShapes import elcCube, elcEmpty
from core.eclDef import Transform

from core.eclCameras import FlyAbsoluteCamera

import pygame 
import math

screen = pygame.display.set_mode([800,800])

pygame.event.get(); pygame.mouse.get_rel()
pygame.mouse.set_visible(0); pygame.event.set_grab(1)


sc = Scene()



cam = FlyAbsoluteCamera(); sc.addObject(cam)
light = elcEmpty(Transform([0,-0.5,-0.8],[0,0,0])); sc.addObject(light,["Light"])
sc.addObject(EuclidianRenderer('EUCLID',cam,lightTag="Light"))

def update_light(time):
    light.transform.position.x = math.sin(time)
    light.transform.position.y = math.cos(time)/2
    light.transform.position.z = math.cos(time)/2

light.onRender = update_light

sc.addObject(elcCube((0,0,0)),["EUCLID"])
sc.addObject(elcCube((0,0,1)),["EUCLID"])
sc.addObject(elcCube((0,0,-1)),["EUCLID"])
sc.addObject(elcCube(Transform([0,2,0],[0,0,0])),["EUCLID"])

sc.load(screen)
sc.loop()