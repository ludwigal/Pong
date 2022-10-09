# package pong.view
import pygame
import time
from model import *
from event.ModelEvent import ModelEvent
from event.EventBus import EventBus
from event.EventHandler import EventHandler
from view.theme.Cool import Cool
from view.theme.Duckie import Duckie
from model.Ball import *
#from model.Paddle import PADDLE_SPEED
from model.Config import *
from model.Paddle import *
pygame.init()

class PongGUI:

    screen = pygame.display.set_mode([500, 500])
    BLACK = (0, 0, 0)
    clock = pygame.time.Clock()
    GAME_SPEED =100
    BLUE = (0, 0, 255)
    GAME_WIDTH = 600
    GAME_HEIGHT = 400
    BALL_SPEED_FACTOR = 1.02
    HALF_SEC = 500_000_000
    paddle1 = Paddle(75, 200)
    paddle2 = Paddle(425, 200)
    RED = (255, 0, 0)
    ball=Ball(200,200)
    score1=0
    score2=0
    points_font = pygame.font.SysFont(None, 24)
    keep_going = True
    start = False

    """
    The GUI for the Pong game (except the menu).
    No application logic here just GUI and event handling.

    Run this to run the game.

    See: https://en.wikipedia.org/wiki/Pong
    """
    running = False    # Is game running?

    # ------- Keyboard handling ----------------------------------
    @classmethod
    def key_pressed(cls, event):
        #if not cls.running:
            #return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                cls.set_paddle2_speed(0, -Paddle.MAX_DY)
            elif event.key == pygame.K_s:
                cls.set_paddle2_speed(0, Paddle.MAX_DY)
            if event.key == pygame.K_UP:
                cls.set_paddle1_speed(0, -Paddle.MAX_DY)
            elif event.key == pygame.K_DOWN:
                cls.set_paddle1_speed(0, Paddle.MAX_DY)

    @classmethod
    def key_released(cls, event):
        #if not cls.running:
         #   return
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
                cls.stop_paddle1()
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_s]:
                cls.stop_paddle2()

    # ---- Menu handling (except themes) -----------------

    # TODO Optional

    @classmethod
    def new_game(cls):
        # TODO rebuild OO model as needed
        pass

    @classmethod
    def kill_game(cls):
        cls.running = False
        # TODO kill all aspects of game

    # -------- Event handling (events sent from model to GUI) ------------

    class ModelEventHandler(EventHandler):
        def on_model_event(self, evt: ModelEvent):
            if evt.event_type == ModelEvent.EventType.NEW_BALL:
                # TODO Optional
                pass
            elif evt.event_type == ModelEvent.EventType.BALL_HIT_PADDLE:
                PongGUI.assets.ball_hit_paddle_sound.play()
            elif evt.event_type == ModelEvent.EventType.BALL_HIT_WALL_CEILING:
                # TODO Optional
                pass

    # ################## Nothing to do below ############################

    # ---------- Theme handling ------------------------------

    assets = None

    @classmethod
    def handle_theme(cls, menu_event):
        s = "Cool"  # ((MenuItem) menu_event.getSource()).getText()
        last_theme = cls.assets
        try:
            if s == "Cool":
                cls.assets = Cool()
            elif s == "Duckie":
                cls.assets = Duckie()
            else:
                raise ValueError("No such assets " + s)
        except IOError as ioe:
            cls.assets = last_theme

    # ---------- Rendering -----------------
    @classmethod
    def render(cls):
        cls.screen.fill(cls.BLACK)
        points1 = cls.score1
        text = f"Player 1 points: {points1}"
        img1 = cls.points_font.render(text, True, cls.RED)
        rect = img1.get_rect()
        rect.topleft = (5, 5)
        cls.screen.blit(img1, rect)
        points2 = cls.score2
        text = f"Player 2 points: {points2}"
        img2 = cls.points_font.render(text, True, cls.RED)
        rect = img2.get_rect()
        rect.topright = (490,0)
        cls.screen.blit(img2, rect)
        pygame.draw.rect(cls.screen, cls.BLUE,
                         (cls.paddle1.get_x(), cls.paddle1.get_y(),
                          cls.paddle1.get_width(), cls.paddle1.get_height()))
        pygame.draw.rect(cls.screen, cls.BLUE,
                         (cls.paddle2.get_x(), cls.paddle2.get_y(),
                          cls.paddle2.get_width(), cls.paddle2.get_height()))
        pygame.draw.circle(cls.screen, cls.RED,
                       (cls.ball.get_center_x(), cls.ball.get_center_y()),
                       cls.ball.get_width() / 2)
        pygame.display.flip()

    @classmethod
    def menuthing(cls):
        cls.screen.fill(cls.BLACK)
        text = f"Whatsup gangsta, u wanna play?"
        img3 = cls.points_font.render(text, True, cls.RED)
        rect = img3.get_rect()
        rect.topleft = (100, 200)
        cls.screen.blit(img3, rect)

        text = f"Yes"
        img4 = cls.points_font.render(text, True, cls.RED)
        rect = img4.get_rect()
        rect.topleft = (100, 300)
        cls.screen.blit(img4, rect)


        text = f"No"
        img5 = cls.points_font.render(text, True, cls.RED)
        rect = img5.get_rect()
        rect.topleft = (300, 300)
        cls.screen.blit(img5, rect)

        pygame.display.flip()

#Det mesta ska inte ligga i GUI egentligen
    # ---------- Game loop ----------------

    @classmethod
    def run(cls):
        cls.set_ball_speed(1,-2)
        cls.menuthing()
        while cls.keep_going:
            events = pygame.event.get()
            cls.handle_events(events)
            if cls.start:
                cls.clock.tick(cls.GAME_SPEED)
                cls.update()
                cls.render()
                events = pygame.event.get()
                cls.handle_events(events)
        pygame.quit()

    @classmethod
    def update(cls):
        ball_angle = [cls.ball.dx, cls.ball.dy]
        cls.paddle1.move()
        cls.paddle2.move()
        cls.paddle_movements()
        cls.ball_bounce(ball_angle)
        cls.ball.move()

    @classmethod
    def handle_events(cls,events):
        for event in events:
            cls.key_pressed(event)
            cls.key_released(event)
            print(pygame.mouse.get_pos()[0])
            if pygame.mouse.get_pressed()[0] and 100 < pygame.mouse.get_pos()[0] < 124 and 300 < pygame.mouse.get_pos()[1] < 312:
                cls.start = True
            if pygame.mouse.get_pressed()[0] and 300 < pygame.mouse.get_pos()[0] < 324 and 300 < pygame.mouse.get_pos()[1] < 312:
                pygame.quit()
            if event.type == pygame.QUIT:
                cls.keep_going = False

    @classmethod
    def paddle_movements(cls):
        if cls.paddle2.y == 0 or cls.paddle2.y < 0:
            cls.stop_paddle2()
        if cls.paddle1.y == 0 or cls.paddle1.y < 0:
            cls.stop_paddle1()
        if cls.paddle2.y == 440 or cls.paddle2.y > 440:
            cls.stop_paddle2()
        if cls.paddle1.y == 440 or cls.paddle1.y > 440:
            cls.stop_paddle1()
        # print(ball_angle[0])
        # print(ball_angle[1])
        # if cls.paddle2.intersects(cls.ball) and ball_angle[0] > 0 and ball_angle[1] > 0:
        #   cls.set_ball_speed(-ball_angle[0], ball_angle[1])


    @classmethod
    def ball_bounce(cls, ball_angle):
        if cls.paddle2.intersects(cls.ball):
            cls.set_ball_speed(-ball_angle[0], ball_angle[1])
        if cls.paddle1.intersects(cls.ball):
            cls.set_ball_speed(-ball_angle[0], ball_angle[1])
        if cls.ball.get_low_y() > 420:
            cls.set_ball_speed(ball_angle[0],-ball_angle[1])
        if cls.ball.get_max_y() < 40:
            cls.set_ball_speed(ball_angle[0],-ball_angle[1])
        if cls.ball.get_max_x() == 500:
            cls.score1+=1
            cls.reset_ball()
        if cls.ball.get_max_x() < 40:
            cls.score2+=1
            cls.reset_ball()

    @classmethod
    def stop_paddle1(cls):
        cls.paddle1.stop()

    @classmethod
    def set_paddle1_speed(cls, dx, dy):
        cls.paddle1.set_dx(dx)
        cls.paddle1.set_dy(dy)

    @classmethod
    def stop_paddle2(cls):
        cls.paddle2.stop()

    @classmethod
    def set_paddle2_speed(cls, dx, dy):
        cls.paddle2.set_dx(dx)
        cls.paddle2.set_dy(dy)

    @classmethod
    def set_ball_speed(cls, dx, dy):
        cls.ball.set_dx(dx)
        cls.ball.set_dy(dy)

    @classmethod
    def reset_ball(cls):
        cls.ball.x = 200
        cls.ball.y = 200


if __name__ == "__main__":
    PongGUI.run()
