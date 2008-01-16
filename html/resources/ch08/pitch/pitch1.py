from gasp import *

begin_graphics(800, 600, title="Catch", background=color.yellow)

x = 10
y = 300
ball = Circle((x, y), 10, filled=True)
dx = 4
dy = 1

while x < 810:
    x += dx
    y += dy
    move_to(ball, (x, y))
    sleep(0.01)

end_graphics()
