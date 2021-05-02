import pygame

class button():
    def __init__(self, color, x, y, width, height, text='',r= 60,img= None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.r= r
        self.img= img
    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline and self.img is None:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        if self.img is None:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '' and self.img is None:
            font = pygame.font.SysFont('comicsans', self.r)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
        if self.img is not None:
            win.blit(self.img,(self.x,self.y))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def isclicked(self):
        if self.isOver(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]==1:
                return True