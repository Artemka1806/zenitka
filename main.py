#Бібліотеки/модулі
import time

import pygame as pg
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

#"Підганяю" систему координат pymunk під систему координат pygame
pymunk.pygame_util.positive_y_is_up = False

#Налаштування Pygame
RES = WIDTH, HEIGHT = 1000, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (179, 169, 168)

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)
font = pg.font.SysFont("Arial", 16)

#Налаштування Pymunk
space = pymunk.Space()
space.gravity = 0, 1000

#Змінна для паузи
paused = False

#Платформа
segment_shape = pymunk.Segment(space.static_body, (1, HEIGHT), (WIDTH, HEIGHT), 26)
space.add(segment_shape)
segment_shape.elasticity = 0.8
segment_shape.friction = 1.0

#Змінні для цілі
target_x_pos, target_y_pos = 50, 150
target_dir=1

#Ціль
target_mass, target_size = 1, (50, 5)
target_moment = pymunk.moment_for_box(target_mass, target_size)
target_body = pymunk.Body(target_mass, target_moment,pymunk.Body.KINEMATIC)
target_body.color = (255, 50, 50, 255)
target_body.position = target_x_pos, target_y_pos
target_shape = pymunk.Poly.create_box(target_body, target_size)
target_shape.elasticity = 0.8
target_shape.friction = 1.0
space.add(target_body, target_shape)

def shoot(target_pos_x,target_pos_y):
	cannonball_radius = 10
	cannonball_mass = mass_s.get_value()
	cannonball_moment = pymunk.moment_for_circle(cannonball_mass, 0, cannonball_radius)
	cannonball_body = pymunk.Body(cannonball_mass, cannonball_moment)
	cannonball_shape = pymunk.Circle(cannonball_body, cannonball_radius)
	cannonball_body.position = (cannon_body.position.x, cannon_body.position.y)
	cannonball_shape.friction = 1.0
	space.add(cannonball_body, cannonball_shape)
	cannonball = pymunk.Circle(cannonball_body, cannonball_radius)
	cannonball.body.position = (cannon_body.position.x, cannon_body.position.y)
	direction = pymunk.Vec2d(target_pos_x - cannonball_body.position.x, target_pos_y - cannonball_body.position.y)
	direction = direction.normalized()
	force = direction * power_s.get_value()
	cannonball.body.apply_impulse_at_local_point(force)


shooting = False

#Гармата
canon_x_pos, canon_y_pos = 500, 575

cannon_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
cannon_shape = pymunk.Circle(cannon_body, 10)
cannon_shape.sensor = True
cannon_shape.color = (255, 50, 50, 255)
cannon_body.position = canon_x_pos, canon_y_pos
space.add(cannon_body, cannon_shape)


class Slider:
	def __init__(self, x, y, width, height, min_value, max_value, default_value):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.min_value = min_value
		self.max_value = max_value
		self.value = default_value

	def draw(self, window):
		pg.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height))
		value_width = (self.value - self.min_value) / (self.max_value - self.min_value) * self.width
		pg.draw.rect(window, WHITE, (self.x, self.y, value_width, self.height))

	def update(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				mouse_x, mouse_y = pg.mouse.get_pos()
				if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
					self.value = (
						(mouse_x - self.x) / self.width * (self.max_value - self.min_value) + self.min_value
					)

	def get_value(self):
		return self.value



gravity_s = Slider(570, 0, 400, 20, -300, 1000, 100)
power_s = Slider(570, 30, 400, 20, 100, 5000, 4000)
distant_s = Slider(570, 60, 400, 20, 10, 1000, 80)
mass_s = Slider(570, 90, 400, 20, 1, 100, 5)


#Відмальовка PyGame
while True:
	#Заливка фону чорним
	surface.fill(pg.Color('black'))

	if paused==False:
		target_x_pos = target_x_pos + target_dir
		target_body.position = target_x_pos, target_y_pos

		if target_x_pos==950:
				target_dir=-1
		if target_x_pos==50:
				target_dir=1
		surface.blit(font.render("Esc для зупинки руху цілі", True, pg.Color("white")),(0, 0),)
	else:
		surface.blit(font.render("Esc для продовження руху цілі", True, pg.Color("white")),(0, 0),)

	#collision_point = pymunk.Shape.shapes_collide(cannonball_shape, target_shape)
	#if collision_point:
	#	print("Столкновение произошло!")

	for i in pg.event.get():
		if i.type == pg.QUIT:
			exit()
		elif i.type == pg.KEYDOWN:
			if i.key == pg.K_ESCAPE:
				if paused==False:
					paused=True
				else:
					paused=False
			elif i.key == pg.K_SPACE:

				if target_dir==1:
					target_coords_now = (target_x_pos+distant_s.get_value()*0.5, target_y_pos)
				else:
					target_coords_now = (target_x_pos-distant_s.get_value()*0.5, target_y_pos)

				shooting = True

		if i.type == pg.MOUSEBUTTONDOWN:
			if i.button == 1:
				mouse_x, mouse_y = pg.mouse.get_pos()
				shoot(mouse_x, mouse_y)

		if shooting:
			shoot(target_coords_now[0],target_coords_now[1])
			shooting = False

		power_s.update(i)
		gravity_s.update(i)
		distant_s.update(i)
		mass_s.update(i)
	power_s.draw(surface)
	gravity_s.draw(surface)
	distant_s.draw(surface)
	mass_s.draw(surface)

	surface.blit(font.render("Гравітація", True, pg.Color("white")),(450, 0),)
	surface.blit(font.render("Сила пострілу", True, pg.Color("white")),(450, 30),)
	surface.blit(font.render("Дальність від цілі", True, pg.Color("white")),(450, 60),)
	surface.blit(font.render("Маса снаряду", True, pg.Color("white")),(450, 90),)

	space.gravity = 0, gravity_s.get_value()

	#Поворот гармати в напрямку цілі
	target_position = pymunk.pygame_util.from_pygame(Vec2d(*(target_x_pos, target_y_pos)), surface)
	cannon_body.angle = (target_position - cannon_body.position).angle
	if target_dir==1:
		pg.draw.line(surface, (255, 255, 0), (canon_x_pos, canon_y_pos), (target_x_pos+distant_s.get_value()*0.5, target_y_pos))
	else:
		pg.draw.line(surface, (255, 255, 0), (canon_x_pos, canon_y_pos), (target_x_pos-distant_s.get_value()*0.5, target_y_pos))

	pg.draw.line(surface, (255, 255, 255), (canon_x_pos, canon_y_pos), (target_x_pos, target_y_pos))

	#Налаштування Pymunk і Pygame
	space.step(1 / FPS)
	space.debug_draw(draw_options)
			
	pg.display.flip()