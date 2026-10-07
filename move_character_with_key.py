from math import hypot
from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_WIDTH = FRAME_HEIGHT = 100
FRAME_COUNT = 8
MOVE_SPEED = 100.0
ANIMATION_INTERVAL = 0.05
MAX_DT = 0.1
LOOP_DELAY = 0.01
LEFT, RIGHT = -1, 1
IDLE, MOVE = 0, 1

running = True
x, y = TUK_WIDTH / 2, TUK_HEIGHT / 2
frame = 0
animation_elapsed = 0.0
pressed_keys = set()
facing = RIGHT
state = IDLE
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


def update_movement(dt):
    global x, y, facing, state, frame, animation_elapsed
    previous_visual = (state, facing)
    previous_position = (x, y)
    dx = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    dy = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    if dx:
        facing = RIGHT if dx > 0 else LEFT
    length = hypot(dx, dy)
    if length:
        x += dx / length * MOVE_SPEED * dt
        y += dy / length * MOVE_SPEED * dt
    x = max(FRAME_WIDTH / 2, min(x, TUK_WIDTH - FRAME_WIDTH / 2))
    y = max(FRAME_HEIGHT / 2, min(y, TUK_HEIGHT - FRAME_HEIGHT / 2))
    state = MOVE if (x, y) != previous_position else IDLE
    changed = (state, facing) != previous_visual
    if changed:
        frame = 0
        animation_elapsed = 0.0
    return changed


def frame_dt(raw_dt):
    return max(0.0, min(raw_dt, MAX_DT))


def update_animation(dt, changed=False):
    global frame, animation_elapsed
    if changed:
        return
    animation_elapsed += dt
    steps = int((animation_elapsed + 1e-12) / ANIMATION_INTERVAL)
    if steps:
        frame = (frame + steps) % FRAME_COUNT
        animation_elapsed = max(0.0, animation_elapsed - steps * ANIMATION_INTERVAL)


def draw_scene():
    clear_canvas()
    background.draw(TUK_WIDTH / 2, TUK_HEIGHT / 2)
    if state == MOVE:
        source_y = 100 if facing == RIGHT else 0
    else:
        source_y = 300 if facing == RIGHT else 200
    character.clip_draw(frame * FRAME_WIDTH, source_y,
                        FRAME_WIDTH, FRAME_HEIGHT, x, y)
    update_canvas()


def main():
    global background, character
    open_canvas(TUK_WIDTH, TUK_HEIGHT)
    try:
        background = load_image('TUK_GROUND.png')
        character = load_image('animation_sheet.png')
        previous_time = get_time()
        while running:
            current_time = get_time()
            dt = frame_dt(current_time - previous_time)
            previous_time = current_time
            handle_events()
            if not running:
                break
            changed = update_movement(dt)
            update_animation(dt, changed)
            draw_scene()
            delay(LOOP_DELAY)
    finally:
        close_canvas()

if __name__ == '__main__':
    main()
