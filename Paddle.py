# package pong.model

from model.Config import GAME_HEIGHT




# A Paddle for the Pong game
class Paddle:

    WIDTH = 10
    HEIGHT = 60
    PADDLE_SPEED = 5
    MAX_DX = 2
    MAX_DY = 2

    def __init__(self, x, y, width=10, height=60, dx=0, dy=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_center_x(self):
        return self.x + self.width / 2

    def get_center_y(self):
        return self.y + self.height / 2

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_max_x(self):
        return self.x + self.width

    def get_max_y(self):
        return self.y + self.height

    def set_dx(self, dx):
        self.dx = dx

    def set_dy(self, dy):
        self.dy = dy

    def stop(self):
        self.dx = self.dy = 0

    def intersects(self, ball):
        above = ball.get_max_y() < self.get_y()
        below = ball.get_y() > self.get_max_y()
        left_of = ball.get_max_x() < self.get_x()
        right_of = ball.get_x() > self.get_max_x()
        return not (above or below or left_of or right_of)