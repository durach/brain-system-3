
from pq_gui import *

import os.path

#Folders
DATA_DIR = 'data'
CONFIG_DIR = 'conf'

# Colors
COLOR_RED = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

#Fonts
FONT_TAHOMA = os.path.join(DATA_DIR, 'Tahoma.ttf')
FONT_COURIER_BOLD = os.path.join(DATA_DIR, 'courbd.ttf')

#Sounds
SOUND_START = os.path.join(DATA_DIR, 'start.wav')
SOUND_WIN = os.path.join(DATA_DIR, 'table.wav')
SOUND_FALSESTART = os.path.join(DATA_DIR, 'falsestart-2.wav')
#SOUND_FALSESTART	= os.path.join(DATA_DIR, 'table.wav')
SOUND_10SEC = os.path.join(DATA_DIR, '10seconds.wav')
SOUND_TIMEOUT = os.path.join(DATA_DIR, 'timeout.wav')

del os

#Buttons
STYLE_BUTTON = {
    TEXT_FONT:(FONT_TAHOMA, 20),
}

STYLE_TIMER_BOX = {
    TEXT_FONT:(FONT_TAHOMA, 14),
}

STYLE_TIMER_TEXT = {
    TEXT_FONT:(FONT_COURIER_BOLD, 55),
}

STYLE_STATUS = {
    TEXT_FONT:(FONT_TAHOMA, 25),
    BG_COLOR: COLOR_GREEN
}

#Messages
MSG_WAITING = 1
MSG_FALSESTART = 2
MSG_PRESSED = 3
MSG_START20 = 4
MSG_START60 = 5
MSG_RESET = 6
MSG_TIMER = 7
MSG_TIMEOUT = 8
MSG_STARTED = 9

MSG = {
    MSG_WAITING: '...ожидание...',
    MSG_FALSESTART: 'Фальстарт\nСтол №%d',
    MSG_PRESSED: 'Нажата кнопка\nСтол №%d',
    MSG_START20: 'Старт 20 (c)',
    MSG_START60: 'Старт 60 (x)',
    MSG_RESET: 'Сброс (z)',
    MSG_TIMER: 'Таймер',
    MSG_TIMEOUT: 'Время вышло',
    MSG_STARTED: 'Время идет (%d)',
}

DBRAIN_TIMER_EVENT = pygame.USEREVENT+30

STATUS_WAITING = 0
STATUS_STARTED = 1
STATUS_STOPPED = 2

