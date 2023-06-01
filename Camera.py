class Camera:
    def __init__(self, position, look_at, up_vector, screen_distance, screen_width):
        self.position = position
        self.look_at = look_at
        self.up_vector = up_vector
        self.screen_distance = screen_distance
        self.screen_width = screen_width

# Get and set functions
    def getPosition(self):
        return self.position

    def getLookAt(self):
        return self.look_at

    def getUp(self):
        return self.up_vector

    def getScreenDistance(self):
        return self.screen_distance

    def getScreenWidth(self):
        return self.screen_width

    def setPosition(self, position):
        self.position = position

    def setLookAt(self,look_at):
        self.look_at = look_at

    def setUp(self, up_vector):
        self.up_vector = up_vector

    def setScreenDistance(self, screen_distance):
        self.screen_distance = screen_distance

    def setScreenWidth(self, screen_width):
        self.screen_width = screen_width