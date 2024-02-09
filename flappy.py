from itertools import cycle
import random
import sys
import  math
import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PIPEGAPSIZE  = 100
BASEY        = SCREENHEIGHT * 0.79

IMAGES, SOUNDS, HITMASKS = {}, {}, {}

PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)


BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)


PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)


try:
    xrange
except NameError:
    xrange = range


def main():
    #ana fonksiyon, ilk çalısır
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('flappy bird')  #ekranın sol usttekı yazı

    # scoru gosteren numaralar
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )


    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()


    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()

    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()


    # dosya uzantıları belırlenıyor
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']   = pygame.mixer
   # SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    while True:

        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            # randon sayı ıle kusun rengı belırnenıyor. sonrasında 0-1-2 ıle kusun kanatlarının durumları eklenıyor
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha()
        )

        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # pipeleri kırpıyor
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # kusları kırpıyır
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    """kusun girişteki hareketleri ve konumu"""

    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # base shift
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # giristeki asagı yukarı haraketi
    playerShmVals = {'val': 0, 'dir': 1 }

    while True:
        for event in pygame.event.get():
            # oyunu kapatan kontrol esc-quıt
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                #ilk kanat sesi ve oyunun baslaması
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen,
                }


        #hazır
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)


        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo):
    from itertools import cycle
    import random
    import sys
    import math
    import pygame
    #from pygame.locals import *

    FPS = 30
    SCREENWIDTH = 288
    SCREENHEIGHT = 512
    PIPEGAPSIZE = 200
    BASEY = SCREENHEIGHT * 0.79

    IMAGES, SOUNDS, HITMASKS = {}, {}, {}

    PLAYERS_LIST = (
        # red bird
        (
            'assets/sprites/yellowbird-upflap.png',
            'assets/sprites/redbird-midflap.png',
            'assets/sprites/redbird-downflap.png',
        ),
        # blue bird
        (
            'assets/sprites/redbird-upflap.png',
            'assets/sprites/bluebird-midflap.png',
            'assets/sprites/bluebird-downflap.png',
        ),
        # yellow bird
        (
            'assets/sprites/bluebird-upflap.png',
            'assets/sprites/yellowbird-midflap.png',
            'assets/sprites/yellowbird-downflap.png',
        ),
    )

    BACKGROUNDS_LIST = (
        'assets/sprites/background-day.png',
        'assets/sprites/background-night.png',
    )

    PIPES_LIST = (
        'assets/sprites/pipe-green.png',
        'assets/sprites/pipe-red.png',
    )

    try:
        xrange
    except NameError:
        xrange = range

    def main():
        # ana fonksiyon, ilk çalısır
        global SCREEN, FPSCLOCK
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('flappy bird')  # ekranın sol usttekı yazı

        # scoru gosteren numaralar
        IMAGES['numbers'] = (
            pygame.image.load('assets/sprites/0.png').convert_alpha(),
            pygame.image.load('assets/sprites/1.png').convert_alpha(),
            pygame.image.load('assets/sprites/2.png').convert_alpha(),
            pygame.image.load('assets/sprites/3.png').convert_alpha(),
            pygame.image.load('assets/sprites/4.png').convert_alpha(),
            pygame.image.load('assets/sprites/5.png').convert_alpha(),
            pygame.image.load('assets/sprites/6.png').convert_alpha(),
            pygame.image.load('assets/sprites/7.png').convert_alpha(),
            pygame.image.load('assets/sprites/8.png').convert_alpha(),
            pygame.image.load('assets/sprites/9.png').convert_alpha()
        )

        IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()

        IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()

        IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

        # dosya uzantıları belırlenıyor
        if 'win' in sys.platform:
            soundExt = '.wav'
        else:
            soundExt = '.ogg'

        SOUNDS['die'] = pygame.mixer
        # SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
        SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit' + soundExt)
        SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
        SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
        SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)

        while True:
            randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
            IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

            randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
            IMAGES['player'] = (
                # randon sayı ıle kusun rengı belırnenıyor. sonrasında 0-1-2 ıle kusun kanatlarının durumları eklenıyor
                pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha()
            )

            pipeindex = random.randint(0, len(PIPES_LIST) - 1)
            IMAGES['pipe'] = (
                pygame.transform.flip(
                    pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
            )

            # pipeleri kırpıyor
            HITMASKS['pipe'] = (
                getHitmask(IMAGES['pipe'][0]),
                getHitmask(IMAGES['pipe'][1]),
            )

            # kusları kırpıyır
            HITMASKS['player'] = (
                getHitmask(IMAGES['player'][0]),
                getHitmask(IMAGES['player'][1]),
                getHitmask(IMAGES['player'][2]),
            )

            movementInfo = showWelcomeAnimation()
            crashInfo = mainGame(movementInfo)
            showGameOverScreen(crashInfo)

    def showWelcomeAnimation():
        """kusun girişteki hareketleri ve konumu"""

        playerIndex = 0
        playerIndexGen = cycle([0, 1, 2, 1])
        loopIter = 0

        playerx = int(SCREENWIDTH * 0.2)
        playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

        messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
        messagey = int(SCREENHEIGHT * 0.12)

        basex = 0
        # base shift
        baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

        # giristeki asagı yukarı haraketi
        playerShmVals = {'val': 0, 'dir': 1}

        while True:
            for event in pygame.event.get():
                # oyunu kapatan kontrol esc-quıt
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP or event.key == K_DOWN):
                    # ilk kanat sesi ve oyunun baslaması
                    SOUNDS['wing'].play()
                    return {
                        'playery': playery + playerShmVals['val'],
                        'basex': basex,
                        'playerIndexGen': playerIndexGen,
                    }

            # hazır
            if (loopIter + 1) % 5 == 0:
                playerIndex = next(playerIndexGen)
            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 4) % baseShift)
            playerShm(playerShmVals)

            SCREEN.blit(IMAGES['background'], (0, 0))
            SCREEN.blit(IMAGES['player'][playerIndex],
                        (playerx, playery + playerShmVals['val']))
            SCREEN.blit(IMAGES['message'], (messagex, messagey))
            SCREEN.blit(IMAGES['base'], (basex, BASEY))

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def mainGame(movementInfo):
        score = playerIndex = loopIter = 0
        playerIndexGen = movementInfo['playerIndexGen']
        playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

        basex = movementInfo['basex']
        baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

        # 2 tane yeni pipe üretme randoom(alt ve üst pipe
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        # yukardakı pipe listesi
        upperPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]

        # asagıdakı pipe listesi
        lowerPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        # cubukların sola kayma hızı
        pipeVelX = -4

        playerVelY = -9  # player's velocity along Y, default same as playerFlapped
        playerMaxVelY = 10  # max vel along Y, max descend speed
        playerMinVelY = -8  # min vel along Y, max ascend speed
        playerAccY = 0  # players downward accleration
        playerRot = 45  # player's rotation
        playerVelRot = 0  # angular speed
        playerRotThr = 20  # rotation threshold
        playerFlapAcc = -9  # players speed on flapping
        playerFlapped = False  # True when player flaps
        playerKey = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > -2 * IMAGES['player'][0].get_height():
                       # playerAccY = 0.04
                        playerVelY = playerFlapAcc
                        playerFlapped = True
                        SOUNDS['wing'].play()

                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_DOWN):
                    if playery > -2 * IMAGES['player'][0].get_height():
                        #playerAccY = 0.04
                        playerVelY = -playerFlapAcc
                        playerFlapped = True
                        SOUNDS['wing'].play()
                if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_UP):
                    playerKey = True
                if event.type == KEYUP and (event.key == K_DOWN or event.key == K_UP):
                    playerKey = False
                if not playerKey:
                    playerVelY = playerVelY / 8

            # carpma kontrol
            crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                                   upperPipes, lowerPipes)
            if crashTest[0]:
                return {
                    'y': playery,
                    'groundCrash': crashTest[1],
                    'basex': basex,
                    'upperPipes': upperPipes,
                    'lowerPipes': lowerPipes,
                    'score': score,
                    'playerVelY': playerVelY,
                    'playerRot': playerRot
                }

            # skoru kontrol
            playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    SOUNDS['point'].play()

            # playerIndex basex change
            if (loopIter + 1) % 3 == 0:
                playerIndex = next(playerIndexGen)
            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 100) % baseShift)

            # kusu dondurme
            if playerRot > 0:
                playerRot -= playerVelRot

            # kusun haraketi
            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            if playerFlapped:
                playerFlapped = False

                playerRot = 45

            playerHeight = IMAGES['player'][playerIndex].get_height()
            playery += min(playerVelY, BASEY - playery - playerHeight)

            # pipelerin sola hareketi
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                uPipe['x'] += pipeVelX
                lPipe['x'] += pipeVelX

            # yeni pipe ekleme
            if 0 < upperPipes[0]['x'] < 5:
                newPipe = getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # ekrandan cıkan pipe  silme
            if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # blit: ekran resımlerını belırlerken kullnılıyor
            SCREEN.blit(IMAGES['background'], (0, 0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            SCREEN.blit(IMAGES['base'], (basex, BASEY))
            # scoru basma
            showScore(score)

            visibleRot = playerRotThr
            if playerRot <= playerRotThr:
                visibleRot = playerRot

            playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
            SCREEN.blit(playerSurface, (playerx, playery))

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def showGameOverScreen(crashInfo):
        """crashes the player down ans shows gameover image"""
        score = crashInfo['score']
        playerx = SCREENWIDTH * 0.2
        playery = crashInfo['y']
        playerHeight = IMAGES['player'][0].get_height()
        playerVelY = crashInfo['playerVelY']
        playerAccY = 2
        playerRot = crashInfo['playerRot']
        playerVelRot = 7

        basex = crashInfo['basex']

        upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

        # play hit and die sounds
        SOUNDS['hit'].play()
        if not crashInfo['groundCrash']:
            # SOUNDS['die'].play()
            SOUNDS['die'].music.load('assets/audio/a.mp3')
            pygame.mixer.music.play(0)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP or event.key == K_DOWN):
                    if playery + playerHeight >= BASEY - 1:
                        return

            # kusun y de kayması
            if playery + playerHeight < BASEY - 1:
                playery += min(playerVelY, BASEY - playery - playerHeight)

            # yandıgında ekranda dusus hızı
            if playerVelY < 15:
                playerVelY += playerAccY

            # pipeye carpınca düşerken ki rotastonu
            if not crashInfo['groundCrash']:
                if playerRot > -90:
                    playerRot -= playerVelRot

            SCREEN.blit(IMAGES['background'], (0, 0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            SCREEN.blit(IMAGES['base'], (basex, BASEY))
            showScore(score)

            playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
            SCREEN.blit(playerSurface, (playerx, playery))
            SCREEN.blit(IMAGES['gameover'], (50, 180))

            FPSCLOCK.tick(FPS)
            pygame.display.update()

    def playerShm(playerShm):
        """oscillates the value of playerShm['val'] between 8 and -8"""
        if abs(playerShm['val']) == 8:
            playerShm['dir'] *= -1

        if playerShm['dir'] == 1:
            playerShm['val'] += 1
        else:
            playerShm['val'] -= 1

    def getRandomPipe():
        """random pipe üretme fonksiyonu"""

        gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
        gapY += int(BASEY * 0.2)
        pipeHeight = IMAGES['pipe'][0].get_height()
        pipeX = SCREENWIDTH + 10

        return [
            {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
            {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipe
        ]

    def showScore(score):
        """scoru gosteren ekran"""
        scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0

        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - totalWidth) / 2

        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
            Xoffset += IMAGES['numbers'][digit].get_width()

    def checkCrash(player, upperPipes, lowerPipes):

        pi = player['index']
        player['w'] = IMAGES['player'][0].get_width()
        player['h'] = IMAGES['player'][0].get_height()

        # eger yere carparsa
        if player['y'] + player['h'] >= BASEY - 1:
            return [True, True]
        else:

            playerRect = pygame.Rect(player['x'], player['y'],
                                     player['w'], player['h'])
            pipeW = IMAGES['pipe'][0].get_width()
            pipeH = IMAGES['pipe'][0].get_height()

            for uPipe, lPipe in zip(upperPipes, lowerPipes):

                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

                pHitMask = HITMASKS['player'][pi]
                uHitmask = HITMASKS['pipe'][0]
                lHitmask = HITMASKS['pipe'][1]

                # eger ust yada alt pipe ye carparsa
                uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

                if uCollide or lCollide:0
                    return [True, False]

        return [False, False]

    def pixelCollision(rect1, rect2, hitmask1, hitmask2):

        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in xrange(rect.width):
            for y in xrange(rect.height):
                if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                    return True
        return False

    def getHitmask(image):

        mask = []
        for x in xrange(image.get_width()):
            mask.append([])
            for y in xrange(image.get_height()):
                mask[x].append(bool(image.get_at((x, y))[3]))
        return mask

    if __name__ == '__main__':
        main()


def showGameOverScreen(crashInfo):
    """crashes the player down ans shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
       # SOUNDS['die'].play()
        SOUNDS['die'].music.load('assets/audio/a.mp3')
        pygame.mixer.music.play(0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # kusun y de kayması
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)


        # yandıgında ekranda dusus hızı
        if playerVelY < 15:
            playerVelY += playerAccY

        # pipeye carpınca düşerken ki rotastonu
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot


        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))
        SCREEN.blit(IMAGES['gameover'], (50, 180))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    """random pipe üretme fonksiyonu"""

    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]


def showScore(score):
    """scoru gosteren ekran"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):

    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # eger yere carparsa
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):

            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)


            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # eger ust yada alt pipe ye carparsa
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):

    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):

    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

if __name__ == '__main__':
    main()
