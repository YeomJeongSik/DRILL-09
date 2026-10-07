from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_WIDTH = FRAME_HEIGHT = 100
FRAME_COUNT = 8

running = True
x, y = TUK_WIDTH / 2, TUK_HEIGHT / 2
frame = 0
background = None
character = None


def draw_scene():
    clear_canvas()
    background.draw(TUK_WIDTH / 2, TUK_HEIGHT / 2)
    update_canvas()


def main():
    global background
    open_canvas(TUK_WIDTH, TUK_HEIGHT)
    background = load_image('TUK_GROUND.png')
    draw_scene()
    close_canvas()


if __name__ == '__main__':
    main()
