class Ray:
    def __init__(self, p, direction, intersection_point=-1, intersection_surface_index=-1):
        self.p = p
        self.direction = direction
        self.intersection_point = intersection_point
        self.intersection_surface_index = intersection_surface_index