# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from ball import Ball, BigBall
import random
import game_world
import game_framework

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'




# bird Run Speed
PIXEL_PER_METER=(10.0/0.3)
RUN_SPEED_KMPH=20.0
RUN_SPEED_MPM=(RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS=(RUN_SPEED_MPM/60.0)
RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)
# fill here

# bird Action Speed
TIME_PER_ACTION=0.5
ACTION_PER_TIME=1.0/TIME_PER_ACTION
FRAMES_PER_ACTION=45               #설정 : 45
# fill here


class Run:

    @staticmethod
    def enter(bird, e):
        bird.dir, bird.action, bird.face_dir = 1, 1, ''
        
    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 14
        bird.x += bird.dir * RUN_SPEED_PPS*game_framework.frame_time
        if(bird.x>1600-bird.size[0]/2):
            bird.dir=-1
            bird.face_dir='h'
        elif(bird.x<0+bird.size[0]/2):
            bird.dir=1
            bird.face_dir=''


    @staticmethod
    def draw(bird):
        bird.image.clip_composite_draw(int(bird.frame%5) * 180+3, 180*2-180*int(bird.frame/5),160,160,0,bird.face_dir, bird.x, bird.y,100,100)


class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run
        self.transitions = {
            Run: {}
        }

    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.bird, e)
                self.cur_state = next_state
                self.cur_state.enter(self.bird, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.bird)




size=8*18/2
class Bird:
    def __init__(self):
        self.x, self.y = random.randint(200,600), random.randint(400,600)
        self.frame = random.randint(0,14)
        self.action = 3
        self.face_dir = ''
        self.dir = 0
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = 'Ball'
        self.v=10           # 새의 속도
        self.size=[180,180] # 새의 크기

    def fire_ball(self):

        if self.item ==   'Ball':
            ball = Ball(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball)
        elif self.item == 'BigBall':
            ball = BigBall(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball)
        # if self.face_dir == -1:
        #     print('FIRE BALL LEFT')
        #
        # elif self.face_dir == 1:
        #     print('FIRE BALL RIGHT')

        pass

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
