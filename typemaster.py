import pygame
import random
import copy
from nltk.corpus import words
import nltk
nltk.download('words')

pygame.init()

# Prepare word list from NLTK
wordlist = words.words()
len_indexes = []
length = 1

wordlist.sort(key=len)

# Prepare indexes based on word length
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)

len_indexes.append(len(wordlist))

# Game window settings
W = 800
H = 600
screen = pygame.display.set_mode([W, H])
pygame.display.set_caption("TYPING MASTER !")
surface = pygame.Surface((W, H), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

# Game variables
level = 1
active = ''
score = 0
live = 5
paused = True
submit = ''
word = []
letters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]
newlevel = True
chioses = [False, True, False, False, False, False, False]

# Fonts
headf = pygame.font.Font('digital-7.ttf', 50)
pausef = pygame.font.Font('digital-7.ttf', 38)
banf = pygame.font.Font('digital-7.ttf', 28)
font = pygame.font.Font('digital-7.ttf', 48)


# Audio setup
pygame.mixer.init()

# Background music
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Sound effects
click_sound = pygame.mixer.Sound('cick.mp3')
woosh_sound = pygame.mixer.Sound('swosh.mp3')
wrong_sound = pygame.mixer.Sound('error.mp3')

# Adjust sound effect volumes
click_sound.set_volume(0.3)
woosh_sound.set_volume(0.3)
wrong_sound.set_volume(0.5)

# Load high score
try:
    with open('high.txt', 'r') as file:
        best = int(file.read().strip())
except (ValueError, FileNotFoundError):
    best = 0

# Word class to represent each word
class Word:
    def __init__(self, text, speed, y, x):
        self.x = x
        self.y = y
        self.text = text
        self.speed = speed

    def draw(self):
        col = 'black'
        screen.blit(font.render(self.text, True, col), (self.x, self.y))
        actlen = len(active)
        if active == self.text[:actlen]:
            screen.blit(font.render(active, True, 'green'), (self.x, self.y))

    def update(self):
        self.x -= self.speed

# Button class for UI
class Button:
    def __init__(self, x, y, text, click, surf, font_size=38):
        self.x = x
        self.y = y
        self.text = text
        self.click = click
        self.surf = surf
        self.font = pygame.font.Font('digital-7.ttf', font_size)  # Allow font size customization

    def draw(self):
        # Draw the circle
        c = pygame.draw.circle(self.surf, ('blue'), (self.x, self.y), 35)
        
        # Detect mouse hover and clicks
        if c.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x, self.y), 35)
                self.click = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x, self.y), 35)
        
        # Draw the circle outline
        pygame.draw.circle(self.surf, ('white'), (self.x, self.y), 35.3)

        # Render the text and calculate its position
        text_surface = self.font.render(self.text, True, "black")
        text_rect = text_surface.get_rect(center=(self.x, self.y))  # Center the text

        # Blit the text onto the surface
        self.surf.blit(text_surface, text_rect)


# Function to draw static UI elements
def draws():
    pygame.draw.rect(screen, ('#030424'), [0, H - 100, W, 100])
    pygame.draw.rect(screen, 'white', [0, 0, W, H], 5)
    pygame.draw.line(screen, 'white', (250, H - 100), (250, H), 2)
    pygame.draw.line(screen, 'white', (700, H - 100), (700, H), 2)
    pygame.draw.line(screen, 'white', (0, H - 100), (W, H - 100), 2)
    pygame.draw.rect(screen, 'black', [0, 0, W, H], 2)

    screen.blit(headf.render(f' Level : {level}', True, 'white'), (10, H - 75))
    screen.blit(headf.render(f' "{active}"', True, 'white'), (270, H - 75))
    screen.blit(banf.render(f' Score : {score}', True, 'Black'), (250, 10))
    screen.blit(banf.render(f' Best : {best}', True, 'Black'), (550, 10))
    screen.blit(banf.render(f' Lives : {live}', True, 'Black'), (10, 10))
    pause = Button(748, H-52, '| |', False, screen,45)
    pause.draw()

    return pause.click

def drawp():
    srface = pygame.Surface((W, H), pygame.SRCALPHA)
    pygame.draw.rect(srface, (0, 0, 0, 100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(srface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)
    resbut = Button(160, 200, '>', False, srface,45)
    resbut.draw()
    quitbut = Button(410, 200, 'X', False, srface,45)
    quitbut.draw()

    srface.blit(headf.render('Menu', True, 'white'), (110, 110))
    srface.blit(headf.render('PLAY!', True, 'white'), (210, 170))
    srface.blit(headf.render('QUIT', True, 'white'), (450, 170))
    srface.blit(headf.render('Active letter lengths:', True, 'white'), (110, 250))

    for i in range(len(chioses)):
        btn = Button(160 + (i * 80), 350, str(i + 2), False, srface)
        btn.draw()
        if btn.click:
            chioses[i] = not chioses[i]

        if chioses[i]:
            pygame.draw.circle(srface, 'green', (160 + (i * 80), 350), 35, 5)
    screen.blit(srface, (0, 0))
    return resbut.click, quitbut.click

# Function to generate new level
def genlevel():
    wordobj = []
    include = []
    verspace = max((H - 150) // max(level, 1), 1)  # Ensure at least 1-pixel spacing

    if True not in chioses:
        chioses[0] = True

    for i in range(len(chioses)):
        if chioses[i]:
            include.append((len_indexes[i], len_indexes[i + 1]))  # Slice the indexes by length

    for i in range(level):
        speed = random.randint(2, 3)
        y_min = 10 + (i * verspace)
        y_max = y_min + verspace - 10

        # Ensure the range is valid
        if y_min >= H - 150:
            y_min = H - 160  # Adjust to stay within bounds
        if y_max > H - 150:
            y_max = H - 150
        if y_min > y_max:
            y_min, y_max = y_max, y_min  # Swap to ensure a valid range

        y = random.randint(y_min, y_max) if y_min <= y_max else H - 150
        x = random.randint(W, W + 1000)
        indsel = random.choice(include)
        index = random.randint(indsel[0], indsel[1])
        text = wordlist[index].lower()
        newword = Word(text, speed, y, x)
        wordobj.append(newword)

    return wordobj


# Function to check and update best score
def checkbest():
    global best
    if score > best:
        best = score
        with open('high.txt', 'w') as file:
            file.write(str(best))

# Function to check if the word is correctly typed and update score
def checka(scor):
    global word
    for wrd in word:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 3)
            scor += int(points)
            word.remove(wrd)
            woosh_sound.play()
    return scor

# Game Loop
run = True
while run:
    screen.fill('light gray')
    timer.tick(fps)

    pauseb = draws()

    if paused:
        resbut, quitbut = drawp()
        if resbut:
            paused = False
        if quitbut:
            checkbest()
            run = False
    elif newlevel and not paused:
        word = genlevel()
        newlevel = False
    else:
        for w in word:
            w.draw()
            if not paused:
                w.update()
            if w.x < -200:
                word.remove(w)
                live -= 1

    if len(word) <= 0 and not paused:
        level += 1
        newlevel = True

    if submit != '':
        init = score
        score = checka(score)
        submit = ''
        if init==score:
            wrong_sound.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            checkbest()
            run = False

        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letters:
                    active += event.unicode.lower()
                    click_sound.play()
                if event.key == pygame.K_BACKSPACE and len(active) > 0:
                    active = active[:-1]
                    click_sound.play()
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    submit = active
                    active = ""
            if event.key == pygame.K_ESCAPE:
                paused = not paused

    if pauseb:
        paused = True

    if live < 0:
        paused = True
        level = 1
        live = 5
        word = []
        newlevel = True
        checkbest()
        score = 0

    pygame.display.flip()

pygame.quit()
