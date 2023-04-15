import sys
import pygame
from chessBoard import ChessBoard


SOLID_BLUE = (50,50,200,127)
BG_COLOR = (4,84,4)

# CONSTANTS
SCREEN_HEIGHT = None
SCREEN_WIDTH = None

selector = 1
player = 1

pygame.init()
screen = pygame.display.set_mode((800,450), pygame.RESIZABLE)
# screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load('assests/W_QUEEN.png'))
turn_font = pygame.font.Font(pygame.font.get_default_font(), 26)

screen.fill(BG_COLOR)
SCREEN_WIDTH = screen.get_rect().width
SCREEN_HEIGHT = screen.get_rect().height

board = ChessBoard(screen,SCREEN_WIDTH,SCREEN_HEIGHT)
board.draw_board()

def clearBg():
    img = pygame.image.load('assests/bg.png')
    img = pygame.transform.scale2x(img)
    screen.blit(img, [0,0,SCREEN_WIDTH,SCREEN_HEIGHT])

def key_down(event):
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_p:
        print(board.move_from)
        print(board.move_to)

def mouse_click(event):
    global selector, player
    if event.button == 1:
        pos = event.pos
        status,player = board.select_box(pos,selector,player)
        if status:
            selector *= -1

def turn_indicator(turn_text):
    turn_surface = pygame.surface.Surface((int(SCREEN_WIDTH*0.05),SCREEN_HEIGHT), pygame.SRCALPHA)
    turn_surface.fill(SOLID_BLUE)
    text = turn_font.render(turn_text, True, (255,255,255))
    text = pygame.transform.rotate(text, 90)
    text_rect = text.get_rect()
    text_rect.center = (int(SCREEN_WIDTH*0.05)//2,SCREEN_HEIGHT//2)
    turn_surface.blit(text,text_rect)
    return turn_surface

curr_player = -1
player_name = ['', 'White\'s Turn', 'Black\'s Turn']
while(True):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            key_down(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click(event)
        elif event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.WINDOWRESIZED:
            SCREEN_WIDTH = screen.get_rect().width
            SCREEN_HEIGHT = screen.get_rect().height
            board.resized(SCREEN_WIDTH, SCREEN_HEIGHT)

    screen.fill(BG_COLOR)
    clearBg()

    if curr_player != player:
        curr_player = player

    screen.blit(turn_indicator(player_name[player]),(0,0))
    board.draw_board()
    pygame.time.Clock().tick(30)
    pygame.display.update()