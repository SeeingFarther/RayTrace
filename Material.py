class Material:
    def __init__(self, diffuse_color, specular_color, reflection_color, phong_specularity, transparency):
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.reflection_color = reflection_color
        self.phong_specularity = phong_specularity
        self.transparency = transparency

    # Get and set functions
    def getDiffuseColor(self):
        return self.diffuse_color

    def getSpecularColor(self):
        return self.specular_color

    def getReflectionColor(self):
        return self.reflection_color

    def getPhongSpecularity(self):
        return self.phong_specularity

    def getTransparency(self):
        return self.transparency

    def setDiffuseColor(self, diffuse_color):
        self.diffuse_color = diffuse_color

    def setSpecularColor(self, specular_color):
        self.specular_color = specular_color

    def setReflectionColor(self, reflection_color):
        self.reflection_color = reflection_color

    def setPhongSpecularity(self, phong_specularity):
        self.phong_specularity = phong_specularity

    def setTransparency(self, transparency):
        self.transparency = transparency
