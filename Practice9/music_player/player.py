import pygame
import os
import sys

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("Music Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
BLUE = (100, 149, 237)

font1 = pygame.font.SysFont("Arial", 32, bold=True)
font2 = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

base = os.path.dirname(__file__)
music_folder = os.path.join(base, "music")

playlist = []
for name in os.listdir(music_folder):
    if name.endswith(".mp3") or name.endswith(".wav"):
        playlist.append(name)

playlist.sort()

cur = 0
playing = False
paused = False
msg = ""


def textt(txt, font, color, x, y):
    img = font.render(txt, True, color)
    screen.blit(img, (x, y))


def timm(sec):
    mm = sec // 60
    ss = sec % 60
    return f"{mm:02}:{ss:02}"


def playy():
    global playing, paused, msg

    if not playlist:
        msg = "No music files"
        return

    path = os.path.join(music_folder, playlist[cur])

    try:
        if paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

        playing = True
        paused = False
        msg = "Playing now"
    except pygame.error:
        playing = False
        paused = False
        msg = "Unsupported audio format"


def pausee():
    global playing, paused, msg
    pygame.mixer.music.pause()
    playing = False
    paused = True
    msg = "Paused"


def stopp():
    global playing, paused, msg
    pygame.mixer.music.stop()
    playing = False
    paused = False
    msg = "Stopped"


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            ch = event.unicode.lower()

            if ch == "q" or ch == "й":
                run = False

            elif ch == "p" or ch == "з":
                if playing:
                    pausee()
                else:
                    playy()

            elif ch == "s" or ch == "ы":
                stopp()

            elif ch == "n" or ch == "т":
                if playlist:
                    cur += 1
                    if cur == len(playlist):
                        cur = 0
                    playy()

            elif ch == "b" or ch == "и":
                if playlist:
                    cur -= 1
                    if cur < 0:
                        cur = len(playlist) - 1
                    playy()

    screen.fill(WHITE)

    textt("Music Player", font1, BLUE, 240, 50)

    if playlist:
        textt("Track: " + playlist[cur], font2, BLACK, 60, 130)
    else:
        textt("Track: No music", font2, BLACK, 60, 130)

    if playing:
        status = "Playing"
        color = GREEN
    elif paused:
        status = "Paused"
        color = BLUE
    else:
        status = "Stopped"
        color = RED

    textt("Status: " + status, font2, color, 60, 180)

    pos = pygame.mixer.music.get_pos() // 1000
    if pos < 0:
        pos = 0
    textt("Position: " + timm(pos), font2, BLACK, 60, 230)

    textt("Message: " + msg, font2, RED, 60, 270)
    textt("P/З-play  S/Ы-stop  N/Т-next  B/И-back  Q/Й-quit", font2, BLACK, 60, 320)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()