import pygame
import os
import random

pygame.init()

#window size
WIDTH, HEIGHT = 500, 700
#game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#title
pygame.display.set_caption("Pink Flappy Bird ")

WHITE = (255, 255, 255) 
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FPS = 60
GRAVITY = 0.5  #makes bird fall downwards
FLAP_STRENGTH = -10 #moves the bird upwards when you press SPACE bar
PIPE_VELOCITY = 3 #pipes move to the left 
GAP_HEIGHT = 200 #space between the top and bottom pipes

#load assets
PINK_BIRDY = pygame.image.load("assets_a5/frame-1.png")
PIPE_IMAGE = pygame.image.load("assets_a5/pipe.png")
BACKGROUND = pygame.image.load("assets_a5/sky.png")

#scale the images
PINK_BIRDY = pygame.transform.scale(PINK_BIRDY, (50, 40))
PIPE_IMAGE = pygame.transform.scale(PIPE_IMAGE, (70, 400))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

#font for text on screen
FONT = pygame.font.SysFont("resistmono", 40)

class Bird:
    def __init__(self, x, y):
        self.image = PINK_BIRDY
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 0 #0 at start, will increase due to gravity
    
    def flap(self):
        self.velocity = FLAP_STRENGTH #when space bar is pressed, velocity is set to a negative value, making the bird jump
    
    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity # increase velocity each frame
    
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Pipe:
    def __init__(self, x):
        self.gap_y = random.randint(150, HEIGHT - 250) #pipe height randomized
        self.top_rect = PIPE_IMAGE.get_rect(topleft=(x, self.gap_y - 400)) #starts above the gap
        self.bottom_rect = PIPE_IMAGE.get_rect(topleft=(x, self.gap_y + GAP_HEIGHT)) #starts below the gap
    
    def update(self):
        self.top_rect.x -= PIPE_VELOCITY
        self.bottom_rect.x -= PIPE_VELOCITY #moves pipes to the left
    
    def draw(self, window):
        window.blit(PIPE_IMAGE, (self.top_rect.x, self.top_rect.y)) #draws the top pipe normally
        window.blit(pygame.transform.flip(PIPE_IMAGE, False, True), (self.bottom_rect.x, self.bottom_rect.y)) #flips the bottom pipe vertically
    
    def off_screen(self):
        return self.top_rect.x < -PIPE_IMAGE.get_width() #returns True if the pipe has moved off the screen

def draw_window(bird, pipes, score):
    WIN.blit(BACKGROUND, (0, 0))
    bird.draw(WIN)
    for pipe in pipes:
        pipe.draw(WIN)
    
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    WIN.blit(score_text, (20, 20))
    pygame.display.update()

def main():
    bird = Bird(100, HEIGHT//2)
    pipes = [Pipe(WIDTH)]
    score = 0
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS)
        
#pressing space makes the bird jump
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                if event.key == pygame.K_s:  #press 'S' to take a screenshot
                    pygame.image.save(WIN, "flappy_screenshot.png")
                    print("Screenshot saved as flappy_screenshot.png")
        
        bird.update()
        
#new pipe is created when the last one reaches a certain distance
        if pipes[-1].top_rect.x < WIDTH - 200:
            pipes.append(Pipe(WIDTH))

#moves pipes and removies off-screen ones
        for pipe in pipes[:]:
            pipe.update()
            if pipe.off_screen():
                pipes.remove(pipe)
                score += 1 #increases the score when a pipe is passed.
            
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect) or bird.rect.y >= HEIGHT:
                run = False #ends the game if the bird hits a pipe or the ground
        
        draw_window(bird, pipes, score)
    
    pygame.quit()

#start screen before the game
def start_screen():
    WIN.fill(WHITE)
    text = FONT.render("Press SPACE to Start", True, BLUE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
    main()

if __name__ == "__main__":
    start_screen()
