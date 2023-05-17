class Light:
    def __init__(self, position, color, specular_intensity, shadow_intensity, width_radius):
        self.position = position
        self.color = color
        self.specular_intensity = specular_intensity
        self.shadow_intensity = shadow_intensity
        self.width_radius = width_radius

    # Get and set functions
    def getPosition(self):
        return self.position

    def getColor(self):
        return self.color

    def getSpecularIntensity(self):
        return self.specular_intensity

    def getShadowIntensity(self):
        return self.shadow_intensity

    def getWidthRadius(self):
        return self.width_radius

    def setPosition(self, position):
        self.position = position

    def setColor(self, color):
        self.color = color

    def setSpecularIntensity(self, specular_intensity):
        self.specular_intensity = specular_intensity

    def setShadowIntensity(self, shadow_intensity):
        self.shadow_intensity = shadow_intensity

    def setWidthRadius(self, width_radius):
        self.width_radius = width_radius
