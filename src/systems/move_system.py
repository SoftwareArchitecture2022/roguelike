from system import System
from llist import dllist
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from components.intention_component import *
from components.real_component import *

class MoveSystem(System):
    def __init__(self, entityFactory, entityStorage, eventExchanger, worldWidth, worldHeight):
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight
        super(MoveSystem, self).__init__(entityFactory, entityStorage, eventExchanger)
        self.components = dllist()


    def update(self):
        events = self.eventExchanger.pullEvents()
        for i in range(len(events)):
            pass

        for node in self.components.iternodes():
            if False: # TODO delete deleted component
                self.components.remove(node)
            self.doMove(node.value)
        
    def doMove(self, intentionComponent):
        realComponent = self.entityStorage.getEntityComponent(intentionComponent.entityId, RealComponent)
        if realComponent.y < self.worldHeight - 1 and ACTION_UP in intentionComponent.actions:
            realComponent.y += 1
        if realComponent.y > 0 and ACTION_DOWN in intentionComponent.actions:
            realComponent.y -= 1
        if realComponent.x < self.worldWidth - 1 and ACTION_RIGHT in intentionComponent.actions:
            realComponent.x += 1
        if realComponent.x > 0 and ACTION_LEFT in intentionComponent.actions:
            realComponent.x -= 1
