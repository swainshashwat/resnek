import time
import random
import pygame
from pygame.locals import *

# Global window Size
pix = 32
winWd = 20
winHt = 20

direction_key = {
    'right' : 0,
    'left' : 1,
    'up' : 2,
    'down' : 3
}

class Apple:
    x = 1*pix
    y = 2*pix

    def __init__(self):
        pass
    
    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))
    
    def relocate_apple(self, player_space):

        self.x = random.randint(0, winWd-1)*pix
        self.y = random.randint(0, winHt-1)*pix

        while (self.x,self.y) in player_space:
            self.x = random.randint(0, winWd-1)*pix
            self.y = random.randint(0, winHt-1)*pix

class Player:
    x = []
    y = []
    step = pix
    direction = 0
    length = 3

    player_space = []

    def __init__(self, length):
        self.length = length
        self.x.append(0)
        self.y.append(0)
        for i in range(1000):
            self.x.append(-100)
            self.y.append(-100)
        
    
    def update(self):
      
        self.player_space = []
        # update previous positions
        for i in range(self.length-1, 0, -1):
            self.player_space.append((self.x[i], self.y[i]))
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update position of head of snake
        if self.direction == 0: # right
            self.x[0] = self.x[0] + self.step
        if self.direction == 1: # left
            self.x[0] = self.x[0] - self.step
        if self.direction == 2: # up
            self.y[0] = self.y[0] - self.step
        if self.direction == 3: # down
            self.y[0] = self.y[0] + self.step
        
        self.player_space.append((self.x[0], self.y[0]))

        self.updateCount = 0


    def moveRight(self):
        self.direction = 0
    
    def moveLeft(self):
        self.direction = 1
    
    def moveUp(self):
        self.direction = 2
    
    def moveDown(self):
        self.direction = 3

    def draw(self, surface, head, skin):
        # drawing head image with head direction
        angle = 0
        if self.direction==0:
            angle = -90
        elif self.direction==1:
            angle = 90
        elif self.direction==3:
            angle = 180
        else:
            pass
            
        head = pygame.transform.rotate(head, angle)
        surface.blit(head, (self.x[0], self.y[0]))
        
        # drawing skin image
        for i in range(1, self.length):
            surface.blit(skin, (self.x[i], self.y[i]))

class Game:
    
    def __init__(self):
        '''
        Class that defines Game Rules
        '''
        # Points
        score = 0

        # initializing rewards
        eat_fruit = 0.8
        go_near_fruit = 0.1
        go_away_from_fruit = -0.2
        dying = -1.0

    def eatsApple(self, pos1, pos2):
        '''
        Check if player eats apple
        '''
        if pos1 == pos2:
                return True
        return False
    
    def eatsSelf(self, player_space):
        '''
        Check if player eat's own body
        '''
        player_head = player_space[-1]
        if player_head in player_space[:-1]:
            return True
        return False
    
    def crashWall(self, player_head, dim):
        '''
        Check if wall is crashed
        '''
        if not (0<=player_head[0]<dim[0] and 0<=player_head[1]<dim[1]):
            return True
        return False

    def dist_from_object(self, player_head, obj):
        '''
        Returns Normalized distance between the player and the head
        '''
        pass



class App:
    windowWidth = winWd*pix
    windowHeight = winHt*pix
    player = 0
    apple = 0

    def __init__(self):
        '''
        Main Game Application
        '''
        self._running = True
        # display image surface
        self._display_surf = None

        # player image surface
        self._head_surf = None
        self._skin_surf = None

        # apple image surface
        self._apple_surf = None

        # initializing classes
        self.player = Player(1)
        self.apple = Apple()
        self.game = Game()
    
    def on_init(self):
        '''
        Initializing Game Variables and Image surfaces
        '''
        pygame.init()
        self._display_surf = pygame.display.set_mode(
                            (self.windowWidth, self.windowHeight),
                            pygame.HWSURFACE)
        pygame.display.set_caption('Reinforcement Snek Game')

        self._running = True

        # load player image
        self._head_surf = pygame.image.load('head.png').convert()
        self._skin_surf = pygame.image.load('skin.png').convert()
        
        # load apple image
        self._apple_surf = pygame.image.load('apple.png').convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        
    def on_loop(self):
        self.player.update()
        player_head = (self.player.x[0], self.player.y[0])

        # snake eats apple
        if self.game.eatsApple(player_head , (self.apple.x, self.apple.y)):
            
            print("REWARD : Eats Apple")            
            self.player.length +=  1
            self.apple.relocate_apple(self.player.player_space)
            return True
        
        # snake eats itself
        if self.game.eatsSelf(self.player.player_space):
            print("PUNISH : Eats Self")
            return False

        # snake crashes with in the wall
        if self.game.crashWall(player_head, (self.windowWidth, self.windowHeight)):
            print("PUNISH : Wall Crash")
            return False

        return True


    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf,
                        self._head_surf, self._skin_surf )
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
    
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while(self._running):
            pygame.event.pump()

            # game controls
            keys = pygame.key.get_pressed()

            # while going in a direction, can't go in the opposite direction
            if keys[K_RIGHT] and self.player.direction != direction_key['left']:
                self.player.moveRight()
            if keys[K_LEFT] and self.player.direction != direction_key['right']:
                self.player.moveLeft()
            if keys[K_UP] and self.player.direction != direction_key['down']:
                self.player.moveUp()
            if keys[K_DOWN] and self.player.direction != direction_key['up']:
                self.player.moveDown()
            if keys[K_ESCAPE]:
                self._running = False
            if keys[K_r]:
                None

            # check conditions in loop
            if not self.on_loop():
                break

            # render with updated values
            self.on_render()

            time.sleep(0.1)
        
        self.on_cleanup()

if __name__=='__main__':
    
    snek = App()
    snek.on_execute()
            
            