

class Ray:
    def __init__(self, p, ray_direction, intersection_point):
        self.p = p
        self.ray_direction = ray_direction
        self.intersection_point = intersection_point

    # Get and set functions
    def getP(self):
        return self.p

    def getDirection(self):
        return self.ray_direction

    def getIntersectionPoint(self):
        return self.intersection_point

    def setP(self, p):
        self.p = p

    def setDirection(self, ray_direction):
        self.ray_direction = ray_direction

    def setIntersectionPoint(self, intersection_point):
        self.intersection_point = intersection_point