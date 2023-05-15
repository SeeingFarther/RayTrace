class Light:
    def __init__(self, position, color, specular_intensity, shadow_intensity, width_radius):
        self.position = position
        self.color = color
        self.specular_intensity = specular_intensity
        self.shadow_intensity = shadow_intensity
        self.width_radius = width_radius