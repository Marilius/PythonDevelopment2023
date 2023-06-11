import pygame

obstacle_x = 400
obstacle_y = 400
obstacle_width = 40
obstacle_height = 40
player_x = 200
player_y = 400
player_width = 20
player_height = 20

class ChessGame():
    #game_state: start_menu, game, game_over
    def __init__(self, **kwargs):
        pygame.init()
        self.screen_shape = (750, 450)
        self.screen = pygame.display.set_mode(self.screen_shape)
        self.game_state = "start_menu"
        self.draw_start_menu()
    
    def draw_start_menu(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 50)
        title = font.render('Chess', True, (255, 255, 255))
        start_button = Button(pos=(self.screen_shape[0] // 2, 300), text="Start", font=30)
        start_button.show(self.screen)
        self.screen.blit(title, (self.screen_shape[0]/2 - title.get_width()/2, 100))
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.draw_game_over()

    
    def draw_game_over(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Over', True, (255, 255, 255))
        self.screen.blit(title, (self.screen_shape[0]/2 - title.get_width()/2, self.screen_shape[1]/2 - title.get_height()/3))
        self.game_state = "game_over"
        pygame.display.update()


class Button():
    def __init__(self, pos=None, text=None, font=30, **kwargs):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.size = (kwargs['size'] if 'size' in kwargs else None)
        self.draw_text(text, **kwargs)

    def draw_text(self, text, colour='white', background='black', **kwargs):
        self.text = self.font.render(text, True, pygame.Color(colour))
        #check outer size !
        self.size = self.text.get_size() 
        self.surface = pygame.Surface(self.size)
        self.surface.fill(background)
        self.surface.blit(self.text, (0, 0))
    
    def show(self, screen):
        screen.blit(self.surface, (self.x - self.size[0] // 2, self.y - self.size[1] // 2))
        




def game() -> None:
    ChessGame().run()


def game_() -> None:
    global game_state
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if game_state == "start_menu":
            draw_start_menu()
            if keys[pygame.K_SPACE]:
                player_x = 200
                player_y = 400
                game_state = "game"
                game_over = False
        elif game_state == "game_over":
            draw_game_over_screen()
            if keys[pygame.K_r]:
                game_state = "start_menu"
            if keys[pygame.K_q]:
                pygame.quit()
                quit()

        elif game_state == "game":
            if keys[pygame.K_LEFT]:
                player_x -= 1
            if keys[pygame.K_RIGHT]:
                player_x += 1

            if player_x + player_width > obstacle_x and player_x < obstacle_x + obstacle_width and player_y + player_height > obstacle_y and player_y < obstacle_y + obstacle_height:
                game_over = True
                game_state = "game_over"

            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0), (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
            pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_width, player_height))
            pygame.display.update()

        elif game_over:
            game_state = "game_over"
            game_over = False
