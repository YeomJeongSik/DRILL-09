from math import hypot
from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_WIDTH = FRAME_HEIGHT = 100
FRAME_COUNT = 8

running = True
x, y = TUK_WIDTH / 2, TUK_HEIGHT / 2
frame = 0
pressed_keys = set()
background = None
character = None


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
            pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)


def update_movement():
    global x, y
    dx = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    dy = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    length = hypot(dx, dy)
    if length:
        x += dx / length * 5
        y += dy / length * 5


def draw_scene():
    clear_canvas()
    background.draw(TUK_WIDTH / 2, TUK_HEIGHT / 2)
    character.clip_draw(frame * FRAME_WIDTH, 300,
                        FRAME_WIDTH, FRAME_HEIGHT, x, y)
    update_canvas()


def main():
    global background, character, frame
    open_canvas(TUK_WIDTH, TUK_HEIGHT)
    background = load_image('TUK_GROUND.png')
    character = load_image('animation_sheet.png')
    while running:
        handle_events()
        if not running:
            break
        update_movement()
        draw_scene()
        frame = (frame + 1) % FRAME_COUNT
        delay(0.05)
    close_canvas()


if __name__ == '__main__':
    main()
