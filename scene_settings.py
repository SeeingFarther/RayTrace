class SceneSettings:
    def __init__(self, background_color, root_number_shadow_rays, max_recursions):
        self.background_color = background_color
        self.root_number_shadow_rays = root_number_shadow_rays
        self.max_recursions = max_recursions

    # Get and set functions
    def getBackgroundColor(self):
        return self.background_color

    def getShadowRays(self):
        return self.root_number_shadow_rays

    def getMaxRecursions(self):
        return self.max_recursions

    def setBackgroundColor(self, background_color):
        self.background_color = background_color

    def setShadowRays(self, root_number_shadow_rays):
        self.root_number_shadow_rays = root_number_shadow_rays

    def setMaxRecursions(self, max_recursions):
        self.max_recursions = max_recursions