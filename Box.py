class Box:
    def __init__(self, position, scale, material):
        self.position = position
        self.scale = scale
        self.material = material

    # Get and set functions
    def getPosition(self):
        return self.position

    def getScale(self):
        return self.scale

    def getMaterial(self):
        return self.material

    def setPosition(self, position):
        self.position = position

    def setScale(self, scale):
        self.scale = scale

    def setMaterial(self, material):
        self.material = material