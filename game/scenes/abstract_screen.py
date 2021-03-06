import pygame
from pygame.locals import *
from game import ResourceManager

class AbstractScreen:
    def __init__(self, menu, image, song=None, transform=False):
        res = ResourceManager.load_config().get_resolution()

        self._menu = menu

        self.image = ResourceManager.load_image_asset(image)
        if transform:
            self.image = pygame.transform.scale(self.image, res)

        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = res[1]

        self._song = song

        self._clicked = None
        self._gui_elements = []

        (self._x_total, self._y_total) = ResourceManager.load_config().get_resolution()
        (self._x_total_half, self._y_total_half) = (self._x_total>>1, self._y_total>>1)

    def start_scene(self):
        if self._song != None:
            song_path = ResourceManager.get_song_path(self._song)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(loops=-1)

    def events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self._clicked = None
                for element in self._gui_elements:
                    if element.pos_in_element(event.pos):
                        self._clicked = element
                        break
            if event.type == MOUSEBUTTONUP:
                for element in self._gui_elements:
                    if element.pos_in_element(event.pos):
                        if self._clicked != None and element == self._clicked:
                            self._clicked.callback()
                            break

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for element in self._gui_elements:
            element.draw(screen)
