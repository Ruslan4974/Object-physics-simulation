import pygame as pg
from random import randrange
import pymunk
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 1200, 1000
FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 8000

#создание мячиков
def create_ball(space, pos):
    ball_mass, ball_radius = 10, 60 #масса и радиус мяча
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius) #момент инерции тела
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = pos #появление мяча в указанном нами месте
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.8 #коэфициент упругости
    ball_shape.friction = 0.5 #коэфициент трения
    space.add(ball_body, ball_shape)


segment_shape = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 20) #пол
segment_shape.elasticity = 0.8
segment_shape.friction = 0.5
space.add(segment_shape)


#создание кирпичиков
box_mass, box_size = 1, (60, 40) #масса и размер
for x in range(120, WIDTH - 60, box_size[0]): #построение стены из кирпичиков
    for y in range(HEIGHT // 2, HEIGHT - 20, box_size[1]): #построение стены из кирпичиков
        box_moment = pymunk.moment_for_box(box_mass, box_size)
        box_body = pymunk.Body(box_mass, box_moment)
        box_body.position = x, y
        box_share = pymunk.Poly.create_box(box_body, box_size)
        box_share.elasticity = 0.1
        box_share.friction = 1.0
        box_share.color = [randrange(256) for i in range(4)]
        space.add(box_body, box_share)

while True:
    surface.fill(pg.Color('black'))

    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()

        #появление мяча по нажатию ЛКМ
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_ball(space, i.pos)

    space.step(1 / FPS)
    space.debug_draw(draw_options)

    pg.display.flip()
    clock.tick(FPS)