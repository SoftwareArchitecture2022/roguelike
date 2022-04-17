import itertools


class Entity:
    id_iter = itertools.count()

    def __init__(self):
        self.id = next(Entity.id_iter)
