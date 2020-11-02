import pygame
from .abstract_menu import AbstractMenu
from .pause_screen import PauseScreen
from pygame.locals import *

class PauseMenu(AbstractMenu):
    def __init__(self, director):
        AbstractMenu.__init__(self, director)

        self._screen_list.append(PauseScreen(self))
        self._show_first_screen()

    def update(self, *args):
        pass

    def events(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.play_game()
                return
        AbstractMenu.events(self, events)

    def play_game(self):
        self._director.end_scene()

    def quit_game(self):
        from .main_menu import MainMenu
        self._director.quit_game()
        self._director.push_scene(MainMenu(self._director))