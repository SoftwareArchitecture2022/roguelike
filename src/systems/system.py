
class System:
    def __init__(self, entityFactory, entityStorage, eventExchanger):
        self.entityFactory = entityFactory
        self.entityStorage = entityStorage
        self.eventExchanger = eventExchanger
