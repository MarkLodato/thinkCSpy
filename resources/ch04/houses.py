from gasp import *

def draw_house(x, y):
    Box((x, y), 100, 100, color=color.BLUE, filled=True)
    Box((x+35, y), 30, 50, color=color.GREEN, filled=True)
    Box((x+20, y+60), 20, 20, color=color.YELLOW, filled=True)
    Box((x+60, y+60), 20, 20, color=color.YELLOW, filled=True)
    Polygon([(x, y+100), (x+50, y+140), (x+100, y+100)],
             color=color.RED, filled=True)
    
begin_graphics(title="Houses at Night", background=color.BLACK)

draw_house(20, 20)
draw_house(250, 20)
draw_house(500, 20)
draw_house(135, 160)
draw_house(375, 160)
draw_house(255, 320)

update_when('key_pressed')

end_graphics()
