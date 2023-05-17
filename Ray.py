class Ray:
    def __init__(self, p, direction, intersection_point=-1, intersection_surface_index=-1):
        self.p = p
        self.direction = direction
        self.intersection_point = intersection_point
        self.intersection_surface_index = intersection_surface_index

    # Get and set functions
    def getP(self):
        return self.p

    def getDirection(self):
        return self.direction

    def getIntersectionPoint(self):
        return self.intersection_point

    def getIntersectionSurfaceIndex(self):
        return self.intersection_surface_index

    def setP(self, p):
        self.p = p

    def setDirection(self, direction):
        self.direction = direction

    def setIntersectionPoint(self, intersection_point):
        self.intersection_point = intersection_point

    def setIntersectionSurfaceIndex(self, intersection_surface_index):
        self.intersection_surface_index = intersection_surface_index
