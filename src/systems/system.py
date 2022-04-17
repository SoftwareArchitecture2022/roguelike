
class System:
    def __init__(self, entity_factory, entity_storage, event_exchanger):
        self.entity_factory = entity_factory
        self.entity_storage = entity_storage
        self.event_exchanger = event_exchanger
