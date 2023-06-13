""" GUI
"""


import gettext
import os

import pygame

from .server_api import ServerAPI


translations_path = os.path.join(os.path.dirname(__file__), 'translation')
translations = {
    'en_NG.UTF-8': gettext.translation('client', translations_path, languages=['en'], fallback=True),
    'ru_RU.UTF-8': gettext.translation('client', translations_path, languages=['ru'])
}

obstacle_x = 400
obstacle_y = 400
obstacle_width = 40
obstacle_height = 40
player_x = 200
player_y = 400
player_width = 20
player_height = 20


class Field():
    """_summary_
    """
    def __init__(self, screen, **kwargs) -> None:
        """_summary_

        :param screen: _description_
        :type screen: _type_
        """
        self.WIDTH, self.HEIGHT, self.MARGIN = 30, 30, 5
        self.grid = [[None] * 8 for i in range(8)]
        # как они там обозначаются?
        self.notation2coords = lambda x: (8 - int(x[1]), ord(x[0]) - ord('a'))  # tuple : "a", "3"
        self.coords2notation = lambda x: (chr(x[1] + ord('a')), 8 - x[0])  # tuple (2, 3)
        self.grid_coordinates = lambda x: (x[0] // (self.HEIGHT + self.MARGIN), x[1] // (self.WIDTH + self.MARGIN))


class ChessGame():
    """_summary_
    """
    # game_state: start_menu, game, game_over
    def __init__(self, **kwargs) -> None:
        """_summary_
        """
        pygame.init()
        self.screen_shape = (750, 450)
        self.screen = pygame.display.set_mode(self.screen_shape)
        self.game_state = 'start_menu'
        self.buttons = dict()
        self.draw_start_menu()

    def draw_start_menu(self) -> None:
        """_summary_
        """
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 50)
        title = font.render(_('Chess'), True, (255, 255, 255))  # noqa: F821
        self.screen.blit(title, (self.screen_shape[0]/2 - title.get_width()/2, 100))

        start_button_hotseat = Button(pos=(self.screen_shape[0] // 4, 300), text=_('Start hotseat'), font=30)  # noqa: F821
        start_button_hotseat.show(self.screen)
        create_room_button = Button(pos=(self.screen_shape[0] // 2, 300), text=_('Create room'), font=30)  # noqa: F821
        create_room_button.show(self.screen)
        join_room_button = Button(pos=(self.screen_shape[0] // 4 * 3, 300), text=_('Join room'), font=30)  # noqa: F821
        join_room_button.show(self.screen)

        self.buttons = dict()
        self.buttons['start_hotseat'] = start_button_hotseat
        self.buttons['create_room'] = create_room_button
        self.buttons['join_room'] = join_room_button
        pygame.display.update()

    def run(self) -> None:
        """_summary_
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif self.game_state == 'start_menu':
                    if self.buttons['start_hotseat'].clicked(event):
                        self.draw_game()
                        self.game_type = 'hotseat'
                    elif self.buttons['create_room'].clicked(event):
                        self.draw_new_room()
                    elif self.buttons['join_room'].clicked(event):
                        self.draw_join_room()

    def draw_new_room(self) -> None:
        """_summary_
        """
        pass

    def draw_join_room(self) -> None:
        """_summary_
        """
        pass

    def draw_game_over(self) -> None:
        """_summary_
        """
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render(_('Game Over'), True, (255, 255, 255))  # noqa: F821
        self.screen.blit(title, (self.screen_shape[0]/2 - title.get_width()/2, self.screen_shape[1]/2 - title.get_height()/3))
        self.game_state = 'game_over'
        self.buttons = dict()
        pygame.display.update()


class Button():
    """_summary_
    """
    def __init__(self, pos: tuple[int, int] = None, text: str = None, font: int = 30, **kwargs) -> None:
        """_summary_

        :param pos: _description_, defaults to None
        :type pos: tuple[int, int], optional
        :param text: _description_, defaults to None
        :type text: str, optional
        :param font: _description_, defaults to 30
        :type font: int, optional
        """
        self.x, self.y = pos
        self.font = pygame.font.SysFont('Arial', font)
        self.size = (kwargs['size'] if 'size' in kwargs else None)
        self.draw_text(text, **kwargs)

    def draw_text(self, text: str, colour: str = 'white', background: str = 'black', **kwargs) -> None:
        """_summary_

        :param text: _description_
        :type text: str
        :param colour: _description_, defaults to 'white'
        :type colour: str, optional
        :param background: _description_, defaults to 'black'
        :type background: str, optional
        """
        self.text = self.font.render(text, True, pygame.Color(colour))
        # check outer size !
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(background)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, screen) -> None:
        """_summary_

        :param screen: _description_
        :type screen: _type_
        """
        screen.blit(self.surface, (self.x - self.size[0] // 2, self.y - self.size[1] // 2))

    def clicked(self, event) -> None:
        """_summary_

        :param event: _description_
        :type event: _type_
        :return: _description_
        :rtype: _type_
        """
        x, y = pygame.mouse.get_pos()
        return event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and self.rect.collidepoint(x, y)


def game() -> None:
    """_summary_
    """
    translations['ru_RU.UTF-8'].install()  # установка русского
    # translations['en_NG.UTF-8'].install()  # установка английского

    server_api = ServerAPI()
    server_api.send('login Marlius')
    server_api.send('new')
    print(server_api.receive())
    server_api.send('move e 2 e 4')
