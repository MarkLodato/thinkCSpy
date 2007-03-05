#!/usr/bin/python
"""Classes for creating worlds with Animals in them.

This module provides the following classes:

World, and its subclasses TurtleWorld, TurmiteWorld and AmoebaWorld.

Interpreter and Cell, which can belong to a World.

Animal and its subclasses Turtle, Turmite and Amoeba.


  Copyright 2006 Allen B. Downey, David Muffley, and Will Dickerson

    This file contains wrapper classes for use with tkinter.  It is
    only meant for use with the lab exercises in "How to Think Like
    a Computer Scientist: Learning with Python" and is not supported
    beyond that, and it is not very well documented.

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License as 
    published by the Free Software Foundation; either version 2 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see
    http://www.gnu.org/licenses/gpl.html or write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
    02110-1301 USA 
"""

from Tkinter import *
from math import *
from threading import *
from Queue import *
import random, os, time

# turning on debugging changes the behavior of Gui.fr so
# that the nested frame structure is apparent
debug = 0

# Gui provides wrappers for many of the methods in the Tk
# class; also, it keeps track of the current frame so that
# you can create new widgets without naming the parent frame
# explicitly.

class Gui(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frame = self          # the current frame
        self.frames = []           # the stack of nested frames

    # frame
    def fr(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        # save the current frame, then create the new one
        self.frames.append(self.frame)
        if debug:
            options['bd'] = 5
            options['relief'] = RIDGE
        self.frame = self.widget(Frame, side, fill, expand, anchor, **options)
        return self.frame

    # end frame
    def endfr(self):
        self.frame = self.frames.pop()

    # top level window
    def tl(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        # push the current frame, then create the new one
        self.frames.append(self.frame)
        self.frame = Toplevel(options)
        return self.frame

    # canvas
    def ca(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        return self.widget(Canvas, side, fill, expand, anchor, **options)

    # label
    def la(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        return self.widget(Label, side, fill, expand, anchor, **options)

    # button
    def bu(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        return self.widget(Button, side, fill, expand, anchor, **options)

    # menu button
    def mb(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        mb = self.widget(Menubutton, side, fill, expand, anchor,
                         **options)
        mb.menu = Menu(mb, relief=SUNKEN)
        mb['menu'] = mb.menu
        return mb

    # menu item
    def mi(self, mb, label='', **options):
        mb.menu.add_command(label=label, **options)        

    # entry
    def en(self, side=TOP, fill=NONE, expand=0, anchor=CENTER,
           text='', **options):
        en = self.widget(Entry, side, fill, expand, anchor, **options)
        en.insert(0, text)
        return en

    # text entry
    def te(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        return self.widget(Text, side, fill, expand, anchor, **options)

    # scrollbar
    def sb(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        return self.widget(Scrollbar, side, fill, expand, anchor, **options)

    class ScrollableText:
        def __init__(self, gui,
                     side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
            self.frame = gui.fr(side, fill, expand, anchor, **options)
            self.scrollbar = gui.sb(RIGHT, fill=Y)
            self.text = gui.te(LEFT, wrap=WORD,
                                 yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.text.yview)
            gui.endfr()
            
    # scrollable text
    # returns a ScrollableText object that contains a frame, a
    # text entry and a scrollbar.
    # note: the options provided to st apply to the frame only;
    # if you want to configure the other widgets, you have to do
    # it after invoking st
    def st(self, side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        return self.ScrollableText(self, side, fill, expand, anchor, **options)

    # this is the mother of all widget constructors.  the constructor
    # argument is the function object that will be called to build
    # the new widget
    def widget(self, constructor,
               side=TOP, fill=NONE, expand=0, anchor=CENTER, **options):
        widget = constructor(self.frame, options)
        widget.pack(side=side, fill=fill, expand=expand, anchor=anchor)
        return widget

    # the following are wrappers on the tk canvas items

    def create_circle(self, x, y, r, fill='', **options):
        options['fill'] = fill
        coords = self.trans([[x-r, y-r], [x+r, y+r]])
        tag = self.canvas.create_oval(coords, options)
        return tag;
    
    def create_oval(self, coords, fill='', **options):
        options['fill'] = fill
        return self.canvas.create_oval(self.trans(coords), options)

    def create_rectangle(self, coords, fill='', **options):
        options['fill'] = fill
        return self.canvas.create_rectangle(self.trans(coords), options)

    def create_line(self, coords, fill='black', **options):
        options['fill'] = fill
        tag = self.canvas.create_line(self.trans(coords), options)
        return tag
    
    def create_polygon(self, coords, fill='', **options):
        options['fill'] = fill
        return self.canvas.create_polygon(self.trans(coords), options)

    def create_text(self, coord, text='', fill='black', **options):
        options['text'] = text
        options['fill'] = fill
        return self.canvas.create_text(self.trans([coord]), options)

    def create_image(self, coord, image, **options):
        options['image'] = image
        return self.canvas.create_image(self.trans([coord]), options)

    def itemconfig(self, tag, **options):
        self.canvas.itemconfig(tag, options)

    def itemcget(self, tag, option):
        return self.canvas.itemcget(tag, option)

    def delete_item(self, tag):
        self.canvas.delete(tag)

    def move_item(self, tag, dx, dy):
        self.canvas.move(tag, dx, dy)

    def print_canvas(self, filename='gui.eps'):
        ps = self.canvas.postscript()
        fp = open(filename, 'w')
        fp.write(ps)
        fp.close()

    def trans(self, coords):
        for trans in self.transforms:
            coords = trans.trans_list(coords)
        return coords


# the following is adapted from Python Cookbook page 225,
# also available at
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65202

def _get_method_names (cls):
    import types
    
    result = []
    for name, func in cls.__dict__.items():
        if type(func) == types.FunctionType:
            result.append((name, func))

    for base in cls.__bases__:
        result.extend(_get_method_names(base))

    return result


class _SynchronizedMethod:

    def __init__ (self, method, obj, lock):
        self.__method = method
        self.__obj = obj
        self.__lock = lock

    def __call__ (self, *args, **kwargs):
        self.__lock.acquire()
        try:
            return self.__method(self.__obj, *args, **kwargs)
        finally:
            self.__lock.release()

class SynchronizedObject:
    
    def __init__ (self, obj, ignore=[], lock=None):
        self.__methods = {}
        self.__obj = obj
        lock = lock and lock or RLock()
        for name, method in _get_method_names(obj.__class__):
            if not name in ignore:
                self.__methods[name] = _SynchronizedMethod(method, obj, lock)

    def __getattr__(self, name):
        try:
            return self.__methods[name]
        except KeyError:
            return getattr(self.__obj, name)


class _QueueMethod:

    def __init__ (self, method, obj, queue):
        self.__method = method
        self.__obj = obj
        self.__queue = queue

    def __call__ (self, *args, **kwargs):
        callable = Callable(self.__method, self.__obj, *args, **kwargs)
#        self.__queue.put(callable)
        callable()


class QueueObject:
    def __init__(self, obj, methods=None):
        self.__dict__['_QueueObject__methods'] = {}
        self.__dict__['_QueueObject__obj'] = obj
        self.__dict__['_QueueObject__queue'] = Queue()

        methods = methods or _get_method_names(obj.__class__)

        import types
        for name, meth in methods:
            if type(meth) == types.FunctionType:
                self.__dict__['_QueueObject__methods'][name] = _QueueMethod(
                    meth, obj, self.__queue)

    def put(self, callable): self.__queue.put(callable)

    def get(self): return self.__queue.get_nowait()

    def __getattr__(self, name):
        try:
            return self.__methods[name]
        except KeyError:
            return getattr(self.__obj, name)

    def __setattr__(self, name, value):
        setattr(self.__obj, name, value)



class Callable:
    # see Python Cookbook 9.1, page 302
    
    def __init__(self, func, *args, **kwds):
        self.func = func
        self.args = args
        self.kwds = kwds

    def __call__(self):
        return apply(self.func, self.args, self.kwds)


class Transform:
    def trans_list(self, points):
        return [self.trans(p) for p in points]

    def invert_list(self, points):
        return [self.invert(p) for p in points]
    

class CanvasTransform(Transform):
    def __init__(self, width, height, xscale=1, yscale=1):
        self.width = width
        self.height = height
        self.xscale = xscale
        self.yscale = yscale
    
    def trans(self, p):
        x =  p[0] * self.xscale + self.width/2
        y = -p[1] * self.yscale + self.height/2      
        return [x, y]



class World(Gui):

    def __init__(self):
        Gui.__init__(self)
        self.exists = True
        self.animals = []
        self.inter = Interpreter(self, top_globals, top_locals)
        self.lock = Lock()
        
    def quit(self):
        self.exists = False
        Gui.quit(self)

    def register(self, animal):
        self.animals.append(animal)

    def unregister(self, animal):
        self.animals.remove(animal)

    def acquire(self): self.lock.acquire()
    def release(self): self.lock.release()

    def clear(self):
        for animal in self.animals:
            if animal.control:
                animal.control.destroy()
            animal.undraw()
        self.animals = []
        self.delete_item('all')

    def step(self):
        for animal in self.animals:
            animal.step()
        
    def run(self):
        self.running = 1
        while self.exists and self.running:
            self.step()
            self.update()
            time.sleep(self.delay)

    def stop(self):
        self.running = 0

    def map_animals(self, callable):
        map(callable, self.animals)
        
    def run_text(self):
        source = self.te_code.get(1.0, END)
        self.inter.run_code(source, '<user-provided code>')

    def run_file(self):
        filename = self.en_file.get()
        fp = file(filename)
        source = fp.read()
        self.inter.run_code(source, filename)

    def trans(self, coords):
        for trans in self.transforms:
            coords = trans.trans_list(coords)
        return coords

    def invert(self, coords):
        for trans in self.transforms:
            coords = trans.invert_list(coords)
        return coords

class Agitator(Thread):

    def __init__(self, delay, callable, *args, **kwds):
        Thread.__init__(self, target=self.agitate)
        self.callable = callable
        self.args = args
        self.kwds = kwds
        self.delay = delay
        self.running = 1
        self.start()

    def agitate(self):
        while self.running:
            self.callable(*self.args, **self.kwds)
            time.sleep(self.delay)
            

class AmoebaWorld(World):

    def __init__(self):
        World.__init__(self)
        self.ca_width = 400
        self.ca_height = 400
        self.transforms = [ CanvasTransform(
                                  self.ca_width, self.ca_height, 20, 20) ]
        self.animals = []
        self.thread = None

        self.fr(LEFT)
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white')
        self.endfr()

        # draw the grid
        dash = {True:'', False:'.'}
        (xmin, xmax) = (-10, 10)
        (ymin, ymax) = (-10, 10)
        for x in range(xmin, xmax+1, 1):
            self.create_line([[x, ymin], [x, ymax]], dash=dash[x==0])
        for y in range(ymin, ymax+1, 1):
            self.create_line([[xmin, y], [xmax, y]], dash=dash[y==0])

    def control_panel(self):
        self.fr(LEFT, fill=BOTH, expand=1)
        
        self.fr(TOP)
        self.bu(LEFT, text='Run', command=self.run_thread)
        self.bu(LEFT, text='Stop', command=self.stop)
        self.bu(LEFT, text='Quit', command=self.quit)
        self.endfr()

        self.fr(fill=X, expand=1)
        self.la(LEFT, text='end time')
        self.en_end = self.en(LEFT, text='10', width=5, fill=X, expand=1)
        self.la(LEFT, text='seconds')
        self.endfr()

        self.en_xoft = self.entry('x(t) = ')
        self.en_yoft = self.entry('y(t) = ')

        self.endfr()

    def entry(self, label):
        self.fr(fill=X, expand=1)
        self.la(LEFT, text=label)
        entry = self.en(LEFT, text=' t', width=5, fill=X, expand=1)
        self.endfr()
        return entry

    def run_thread(self):
        # if there is already a thread, kill it and wait for it to die
        if self.thread:
            self.running = 0
            self.thread.join()

        # find out how long to run
        end = self.en_end.get()
        end = int(end)

        # create a thread and start it
        self.thread = Thread(target=self.run, args=[end])
        self.thread.start()

    def run(self, end=10):
        self.running = 1
        start_time = time.time()
        t = 0
        while self.exists and self.running and t < end:
            for amoeba in self.animals:
                x = amoeba.xoft(t)
                y = amoeba.yoft(t)
                print 't = %.1f   x = %.1f   y = %.1f' % (t, x, y)
                amoeba.redraw(x, y)
            time.sleep(0.1)
            t = time.time() - start_time
            
    def xoft(self, t):
        return eval(self.en_xoft.get())

    def yoft(self, t):
        return eval(self.en_yoft.get())

        
class Amoeba:

    def __init__(self, world, xoft=None, yoft=None):
        self.world = world
        self.xoft = xoft or self.xoft
        self.yoft = yoft or self.yoft
        self.size = 0.5
        self.color1 = 'violet'
        self.color2 = 'medium orchid'
        world.register(self)

    def xoft(self, t):
        return t

    def yoft(self, t):
        return t

    def undraw(self):
        try:
            self.world.delete_item(self.tag)
        except AttributeError:
            pass

    def redraw(self, x, y):
        self.undraw()
        self.draw(x, y)

    def draw(self, x, y):
        thetas = range(0, 360, 30)
        self.tag = 'Amoeba%d' % id(self)

        slime = 'lavender'
        coords = self.poly_coords(x, y, thetas, self.size)
        self.world.create_polygon(coords, fill=slime, outline=slime)
        self.world.create_polygon(coords,
            fill=self.color1, outline=self.color2, tags=self.tag)

        coords = self.poly_coords(x, y, thetas, self.size/2)
        self.world.create_polygon(coords,
            fill=self.color2, outline=self.color1, tags=self.tag)

    def poly_coords(self, x, y, thetas, size):
        rs = [size+random.uniform(0, size) for theta in thetas]
        coords = [self.polar(x, y, r, theta) for (r, theta) in zip(rs, thetas)]
        return coords

    def polar(self, x, y, r, theta):
        rad = theta * pi/180
        s = sin(rad)
        c = cos(rad)
        return [ x + r * c, y + r * s ]         


class GuiAmoeba(Amoeba):

    def xoft(self, t):
        return self.world.xoft(t)

    def yoft(self, t):
        return self.world.yoft(t)


class RotateTransform(Transform):

    def __init__(self, theta):
        self.theta = theta

    def rotate(self, p, theta):
        s = sin(theta)
        c = cos(theta)
        x =   c * p[0] + s * p[1]
        y =  -s * p[0] + c * p[1]
        return [x, y]
    
    def trans(self, p):
        return self.rotate(p, self.theta)

    def invert(self, p):
        return self.rotate(p, -self.theta)


class SwirlTransform(RotateTransform):

    def trans(self, p):
        d = sqrt(p[0]*p[0] + p[1]*p[1])
        return self.rotate(p, self.theta*d)

    def invert(self, p):
        d = sqrt(p[0]*p[0] + p[1]*p[1])
        return self.rotate(p, -self.theta*d)




class TurtleWorld(World):

    def __init__(self):
        World.__init__(self)
        self.delay = 0.1           # time in seconds to sleep after an update
        self.setup()
#        self.transforms = [ SwirlTransform(pi/400),
#                            CanvasTransform(self.ca_width, self.ca_height) ]
        self.transforms = [ CanvasTransform(self.ca_width, self.ca_height) ]

    def setup(self):
        self.ca_width = 400
        self.ca_height = 400

        # left frame
        self.fr(LEFT)
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white')
        self.endfr()

        # right frame
        self.fr(LEFT, fill=BOTH, expand=1)

        self.fr()
        self.bu(LEFT, text='Make Turtle', command=self.make_turtle)
        self.bu(LEFT, text='Print Canvas', command=self.print_canvas)
        self.bu(LEFT, text='Quit', command=self.quit)
        self.endfr()

        self.fr(fill=X)
        self.bu(LEFT, text='Run File', command=self.run_file)
        self.en_file = self.en(LEFT, text='turtle_code.py', width=5,
                               fill=X, expand=1)
        self.endfr()

        self.bu(BOTTOM, text='Run Code', command=self.run_text)
        self.te_code = self.te(BOTTOM, height=10, width=40)
        self.te_code.insert(END, 'world.clear()\n')
        self.te_code.insert(END, 'bob = Turtle(world)\n')
        # leave the right frame open so that Turtles can add TurtleControls
        # self.endfr()

    def setup_run(self):
        self.fr()
        self.bu(LEFT, text='Run', command=self.run)
        self.bu(LEFT, text='Stop', command=self.stop)
        self.bu(LEFT, text='Step', command=self.step)
        self.bu(LEFT, text='Clear', command=self.clear)
        self.endfr()

    def make_turtle(self):
        turtle = Turtle(self)
        turtle.control = TurtleControl(turtle)


class TurmiteWorld(World):

    def __init__(self):
        World.__init__(self)
        self.delay = 0.0           # time in seconds to sleep after an update
        self.ca_width = 500
        self.ca_height = 500
        self.csize = 5
        self.cells = {}
        self.transforms = [ SwirlTransform(pi/400),
                           CanvasTransform(self.ca_width, self.ca_height) ]
#        self.transforms = [ CanvasTransform(self.ca_width, self.ca_height) ]
        self.setup()
        self.mainloop()

    def setup(self):

        # left frame
        self.fr(LEFT)
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white')
        self.endfr()

        # right frame
        self.fr(LEFT, fill=BOTH, expand=1)

        self.fr()
        self.bu(LEFT, text='Make Turmite', command=self.make_turmite)
        self.bu(LEFT, text='Quit', command=self.quit)
        self.endfr()

        self.fr()
        self.bu(LEFT, text='Run', command=self.run)
        self.bu(LEFT, text='Stop', command=self.stop)
        self.bu(LEFT, text='Step', command=self.step)
        self.bu(LEFT, text='Clear', command=self.clear)
        self.endfr()

        self.bu(BOTTOM, text='run this code', command=self.run_text)
        self.te_code = self.te(BOTTOM, height=20, width=40)
        self.te_code.insert(END, 't1 = Turmite(world)\n')
        self.te_code.insert(END, 't2 = Turmite(world)\n')
        self.te_code.insert(END, 't3 = Turmite(world)\n')
        self.te_code.insert(END, 't2.lt()\n')
        self.te_code.insert(END, 't3.rt()\n')
        self.te_code.insert(END, 'world.run()\n')

        # self.endfr()

        low = [-20, -20]
        high = [20, 20]
        # self.make_cells([low, high], **self.unmarked_options)

    def clear(self):
        for animal in self.animals:
            animal.undraw()
        for cell in self.cells.values():
            cell.undraw()
        self.animals = []
        self.cells = {}

    def quit(self):
        self.running = 0
        self.root.quit()

    def get_bounds(self):
        return self.trans.invert_list([[0, 0],
                                       [self.ca_width, self.ca_height]])

    def cell_bounds(self, x, y):
        p1 = [x, y]
        p2 = [x+1, y]
        p3 = [x+1, y+1]
        p4 = [x, y+1]
        bounds = [[p[0]*self.csize, p[1]*self.csize] for p in [p1, p2, p3, p4]]
        return bounds

    def make_cells(self, limits):
        low, high = limits
        for x in range(low[0], high[0]):
            col = []
            for y in range(low[1], high[1]):
                bounds = self.cell_bounds(x, y)
                self.cells[x,y] = Cell(self, bounds)

    def get_cell(self, x, y):
        x, y = int(round(x)), int(round(y))
        cell = self.cells.get((x,y), None)
        if cell==None:
            bounds = self.cell_bounds(x, y)
            cell = Cell(self, bounds)
            self.cells[x,y] = cell
        return cell

    def make_turmite(self):
        turmite = Turmite(self)

# assemble a set of keyword arguments into a dictionary
def makedict(**kwds):
    return kwds

class Cell:
    
    def __init__(self, world, bounds):
        self.world = world
        self.marked_options = makedict(fill='black', outline='gray80')
        self.unmarked_options = makedict(fill='yellow', outline='gray80')
        self.tag = world.create_polygon(bounds, **self.unmarked_options)
        self.marked = 0

    def __del__(self):
        self.undraw()

    def undraw(self):
        self.world.delete_item(self.tag)
        
    def config_cell(self, **options):
        self.world.itemconfig(self.tag, **options)

    def cget_cell(self, x, y, option):
        print self.world.itemconfig(self.tag, option)

    def mark(self):
        self.marked = 1
        self.config_cell(**self.marked_options)
        
    def unmark(self):
        self.marked = 0
        self.config_cell(**self.unmarked_options)
        
    def is_marked(self):
        return self.marked



class Interpreter:

    def __init__(self, world, globals=globals(), locals=locals()):
        self.world = world
        self.globals = globals
        self.locals = locals
        self.globals['world'] = world

    def run_code_thread(self, *args):
        Thread(target=self.run_code, args=args).start()
        
    def run_code(self, source, filename):
        code = compile(source, filename, 'exec')
        try:
            exec code in self.globals, self.locals
        except KeyboardInterrupt:
            self.world.quit




class TurtleControl:

    def __init__(self, turtle):
        self.turtle = turtle
        self.world = turtle.world
        self.objs = {}
        self.setup()
        self.tag = 'TurtleControl%d' % id(self)

    def setup(self):
        w = self.turtle.world

        self.objs['fr'] = w.fr(bd=3, relief=SUNKEN)
        self.objs['la'] = w.la(text='Turtle Control')

        # ROW 1
        self.objs['fr1'] = w.fr(fill=X, expand=1)
        self.objs['fd'] = w.bu(LEFT, text=' fd ', command=self.fd)
        self.objs['en'] = self.en_r = w.en(LEFT, X, 1, text='10', width=5)
        self.objs['lt'] = w.bu(LEFT, text='lt', command=self.turtle.lt)
        self.objs['rt'] = w.bu(LEFT, text='rt', command=self.turtle.rt)
        w.endfr()

        # ROW 2
        self.objs['fr2'] = w.fr(fill=X, expand=1)
        self.objs['pu'] = w.bu(LEFT, text='pu', command=self.turtle.pu)
        self.objs['pd'] = w.bu(LEFT, text='pd', command=self.turtle.pd)

        colors = 'red', 'orange', 'yellow', 'green', 'blue', 'violet'
        self.mb = w.mb(text=colors[0], fill=X, relief=SUNKEN)
        self.mb.pack(pady=1)
        for color in colors:
            w.mi(self.mb, color, command=Callable(self.color, color))

        for ob in self.objs.values():
            ob.pack()
        w.endfr()

        w.endfr()

    def color(self, color):
        self.mb.config(text=color)
        self.turtle.set_color(color)

    def fd(self):
        r = int(self.en_r.get())
        self.turtle.fd(r)

    def turn(self):
        theta = int(self.en_theta.get())
        self.turtle.turn(theta)

    def destroy(self):
        for ob in self.objs.values():
            ob.destroy()


class Animal:

    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 0
        self.control = None
        self.delay = 0
        
    def __del__(self):
        self.undraw()

    def step(self):
        pass

    def draw(self):
        pass

    def undraw(self):
        try:
            self.world.delete_item(self.tag)
        except AttributeError:
            pass

    def die(self):
        self.world.unregister(self)
        self.undraw()

    def redraw(self):
        self.undraw()
        self.draw()

    def update(self):
        self.world.update()
        time.sleep(self.delay)


class Turtle(Animal):

    def __init__(self, world):
        Animal.__init__(self, world)
        self.r = 5
        self.heading = 0
        self.pen = 1
        self.color = 'red'
        self.delay = 0.5
        self.draw()
        world.register(self)

    def step(self):
        self.fd()

    def polar(self, x, y, r, theta):
        rad = theta * pi/180
        s = sin(rad)
        c = cos(rad)
        return [ x + r * c, y + r * s ]         

    def draw_line(self, scale, dtheta, **options):
        r = scale * self.r
        theta = self.heading + dtheta
        head = self.polar(self.x, self.y, r, theta)
        tail = self.polar(self.x, self.y, -r, theta)
        self.world.create_line([tail, head], **options)

    def draw(self):
        self.tag = 'Turtle%d' % id(self)
        lw = self.r/2
        self.draw_line(2.5, 0, tags=self.tag, width=lw, arrow=LAST)
        self.draw_line(2.5, 0, tags=self.tag, width=lw, arrow=FIRST)
        self.draw_line(1.8, 40, tags=self.tag, width=lw)
        self.draw_line(1.8, -40, tags=self.tag, width=lw)
        self.world.create_circle(self.x, self.y, self.r, self.color,
                                 tags=self.tag)
        self.update()

    def fd(self, r=1):
        x = self.x
        y = self.y
        p1 = [x, y]
        p2 = self.polar(x, y, r, self.heading)
        self.x = p2[0]
        self.y = p2[1]
        if (self.pen):
            self.world.create_line([p1, p2], fill='black')
        self.redraw()

    def bk(self, r=1):
        self.fd(-r)

    def rt(self, angle=90):
        self.heading = self.heading - angle
        self.redraw()

    def lt(self, angle=90):
        self.heading = self.heading + angle
        self.redraw()

    def pd(self):
        self.pen = 1

    def pu(self):
        self.pen = 0

    def set_color(self, color):
        self.color = color
        self.redraw()


class Turmite(Animal):

    def __init__(self, world):
        Animal.__init__(self, world)
        self.dir = 0
        # have to draw yourself before registering!
        self.draw()
        world.register(self)


    def draw(self):
        bounds = world.cell_bounds(self.x, self.y)
        bounds = rotate(bounds, self.dir)
        mid = vmid(bounds[1], bounds[2])
        self.tag = self.world.create_polygon([bounds[0], mid, bounds[3]],
                               fill='red')

    def fd(self, r=1):
        if self.dir==0:
            self.x += r
        elif self.dir==1:
            self.y += r
        elif self.dir==2:
            self.x -= r
        else:
            self.y -=r
        self.redraw()

    def bk(self, r=1):
        self.fd(-r)

    def rt(self):
        self.dir = (self.dir-1) % 4

    def lt(self):
        self.dir = (self.dir+1) % 4

    def get_cell(self):
        return self.world.get_cell(self.x, self.y)
        
    def mark(self):
        cell = self.get_cell()
        cell.mark()

    def unmark(self):
        cell = self.get_cell()
        cell.unmark()

    def toggle(self):
        if self.is_on_mark():
            self.unmark()
        else:
            self.mark()

    def is_on_mark(self):
        cell = self.get_cell()
        return cell.is_marked()

    def step(self):
        if self.is_on_mark():
            self.lt()
        else:
            self.rt()
        self.toggle()
        self.fd()


# the following are some random linear-algebra utilities
# written as functions (not methods)

def vadd(p1, p2):
    return [x+y for x,y in zip(p1, p2)]

def vscale(p, s):
    return [x*s for x in p]

def vmid(p1, p2):
    return vscale(vadd(p1, p2), 0.5)

def rotate(v, n=1):
    n %= len(v)
    return v[n:] + v[:n]

# add the turtle functions to the global dictionary
# so they can be invoked as simple functions (not methods)
fd = Turtle.fd
bk = Turtle.bk
lt = Turtle.lt
rt = Turtle.rt
pu = Turtle.pu
pd = Turtle.pd
die = Turtle.die
set_color = Turtle.set_color

# top_globals and top_locals are used to create the
# Interpreter that executes user-provided code.
# It is necessary
# to provide a top-level environment so that user-
# defined functions are top-level functions

top_globals = globals()
top_locals = locals()

if __name__ == '__main__':
    world = TurtleWorld()
    world.mainloop()
