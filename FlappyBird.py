import pygame
import random


pygame.init()

window_width = 800  # window width
window_height = 700  # window height


# bird class
class Bird(object):
    def __init__(self, x, y, width, height):
        self.x = x  # x position
        self.y = y  # y position
        self.width = width  # bird's width
        self.height = height  # bird's height
        self.vel = 15  # bird's falling speed
        self.jumpcount = 10  # control how high the bird jump every time
        self.jump = False  # jump status

    def draw(self, window):
        """draw the bird on the screen"""
        pygame.draw.rect(window, (255, 255, 255), (self.x, self.y, self.width, self.height))


# block class
class Block(object):
    def __init__(self, x, up_height, color):
        self.x = x  # x location
        self.up_height = up_height  # the height of block at the top
        self.vel = 5  # block's moving velocity
        self.color = color  # block's color

    def draw(self, window):
        """draw the blocks on the screen"""
        # draw the upper block
        pygame.draw.rect(window, self.color, (self.x, 0, 50, self.up_height))
        # draw the bottom block
        pygame.draw.rect(window, self.color, (self.x, self.up_height + 128, 50, window_height - self.up_height - 128))


def update_score(newscore):  # update the score
    """update the top score and write it into a txt file"""
    score = max_score()  # read the max score
    with open('scores.txt', 'w') as f:
        if newscore > int(score):  # if break the record
            f.write(str(newscore))  # write the new score
        else:
            f.write(str(score))  # write the origin score


def max_score():
    """read the top score from a txt file"""
    with open('scores.txt', 'r') as f:
        lines = f.readlines(0)  # read all the lines
        score = lines[0].strip()  # get the first line
    return score


def draw_lost(window):
    """draw the sentence "YOU LOST!" when you lost the game"""
    lostfont = pygame.font.SysFont('comicsans', 80, bold=True)  # define the font and size
    label = lostfont.render('YOU LOST!', 1, (255, 255, 255))  # define the contant and the color
    x = (window_width - label.get_width())/2  # define the x location of this sentence
    y = (window_height - label.get_height())/2  # definr the y location of this sentence
    window.blit(label, (x, y))  # show this on the screen


def overlap(l1, r1, l2, r2):
    """check if two rectangles are overlapped"""
    if l1[0] > r2[0] or l2[0] > r1[0]:
        return False
    if l1[1] > r2[1] or l2[1] > r1[1]:
        return False
    return True


def check_blocked(player, blocks):
    """check if the bird is blocked by any of the blocks"""
    for block in blocks:  # for every block
        if overlap((block.x, 0), (block.x + 50, block.up_height),
                   (player.x, player.y), (player.x + 32, player.y + 32)):  # check if bird overlap with the upper block
            return True
        if overlap((block.x, block.up_height + 128), (block.x + 50, window_height),
                   (player.x, player.y), (player.x + 32, player.y + 32)):  # check if bird overlap with the bottom block
            return True
    return False


def check_lost(player, blocks):
    """check if you lost the game"""
    if player.y > window_height - player.height:  # if the bird touched the bottom, then you loss
        return True
    return check_blocked(player, blocks)  # check if the bird get blocked by the blocks


def draw_win(window, player, myscore, mybest, blocks):
    """draw the whole window"""
    window.fill((0, 0, 0))  # background color -> black
    for block in blocks:
        block.draw(window)  # draw the blocks
    myfont = pygame.font.SysFont('comicsans', 30, True)  # define a new font
    if myscore < 0:  # if the score is less than 0, set it to 0
        myscore = 0
    score = myfont.render('Score: ' + str(myscore), 1, (255, 255, 255))  # display the score
    best = myfont.render('Best: ' + str(mybest), 1, (255, 255, 255))  # display the best score
    window.blit(score, (350, 10))  # display location
    window.blit(best, (350, 30))  # display location
    player.draw(window)  # draw the player
    pygame.display.update()  # updata the window


def main(window):
    """main loop of the game"""
    run = True
    bird_size = 32  # image's size
    player = Bird(window_width/4 - bird_size/2, window_height/2 - bird_size/2, bird_size, bird_size)  # define the player
    blocks = []  # to store all the blocks
    score = -5  # score initial it to -5
    best = int(max_score())  # the best score

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:  # when a key is pressed
                if event.key == pygame.K_SPACE:  # when space is pressed
                    player.jump = True  # the bird need jump

        # if there is no block or the newest block is at location 450, we need a newblock
        if not blocks or blocks[-1].x < 450:
            blocks.append(Block(window_width, random.randint(100, 400), (0, 128, 0)))

        # move every block by its speed, if the block is outside the screen, we remove it
        for block in blocks:
            block.x -= block.vel
            if block.x <= -400:  # if the block is outside the screen
                blocks.pop(blocks.index(block))  # remove then block

        #  implement the jump action
        if player.jump:  # if jump
            player.y -= 35  # jump up by 35
            player.jump = False  # jump status set to false
        else:  # if not jump
            player.y += player.vel  # move down by its speed

        # add 5 to the score when you pass a block completely
        if blocks[-1].x == 465:
            score += 5

        # check is you loss then game or not
        if check_lost(player, blocks):  # if you loss
            draw_lost(window)  # display the sentence "YOU LOST!"
            pygame.display.update()  # update the screen
            pygame.time.delay(1500)  # wait for 1.5 second
            run = False  # quit the main loop
            update_score(score)  # update the score
        else:  # if you not loss
            draw_win(window, player, score, best, blocks)  # draw the window


def main_menu(window):
    """this is a window as a welcom window"""
    run = True
    while run:
        window.fill((0, 0, 0))  # background color -> black
        startfont = pygame.font.SysFont('comicsans', 60, True)  # initial the font
        label1 = startfont.render('Welcome to Flappy Bird', 1, (255, 255, 255))  # the sentence and color
        label2 = startfont.render('By Yutao Chen', 1, (255, 255, 255))  # the sentence and color
        label3 = startfont.render('Press Any Key To Play!', 1, (255, 255, 255))  # the sentence and color
        # display the sentence on the screen
        window.blit(label1, ((window_width - label1.get_width())/2, (window_height/2 - label1.get_height()-25)))
        window.blit(label2, ((window_width - label2.get_width())/2, (window_height - label2.get_height())/2))
        window.blit(label3, ((window_width - label3.get_width())/2, (window_height + label3.get_height())/2))
        pygame.display.update()  # update the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit
                run = False
            if event.type == pygame.KEYDOWN:  # if any key is pressed, start the game
                main(window)  # main loop of the game

    pygame.display.quit()  # quit the game


surface = pygame.display.set_mode((window_width, window_height))  # initial the window
pygame.display.set_caption('Flappy Bird')  # the title of the game
main_menu(surface)  # call the function and start the game
