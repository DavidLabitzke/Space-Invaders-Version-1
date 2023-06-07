import pygame
from wall import Wall


class WallManager:
    def __init__(self, wall_image):
        self.wall_image = wall_image
        self.walls = [Wall(100, 350, self.wall_image), Wall(300, 350, self.wall_image),
                      Wall(500, 350, self.wall_image), Wall(700, 350, self.wall_image)]

    def remove_dead_walls(self):
        for wall in self.walls:
            if wall.health == 0:
                self.walls.remove(wall)

    def reset_walls(self):
        self.walls = [Wall(100, 350, self.wall_image), Wall(300, 350, self.wall_image),
                      Wall(500, 350, self.wall_image), Wall(700, 350, self.wall_image)]
