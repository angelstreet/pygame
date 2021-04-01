# AngelStreet @2021
####################################################
import pygame as pg
from engine.src.game import Game, FONT_NAME, WHITE, BLACK, LAYER_GAME, LAYER_UI
from engine.src.player import HorizontalPlayer, VerticalPlayer, FourDirPlayer

FPS = 60
GAME_WIDTH, GAME_HEIGHT = 600, 400
TITLE = "Sprite animation"
KEYBOARD = "AZERTY"


def get_keyboard_keys():
    if KEYBOARD == "AZERTY":
        return pg.K_q, pg.K_d, pg.K_z, pg.K_s
    return pg.K_a, pg.K_d, pg.K_w, pg.K_s


def next(game, player, direction):
    if isinstance(player, HorizontalPlayer):
        if not player.force_right:
            player.force_right = True
            direction.text = "horizontal force right"
        else:
            player.kill()
            player = game.add_v_player(
                LAYER_GAME, 250, 150, '../assets/data/player1_4dir.json', 0.5)
            direction.text = "vertical"

    elif isinstance(player, VerticalPlayer):
        if not player.force_up:
            player.force_up = True
            direction.text = "vertical force up"
        else:
            player.kill()
            player = game.add_4D_player(
                LAYER_GAME, 250, 150, '../assets/data/player1_4dir.json', 0.5)
            direction.text = "4 dir"
    elif isinstance(player, FourDirPlayer):
        player.kill()
        player = game.add_h_player(LAYER_GAME, 250, 150, '../assets/data/player1_4dir.json', 0.5)
        direction.text = "add_h_player"
        player.force_right = False
    return player


def main():
    # INIT pg----------------------
    pg.init()  # initiates pg
    pg.display.set_caption(TITLE)
    display = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    # GAME ---------------------
    game = Game(display, GAME_WIDTH, GAME_HEIGHT)
    fpstext = game.add_dynamic_text(LAYER_UI, GAME_WIDTH-70, 20, '', FONT_NAME, 20, BLACK, None)
    direction = game.add_dynamic_text(LAYER_UI, 150, 25, 'horizontal', FONT_NAME, 20, BLACK, None)
    player = game.add_h_player(LAYER_GAME, 250, 150, '../assets/data/player1_4dir.json', 0.5)
    button = game.add_button(LAYER_GAME, 20, 20, 60, 30, 'next', FONT_NAME, 20, WHITE, BLACK)
    K_LEFT, K_RIGHT, K_UP, K_DOWN = get_keyboard_keys()
    # LOOP ---------------------
    running = True
    clock = pg.time.Clock()
    button_over = False
    k_space_released = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return pg.quit()
            if event.type == pg.MOUSEMOTION:
                if not button_over and button.rect.collidepoint(pg.mouse.get_pos()):
                    button.rollover()
                    button_over = True
                elif button_over and not button.rect.collidepoint(pg.mouse.get_pos()):
                    button.rollout()
                    button_over = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if button.rect.collidepoint(pg.mouse.get_pos()):
                    player = next(game, player, direction)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and k_space_released:
                    player = next(game, player, direction)
                    k_space_released = False
                elif event.key == pg.K_LEFT or event.key == K_LEFT:
                    player.K_LEFT = True
                elif event.key == pg.K_RIGHT or event.key == K_RIGHT:
                    player.K_RIGHT = True
                if event.key == pg.K_UP or event.key == K_UP:
                    player.K_UP = True
                elif event.key == pg.K_DOWN or event.key == K_DOWN:
                    player.K_DOWN = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    k_space_released = True
                elif event.key == pg.K_LEFT or event.key == K_LEFT:
                    player.K_LEFT = False
                elif event.key == pg.K_RIGHT or event.key == K_RIGHT:
                    player.K_RIGHT = False
                if event.key == pg.K_UP or event.key == K_UP:
                    player.K_UP = False
                elif event.key == pg.K_DOWN or event.key == K_DOWN:
                    player.K_DOWN = False
        fpstext.text = str(int(clock.get_fps()))+" FPS"
        game.draw()
        clock.tick(FPS)
        pg.display.update()


if __name__ == "__main__":
    main()
