from enum import Enum, auto

import pygame as pg
from pygame.math import Vector2
from vi import Agent, BaseConfig, Simulation, serde


@serde
class FlockingConfig(BaseConfig):
    alignment_weight: float = 1.5
    cohesion_weight: float = 1
    separation_weight: float = 2

    delta_time: float = 3
    speed_limit: float = 4

    mass: int = 20

    def weights(self) -> tuple[float, float, float]:
        return (self.alignment_weight, self.cohesion_weight, self.separation_weight)


class Bird(Agent):
    config: FlockingConfig

    def update_position(self):
        # Pac-man-style teleport to the other end of the screen when trying to escape
        self.there_is_no_escape()

        neighbours = self.within_distance(25)
        n = len(neighbours)

        if n == 0:
            self.pos += self.move * self.config.delta_time
            return

        # Alignment
        average_velocity = sum((bird.move for bird in neighbours), Vector2(0)) / n
        alignment = (average_velocity - self.move).normalize()

        # Separation
        separation = (
            sum(((self.pos - bird.pos).normalize() for bird in neighbours), Vector2(0))
            / n
        )

        # Cohesion
        average_position = sum((bird.pos for bird in neighbours), Vector2(0)) / n
        cohesion = (average_position - self.pos - self.move).normalize()

        # ftotal
        steering = (
            self.config.alignment_weight * alignment
            + self.config.separation_weight * separation
            + self.config.cohesion_weight * cohesion
        ) / self.config.mass

        self.move = self.move + steering
        if self.move.length() > self.config.speed_limit:
            self.move = self.move / self.move.length() * self.config.speed_limit

        self.pos += self.move * self.config.delta_time


class Selection(Enum):
    ALIGNMENT = auto()
    COHESION = auto()
    SEPARATION = auto()


class FlockingLive(Simulation):
    selection: Selection = Selection.ALIGNMENT
    config: FlockingConfig

    def handle_event(self, by: float):
        if self.selection == Selection.ALIGNMENT:
            self.config.alignment_weight += by
        elif self.selection == Selection.COHESION:
            self.config.cohesion_weight += by
        elif self.selection == Selection.SEPARATION:
            self.config.separation_weight += by

    def before_render(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.handle_event(by=0.1)
                elif event.key == pg.K_DOWN:
                    self.handle_event(by=-0.1)
                elif event.key == pg.K_1:
                    self.selection = Selection.ALIGNMENT
                elif event.key == pg.K_2:
                    self.selection = Selection.COHESION
                elif event.key == pg.K_3:
                    self.selection = Selection.SEPARATION

        a, c, s = self.config.weights()
        print(f"A: {a:.1f} - C: {c:.1f} - S: {s:.1f}")


(
    FlockingLive(FlockingConfig())
    .batch_spawn_agents(Bird, image_paths=["images/white.png"])
    .run()
)
