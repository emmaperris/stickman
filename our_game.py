from tkinter import *
import random
import time
from platform_sprite import PlatformSprite
from sprite import Sprite
from coords import Coords
from moving_platform_sprite import MovingPlatformSprite
from door_sprite import DoorSprite

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Mr. Stick Man Races for the Exit")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, \
                highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file="./stickman/background.gif")
        self.bg2 = PhotoImage(file="./stickman/background2.gif")
        w = self.bg.width()
        h = self.bg.height()
        w2 = self.bg2.width()
        h2 = self.bg2.height()

        for x in range (0, 5):
            for y in range(0, 5):
                if (x+y) % 2 != 0:
                    self.canvas.create_image(x * w, y * h, \
                            image=self.bg, anchor='nw')
                else:
                    self.canvas.create_image(x * w2, y * h2, \
                            image=self.bg2, anchor='nw')
                    
        self.sprites = []
        self.running = True 

    def mainloop(self):
        while True:
            if self.running:
                for sprite in self.sprites:
                    sprite.move()

            self.tk.update_idletasks()
            self.tk.update()

            time.sleep(0.01)

            if sf.endgame == True:
                you_win()
                break

def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
        or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
        or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
        or (co2.x2 > co1.x1 and co2.x2 < co1.x1):
        return True
    else:
        return False
        
def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
        or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
        or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
        or (co2.y2 > co1.y1 and co2.y2 < co1.y1):
        return True
    else:
        return False
        
def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            print(f"Collision left detected: {co1.x1}, {co2.x1}, {co2.x2}")
            return True
    return False

def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            print(f"Collision right detected: {co1.x2}, {co2.x1}, {co2.x2}")
            return True
    return False

def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False


class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="./stickman/Figure-L1.gif"),
            PhotoImage(file="./stickman/Figure-L2.gif"),
            PhotoImage(file="./stickman/Figure-L3.gif")
        ]
        self.images_right = [
            PhotoImage(file="./stickman/Figure-R1.gif"),
            PhotoImage(file="./stickman/Figure-R2.gif"),
            PhotoImage(file="./stickman/Figure-R3.gif")
        ]
        self.image = game.canvas.create_image(200, 470, \
                image=self.images_left[0], anchor='nw')
        self.x = 0
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyRelease-Left>', self.stop_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<KeyRelease-Right>', self.stop_right)
        game.canvas.bind_all('<space>', self.jump)
        self.endgame = False

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -1.5

    def stop_left(self, evt):
        if self.x == -1.5:
            self.x = 0

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 1.5

    def stop_right(self, evt):
        if self.x == 1.5:
            self.x = 0

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0
    
    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_right[self.current_image])
                
    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates
    
    def move(self):
        self.animate() 
    
        for sprite in self.game.sprites:
            if isinstance(sprite, DoorSprite):
                door_coords = sprite.coords()
                if collided_left(self.coords(), door_coords) or collided_right(self.coords(), door_coords):
                    # Open the door.

                    # Make a PhotoImage instance.
                    open_door_image = PhotoImage(file="./stickman/door-opened.gif")
                    
                    # Create a image on the canvas.
                    open_door = DoorSprite(g, open_door_image, 45, 30, 40, 35)
                    g.sprites.append(open_door)

                    self.endgame = True
                    g.canvas.delete(sf)
                    break

        if self.y < 0: 
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4 
        if self.y > 0:  
            self.jump_count -= 1

        co = self.coords()
    
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0  
            bottom = False

        elif self.y < 0 and co.y1 <= 0:
            self.y = 0  
            top = False 

        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0  
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0  
            left = False

        for sprite in self.game.sprites:
            if sprite == self:  
                continue

            sprite_co = sprite.coords()
        
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y  
                top = False  

            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2  
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False

            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(1, co, sprite_co):
                falling = False  
                if left and self.x < 0 and collided_left(co, sprite_co):
                    self.x = 0  
                    left = False
                    if sprite.endgame:
                        self.game.running = False
                if right and self.x > 0 and collided_right(co, sprite_co):
                    self.x = 0  
                    right = False
                    self.game.running = False
        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = 4  

        self.game.canvas.move(self.image, self.x, self.y)

def you_win():

    g.canvas.create_text(250, 250, text='YOU WIN!!!',
    font=('Times', 22))
    g.tk.update()
    time.sleep(2)
    g.tk.quit()


g = Game()

platform1 = PlatformSprite(g, PhotoImage(file="./stickman/platform3.gif"), \
    0, 480, 100, 10)
platform2 = PlatformSprite(g, PhotoImage(file="./stickman/platform3.gif"), \
    150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file="./stickman/platform3.gif"), \
    300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file="./stickman/platform3.gif"), \
    300, 160, 100, 10)
platform5 = PlatformSprite(g, PhotoImage(file="./stickman/platform2.gif"), \
    175, 350, 66, 10)
platform6 = MovingPlatformSprite(g, PhotoImage(file="./stickman/platform2.gif"), \
    50, 300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file="./stickman/platform2.gif"), \
    170, 120, 66, 10)
platform8 = PlatformSprite(g, PhotoImage(file="./stickman/platform2.gif"), \
    45, 60, 66, 10)
platform9 = PlatformSprite(g, PhotoImage(file="./stickman/platform1.gif"), \
    170, 250, 32, 10)
platform10 = PlatformSprite(g, PhotoImage(file="./stickman/platform1.gif"), \
    230, 200, 32, 10)

g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
door = DoorSprite(g, PhotoImage(file="./stickman/door-closed.gif"), 45, 30, 40, 35)
g.sprites.append(door)
sf = StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()