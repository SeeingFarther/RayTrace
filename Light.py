class Light:
    def __init__(self, position, color, specular_intensity, shadow_intensity, radius):
        self.position = position
        self.color = color
        self.specular_intensity = specular_intensity
        self.shadow_intensity = shadow_intensity
        self.radius = radius

    # Get and set functions
    def getPosition(self):
        return self.position

    def getColor(self):
        return self.color

    def getSpecularIntensity(self):
        return self.specular_intensity

    def getShadowIntensity(self):
        return self.shadow_intensity

    def getRadius(self):
        return self.radius

    def setPosition(self, position):
        self.position = position

    def setColor(self, color):
        self.color = color

    def setSpecularIntensity(self, specular_intensity):
        self.specular_intensity = specular_intensity

    def setShadowIntensity(self, shadow_intensity):
        self.shadow_intensity = shadow_intensity

    def setRadius(self, radius):
        self.radius = radius