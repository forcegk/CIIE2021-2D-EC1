from game import ResourceManager
from .character import Character
from .enemy import Enemy
from ..farm import Farm

class Shot(Enemy):
    SPEEDX = 10
    SPEEDY = 0

    def __init__(self, level, data, coord, left, scroll):
        Enemy.__init__(self, level, data, coord, Shot.SPEEDX, Shot.SPEEDY, False)

        self._scroll = scroll
        self._left = left

    def move_cpu(self):
        direction_x = Character.LEFT if self._left else Character.RIGHT
        Character.move(self, (direction_x, Character.STILL))

    def update(self, elapsed_time):
        Enemy.update(self, elapsed_time)
        width, _ = ResourceManager.load_config().get_resolution()

        if Farm.touches_anything_visible(self) or self.rect.left < -50 or self.rect.right > width + 50:
            self.kill()