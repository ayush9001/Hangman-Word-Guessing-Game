import pygame
import sys
import os

pygame.init()

if getattr( sys, 'frozen', False ) :
    # running in a bundle (.exe)
    main_file = sys.executable
else :
    # running live (.py)
    main_file = __file__

def loadImage(image_path,size=(None,None)): #image_path is location of image file withing Game/data folder.
    path = os.path.dirname(main_file)
    img = pygame.image.load(os.path.join(path,"data/"+image_path))
    if size!=(None,None):
        img = pygame.transform.scale(img,size)
    else:
        pass
    return img



class Checkbox:
    def __init__(self, surface, x, y, length=25):
        self.surface = surface
        self.x = x
        self.y = y
        self.l = length
        # variables to test the different states of the checkbox
        self.checked = False
        self.active = False
        self.unchecked = True
        self.click = False
        self.obj_c = loadImage("checkbox_green.png",(self.l,self.l))
        self.obj_u = loadImage("blankbox_blue.png",(self.l,self.l))
        self.obj_uh = loadImage("blankbox_green.png",(self.l,self.l))
        
    def render_checkbox(self):
        if self.checked:
            self.surface.blit(self.obj_c,(self.x,self.y))

        elif self.unchecked:
            if self.active:
                self.surface.blit(self.obj_uh,(self.x,self.y))
            else:
                self.surface.blit(self.obj_u,(self.x,self.y))

            
    def _update(self, event_object):
        x, y = event_object.pos
        # self.x, self.y, self.l, self.l
        px, py, w, h = self.x,self.y,self.l,self.l  # getting check box dimensions
        if px < x < px + w and py < y < py + h:
            self.active = True
        else:
            self.active = False

    def _mouse_up(self):
            if self.active and not self.checked and self.click:
                    self.checked = True
                    self.unchecked = False
            elif self.checked and self.active:
                self.checked = False
                self.unchecked = True

            if self.click is True and self.active is False:
                if self.checked:
                    self.checked = True
                    self.unchecked = False
                if self.unchecked:
                    self.unchecked = True
                self.active = False

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            # self._mouse_down()
        if event_object.type == pygame.MOUSEBUTTONUP:
            self._mouse_up()
            self.click = False
        if event_object.type == pygame.MOUSEMOTION:
            self._update(event_object)

    def is_checked(self):
        if self.checked is True:
            return True
        else:
            return False

    def is_unchecked(self):
        if self.checked is False:
            return True
        else:
            return False
