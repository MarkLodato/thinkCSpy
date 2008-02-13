from gasp import *

begin_graphics(800, 600, title="Catch", background=color.yellow)

mitt_x = 780
mitt_y = 300
mitt = Circle((mitt_x, mitt_y), 20)

while True:
    if key_pressed('j') and mitt_y <= 580:
        mitt_y += 5
    elif key_pressed('k') and mitt_y >= 20:
        mitt_y -= 5
    elif key_pressed('escape'):
        break
    move_to(mitt, (mitt_x, mitt_y))
    sleep(0.01)

end_graphics()
