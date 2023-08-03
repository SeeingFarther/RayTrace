class Material:
    def __init__(self, diffuse_color, specular_color, reflection_color, shininess, transparency):
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.reflection_color = reflection_color
        self.shininess = shininess
        self.transparency = transparency

    # Get and set functions
    def getDiffuseColor(self):
        return self.diffuse_color

    def getSpecularColor(self):
        return self.specular_color

    def getReflectionColor(self):
        return self.reflection_color

    def getShininess(self):
        return self.shininess

    def getTransparency(self):
        return self.transparency

    def setDiffuseColor(self, diffuse_color):
        self.diffuse_color = diffuse_color

    def setSpecularColor(self, specular_color):
        self.specular_color = specular_color

    def setReflectionColor(self, reflection_color):
        self.reflection_color = reflection_color

    def setShininess(self, shininess):
        self.shininess = shininess

    def setTransparency(self, transparency):
        self.transparency = transparency
