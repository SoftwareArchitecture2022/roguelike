from src.components.component import Component


class DrawableComponent(Component):

    def __init__(self, entity_id, assets_path):
        super().__init__(entity_id)
        self.assets_path = assets_path
        self.image = None

    def get_image(self, size):
        if self.image is None or len(self.image) != size:
            with open(self.assets_path + str(size)) as file:
                self.image = file.readlines()
        return self.image
