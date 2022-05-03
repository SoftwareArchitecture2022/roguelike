import itertools


class Entity:
    id_iter = itertools.count()

    def __init__(self):
        """
        sets a unique entity id
        """
        self.id = next(Entity.id_iter)
