from .character import Character
from ..player_repository import PlayerRepository
from .animated_text import AnimatedText
from game import ResourceManager
from ..farm import Farm
from .shot import Shot
from ..audio.rocker import Rocker
import pygame


class Player(Character):
    PARRY_CD = 2
    PARRY_DUR = 0.5

    PARRY_ON = "Parry ON!"
    PARRY_OFF = "Parry OFF!"
    PARRY_TEXT = "Parry!"
    MASK_TEXT = "Mask!"
    HEART_TEXT = "Heart!"
    HIT_TEXT = "Damage!"

    MASK_COLOR = (0, 206, 209)
    PARRY_COLOR = (255, 165, 0)
    HIT_COLOR = (255, 0, 0)

    INVULNERABILITY_LAPSE = 1.3

    TRIGGER_HYST = 0.125

    def __init__(self, level, data, coord, speedx=25, speedy=40, invert=False, invincible=False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)

        self._repo = ResourceManager.get_player_repository()
        self._text = ResourceManager.get_text_repository()

        self._last_hit = Player.INVULNERABILITY_LAPSE
        self._parry = Player.PARRY_CD

        self._invincible = invincible
        self._end_parry = True

        self._pending_trigger = None
        self._last_triggered = Player.TRIGGER_HYST
        self._interact_last_displayed = AnimatedText.get_duration()
        self._interact = False

    def get_repository(self):
        return self._repo

    def set_repository(self, repo):
        self._repo = repo

    def update(self, elapsed_time):
        Character.update(self, elapsed_time)
        self._last_hit += elapsed_time
        self._parry += elapsed_time

        if self.is_invulnerable():
            if ((self._last_hit * 1000) % 150) > 85:
                self.image.set_alpha(0)

        # Iñaki no me toques el print que te veo venir
        # print(f"{self._position}")

        if self._parry >= Player.PARRY_DUR and not self._end_parry:
            self._end_parry = True
            pos = self._position[0], self._position[1] - self.rect.height
            self._text.add_sprite(AnimatedText(pos, Player.PARRY_OFF, self._scroll, Player.PARRY_COLOR))

    def move(self, keys_pressed, up, down, left, right, parry, dash, interact):
        if keys_pressed[up[0]] or keys_pressed[up[1]]:
            y = Character.UP
        elif keys_pressed[down]:
            y = Character.DOWN
        else:
            y = Character.STILL

        if keys_pressed[left]:
            x = Character.LEFT
        elif keys_pressed[right]:
            x = Character.RIGHT
        else:
            x = Character.STILL
        Character.move(self, (x, y))

        if keys_pressed[parry]:
            Rocker.action(Rocker.AUD_PARRY)
            self.do_parry()

        if keys_pressed[dash]:
            Rocker.action(Rocker.AUD_DASH)
            Character.do_dash(self)

        self._interact = keys_pressed[interact]

    def teleport(self, position):
        self.set_global_position(position)

    def hit(self):
        self._last_hit = 0
        current_health = self._repo.get_parameter(PlayerRepository.ATTR_HEALTH)
        self._repo.set_parameter(PlayerRepository.ATTR_HEALTH, current_health - 1)

        pos = self._position[0], self._position[1] - self.rect.height
        self._text.add_sprite(AnimatedText(pos, Player.HIT_TEXT, self._scroll, Player.HIT_COLOR))
        Rocker.action(Rocker.AUD_HIT)

    def insta_kill(self):
        if not self.is_invulnerable():
            Rocker.action(Rocker.AUD_HIT)
            self._repo.set_parameter(PlayerRepository.ATTR_HEALTH, 0)

    def is_interacting(self):
        return self._interact

    def is_parrying(self):
        return self._parry < Player.PARRY_DUR

    def is_invulnerable(self):
        return (self._last_hit < Player.INVULNERABILITY_LAPSE) or self._invincible

    def end_parry(self):
        self._parry = Player.PARRY_DUR
        self._end_parry = True
        pos = self._position[0], self._position[1] - self.rect.height
        self._text.add_sprite(AnimatedText(pos, Player.PARRY_TEXT, self._scroll, Player.PARRY_COLOR))

    def pick_mask(self):
        pos = (self._position[0], self._position[1] - self.rect.height)
        self._text.add_sprite(AnimatedText(pos, Player.MASK_TEXT, self._scroll, Player.MASK_COLOR))
        current_masks = self._repo.get_parameter(PlayerRepository.ATTR_MASKS)
        self._repo.set_parameter(PlayerRepository.ATTR_MASKS, current_masks + 1)

    def pick_toilet(self):
        pos = (self._position[0], self._position[1] - self.rect.height)
        #self._text.add_sprite(AnimatedText(pos, Player.MASK_TEXT, self._scroll, Player.MASK_COLOR))
        current_toilets = self._repo.get_parameter(PlayerRepository.ATTR_TOILET_PAPER)
        self._repo.set_parameter(PlayerRepository.ATTR_TOILET_PAPER, current_toilets + 1)
        print(f"{self._repo.get_parameter(PlayerRepository.ATTR_TOILET_PAPER)}")

    def do_parry(self):
        current_masks = self._repo.get_parameter(PlayerRepository.ATTR_MASKS)
        if self._parry >= Player.PARRY_CD and current_masks > 0:
            pos = self._position[0], self._position[1] - self.rect.height
            self._text.add_sprite(AnimatedText(pos, Player.PARRY_ON, self._scroll, Player.PARRY_COLOR))
            self._parry = 0
            self._end_parry = False
            self._repo.set_parameter(PlayerRepository.ATTR_MASKS, current_masks - 1)
