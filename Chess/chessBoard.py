import random
import sys
import pygame
from pieces import Piece

class ChessBoard:

    def __init__(self,screen,width,height):
        self.screen = screen
        self.width = width
        self.height = height
        self.size = (height//8)*8
        self.box_size = self.size//8-4
        self.piece_size = (int((self.box_size*8)/10), int((self.box_size*8)/10))
        self.box_center = self.box_size//2
        self.pawn_updater_position = (width-self.box_size-10, height//2-2*self.box_size)
        self.piece = Piece(self.piece_size)
        self.white_castle=True
        self.black_castle=True
        self.move_from = []
        self.move_to = []

        self.primary_color = (255,255,255,255)
        self.secondary_color = (4,84,4,255)
        self.selection_color = [100,100,255]
        self.color = [None, self.primary_color, self.secondary_color]

        self.b_dead_pieces = []
        self.w_dead_pieces = []
        self.valid_moves = []
        self.pieces_under_attack = []

        # SURFACE DECLARATION FOR CHESS BOARD AND DEAD PIECE DISPLAY
        self.board_surf = pygame.surface.Surface((self.size, self.size), pygame.SRCALPHA)
        self.b_dead_piece_surf = pygame.surface.Surface((2*self.box_size, 8*self.box_size), pygame.SRCALPHA)
        self.w_dead_piece_surf = pygame.surface.Surface((2*self.box_size, 8*self.box_size),  pygame.SRCALPHA)
        # self.w_dead_piece_surf.fill(self.primary_color)

        # SURFACE ALLIGNMENT OVER THE MAIN SCREEN
        self.board_surf_rect = self.board_surf.get_rect()
        self.board_surf_rect.center = self.screen.get_rect().center
        self.b_dead_piece_surf_rect = self.b_dead_piece_surf.get_rect()
        self.b_dead_piece_surf_rect.right = self.board_surf_rect.left
        self.w_dead_piece_surf_rect = self.w_dead_piece_surf.get_rect()
        self.w_dead_piece_surf_rect.left = self.board_surf_rect.right

        self.b_dead_piece_surf_rect.centery = self.board_surf_rect.centery
        self.w_dead_piece_surf_rect.centery = self.board_surf_rect.centery

        self.grid = [
            ['black rook','black knight','black bishop','black queen','black king','black bishop','black knight','black rook',],
            ['black pawn', 'black pawn', 'black pawn', 'black pawn', 'black pawn', 'black pawn', 'black pawn', 'black pawn',],
            [0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,],
            ['white pawn', 'white pawn', 'white pawn', 'white pawn', 'white pawn', 'white pawn', 'white pawn', 'white pawn', ],
            ['white rook','white knight','white bishop','white queen','white king','white bishop','white knight','white rook',],
        ]

        # self.grid = [
        #     [0, 0, 0, 0, 0, 0, 0, 0, ],
        #     ['black pawn', 0, 0, 0, 0, 0, 0, 0, ],
        #     [0, 0, 0, 0, 'black king', 0, 0, 0, ],
        #     [0, 0, 0, 0, 0, 0, 0, 0, ],
        #     [0, 0, 0, 0, 'white pawn', 'white queen', 0, 0, ],
        #     [0, 0, 0, 0, 0, 0, 0, 0, ],
        #     [0, 0, 0, 0, 0, 0, 0, 0, ],
        #     ['white king', 0, 0, 0, 0, 0, 0, 0, ],
        # ]

        self.black_attacking_cells = [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [True , True , True , True , True , True , True , True ],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
        ]

        self.white_attacking_cells = [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [True , True , True , True , True , True , True , True ],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
        ]

    def _get_piece(self, piece, surface, center):
        img = self.piece.get_piece(piece)
        if img != None:
            """ Getting Image of Piece and Displaying it in Current Box """
            img_rect = img.get_rect()
            img_rect.center = center
            surface.blit(img, img_rect)

    def _cell_coordinates_by_point(self,point):
        X = self.width // 2 - 4 * self.box_size
        Y = self.height // 2 - 4 * self.box_size
        x = point[0] - X
        y = point[1] - Y
        cor_x,cor_y = None,None
        for i in range(8):
            if x in range(int(i*self.box_size),int((i+1)*self.box_size)):
                cor_y = i
                break
        for i in range(8):
            if y in range(int(i*self.box_size),int((i+1)*self.box_size)):
                cor_x = i
                break
        return cor_x,cor_y

    def _update_white_attack_positions(self):
        points = []
        for i in range(8):
            for j in range(8):
                if self.grid[i][j]!=0 and self.grid[i][j][:5]=='white':
                    # if self.grid[i][j][6:]=='knight':
                    #     m1, m2, m3 = self.get_valid_moves('white', (i, j))
                    #     points+=m1+m2+m3
                    #     continue
                    m1,m2,m3 = self.get_valid_moves('white', (i,j))
                    if self.grid[i][j][6:]=='pawn':
                        points += m2 + [(i-1, j-1), (i-1, j+1)]
                    else:
                        points += m1+m2+m3

        # REMOVED ALL REPEATATIVE POSITIONS
        points = list(set(points))

        # Resetting all values to False
        for i in range(8):
            for j in range(8):
                self.white_attacking_cells[i][j] = False

        for i in range(8):
            for j in range(8):
                if (i,j) in points and i in range(8) and j in range(8):
                    self.white_attacking_cells[i][j] = True

    def _update_black_attack_positions(self):
        points = []
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] != 0 and self.grid[i][j][:5] == 'black':
                    # if self.grid[i][j][6:]=='knight':
                    #     m1, m2, m3 = self.get_valid_moves('black', (i, j))
                    #     points+=m1+m2+m3
                    #     continue
                    m1, m2, m3 = self.get_valid_moves('black', (i, j))
                    if self.grid[i][j][6:] == 'pawn':
                        points += m2 + [(i+1,j-1), (i+1,j+1)]
                    else:
                        points += m1+m2+m3

        # REMOVED ALL REPEATATIVE POSITIONS
        points = list(set(points))
        self.black_attacking_cells = [[False]*8]*8

        # Resetting all values to False
        for i in range(8):
            for j in range(8):
                self.black_attacking_cells[i][j] = False

        for i in range(8):
            for j in range(8):
                if (i, j) in points and i in range(8) and j in range(8):
                    self.black_attacking_cells[i][j] = True

    """_________________________________UTILITY FUNCTIONS_________________________________"""

    def resized(self,width,height):
        self.width = width
        self.height = height
        self.size = (height//8)*8
        self.box_size = self.size//8-4
        self.piece_size = (int((self.box_size*8)/10), int((self.box_size*8)/10))
        self.box_center = self.box_size//2
        self.pawn_updater_position = (width-self.box_size-10, height//2-2*self.box_size)
        self.piece = Piece(self.piece_size)


        # SURFACE DECLARATION FOR CHESS BOARD AND DEAD PIECE DISPLAY
        self.board_surf = pygame.surface.Surface((self.size, self.size))
        self.b_dead_piece_surf = pygame.surface.Surface((2*self.box_size, 8*self.box_size), pygame.SRCALPHA)
        self.w_dead_piece_surf = pygame.surface.Surface((2*self.box_size, 8*self.box_size),  pygame.SRCALPHA)
        # self.w_dead_piece_surf.fill(self.primary_color)

        # SURFACE ALLIGNMENT OVER THE MAIN SCREEN
        self.board_surf_rect = self.board_surf.get_rect()
        self.board_surf_rect.center = self.screen.get_rect().center
        self.b_dead_piece_surf_rect = self.b_dead_piece_surf.get_rect()
        self.b_dead_piece_surf_rect.right = self.board_surf_rect.left
        self.w_dead_piece_surf_rect = self.w_dead_piece_surf.get_rect()
        self.w_dead_piece_surf_rect.left = self.board_surf_rect.right

        self.b_dead_piece_surf_rect.centery = self.board_surf_rect.centery
        self.w_dead_piece_surf_rect.centery = self.board_surf_rect.centery

    def draw_board(self):
        # GREEN AND WHITE STRIP AROUND PLAYING REGION
        pygame.draw.rect(self.board_surf, self.secondary_color, (0, 0, self.size, self.size))
        pygame.draw.rect(self.board_surf, self.primary_color, (3, 3, self.size - 6, self.size - 6))
        flag = 1

        # DRAWING CHESS BOARD
        for i in range(8):
            for j in range(8):
                if flag == 1:
                    pygame.draw.rect(self.board_surf, self.secondary_color, (16 + j * self.box_size, 16 + i * self.box_size, self.box_size, self.box_size))
                flag*=-1
            flag*=-1

        # HighLight Valid Moves and Piece Under Attack
        selector_layer = self._highlight_boxes(self.valid_moves, self.pieces_under_attack)

        """ Highlighting Selected Box to Move """
        if self.move_from != []:
            i = self.move_from[0]
            j = self.move_from[1]
            self._box_over_layer(selector_layer, i, j, self.selection_color);
        self.board_surf.blit(selector_layer, (16, 16))

        # PLACING PIECES ON THE BOARD
        for i in range(8):
            for j in range(8):
                self._get_piece(self.grid[i][j], self.board_surf,
                                (16 + j * self.box_size + self.box_center, 16 + i * self.box_size + self.box_center))

        # BORDER AROUND THE PLAYING REGION
        pygame.draw.rect(self.board_surf, self.secondary_color, (16, 16, self.size - 32, self.size - 32), width=2)

        """ Displaying Dead Pieces """
        self._display_dead_piece()

        # BLITING ALL THE SURFACES ON MAIN SCREEN
        self.screen.blit(self.board_surf, self.board_surf_rect)
        self.screen.blit(self.b_dead_piece_surf, self.b_dead_piece_surf_rect)
        self.screen.blit(self.w_dead_piece_surf, self.w_dead_piece_surf_rect)

    def _display_dead_piece(self):
        i = 1
        j = 0
        # FOR BLACK PIECES
        for piece in self.b_dead_pieces:
            self._get_piece(piece, self.b_dead_piece_surf,
                            (i * self.box_size + self.box_center, j * self.box_size + self.box_center))

            if j == 7:
                i = 0
                j = 0
            else:
                j += 1

        i = 0
        j = 7
        # FOR WHITE PIECES
        for piece in self.w_dead_pieces:
            self._get_piece(piece, self.w_dead_piece_surf,
                            (i * self.box_size + self.box_center, j * self.box_size + self.box_center))

            if j == 0:
                i = 1
                j = 7
            else:
                j -= 1

    def _pawn_update_selector(self, player):
        self.draw_board()
        x_min, y_min = self.pawn_updater_position
        local_surface = pygame.surface.Surface((self.box_size, 4 * self.box_size + 1))
        inactive_layer = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        inactive_layer.fill((0,0,0,127))
        local_surface.fill(self.primary_color)
        offset = (self.box_size-self.piece_size[0])//2

        for i in range(4):
            pygame.draw.rect(local_surface, (0,0,0), (0, i*self.box_size, self.box_size,self.box_size+1), 1)

        if player=="white":
            local_surface.blit(self.piece.get_piece("white queen"), (0 + offset, 0 + self.box_size * 0 + offset))
            local_surface.blit(self.piece.get_piece("white rook"), (0 + offset, 0 + self.box_size * 1 + offset))
            local_surface.blit(self.piece.get_piece("white bishop"), (0 + offset, 0 + self.box_size * 2 + offset))
            local_surface.blit(self.piece.get_piece("white knight"), (0 + offset, 0 + self.box_size * 3 + offset))
        else:
            local_surface.blit(self.piece.get_piece("black queen"), (0 + offset, 0 + self.box_size * 0 + offset))
            local_surface.blit(self.piece.get_piece("black rook"), (0 + offset, 0 + self.box_size * 1 + offset))
            local_surface.blit(self.piece.get_piece("black bishop"), (0 + offset, 0 + self.box_size * 2 + offset))
            local_surface.blit(self.piece.get_piece("black knight"), (0 + offset, 0 + self.box_size * 3 + offset))

        self.screen.blit(inactive_layer,(0,0))
        self.screen.blit(local_surface, self.pawn_updater_position)
        selected_piece = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] in range(x_min, x_min+self.box_size):
                            if event.pos[1] in range(y_min + self.box_size*0, y_min+self.box_size*1):
                                selected_piece = 1
                            elif event.pos[1] in range(y_min + self.box_size*1, y_min+self.box_size*2):
                                selected_piece = 2
                            elif event.pos[1] in range(y_min + self.box_size*2, y_min+self.box_size*3):
                                selected_piece = 3
                            elif event.pos[1] in range(y_min + self.box_size*3, y_min+self.box_size*4):
                                selected_piece = 4
                elif event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

            pygame.display.update()
            if selected_piece != None:
                break
        response = [None, 'queen', 'rook', 'bishop', 'knight']
        return f'{player} {response[selected_piece]}'

    def _box_over_layer(self, layer_surface, i, j, color, i_offset=0,j_offset=0):
        d = 0
        for k in range(255, -1, -255 // (self.box_size // 3)):
            pygame.draw.rect(layer_surface, color + [k],
                    (j_offset + j * self.box_size + d,i_offset + i * self.box_size + d, self.box_size - 2 * d, self.box_size - 2 * d),1)
            d+=1

    def _highlight_boxes(self, yellow_boxes, red_boxes):
        highlight_color = [233,255,50]
        alert_color = [233,0,0]

        # yellow_boxes,red_boxes = [], []
        # for i in range(8):
        #     for j in range(8):
        #         if self.white_attcking_cells[i][j]:
        #             yellow_boxes.append((i,j))
        #         if self.black_attcking_cells[i][j]:
        #             red_boxes.append((i,j))


        layer_surface = pygame.surface.Surface((int(self.box_size*8), int(self.box_size*8)), pygame.SRCALPHA)
        for box in yellow_boxes:
            i,j = box
            self._box_over_layer(layer_surface, i, j, highlight_color)

        for box in red_boxes:
            i,j = box
            self._box_over_layer(layer_surface, i, j, alert_color)

        return layer_surface

    """___________________________________________________________________________________"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """_________________________________MOVEMENT FUNCTIONS________________________________"""

    def _move_peice(self, move_from, move_to, player):
        status = False

        if self.grid[move_from[0]][move_from[1]]!=0:
            temp_piece = self.grid[move_from[0]][move_from[1]]
            # King's Move
            if temp_piece[6:] == 'king' and temp_piece[:5] == player:
                status = self.king_move(player, move_from, move_to)

            # Knight's Move
            elif temp_piece[6:] == 'knight' and temp_piece[:5] == player:
                status = self.knight_move(player, move_from, move_to)

            # Rook's Move
            elif temp_piece[6:] == 'rook' and temp_piece[:5] == player:
                status = self.rook_move(player, move_from, move_to)

            # Bishop's Move
            elif temp_piece[6:] == 'bishop' and temp_piece[:5] == player:
                status = self.bishop_move(player, move_from, move_to)

            # Queen's Move
            elif temp_piece[6:] == 'queen' and temp_piece[:5] == player:
                status = self.queen_move(player, move_from, move_to)

            # Pawn's Move
            elif temp_piece[6:] == 'pawn' and temp_piece[:5] == player:
                status = self.pawn_move(player, move_from, move_to)

        self.move_from = self.move_to
        self.move_to = []
        if status:
            if player == 'white':
                self._update_white_attack_positions()
            else:
                self._update_black_attack_positions()

        return status

    def movement_helper(self, player, valid_moves, killing_moves, move_from, move_to):
        if tuple(move_to) in valid_moves:
            self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
            self.grid[move_from[0]][move_from[1]] = 0
        elif tuple(move_to) in killing_moves:
            if player == 'white':
                self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
            else:
                self.w_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
            self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
            self.grid[move_from[0]][move_from[1]] = 0
        else:
            return False
        return True

    def king_move(self, player, move_from, move_to):
        valid_moves, killing_moves, garbage = self.get_king_moves(player, move_from[0], move_from[1])

        if tuple(move_to) in valid_moves:
            dist = (move_to[0]-move_from[0])**2 + (move_to[1]-move_from[1])**2

            # CASTLING HANDLING
            if dist == 4:
                if player=='white':
                    if move_to == (7,2):
                        self.grid[7][0] = 0
                        self.grid[7][4]=0
                        self.grid[7][2]='white king'
                        self.grid[7][3]='white rook'
                        self.white_castle=False
                        return True
                    else:
                        self.grid[7][7] = 0
                        self.grid[7][4] = 0
                        self.grid[7][6] = 'white king'
                        self.grid[7][5] = 'white rook'
                        self.white_castle = False
                        return True
                else:
                    if move_to == (0,2):
                        self.grid[0][0] = 0
                        self.grid[0][4]=0
                        self.grid[0][2]='black king'
                        self.grid[0][3]='black rook'
                        self.black_castle=False
                        return True
                    else:
                        self.grid[0][7] = 0
                        self.grid[0][4] = 0
                        self.grid[0][6] = 'black king'
                        self.grid[0][5] = 'black rook'
                        self.black_castle = False
                        return True

            self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
            self.grid[move_from[0]][move_from[1]] = 0
        elif tuple(move_to) in killing_moves:
            if player == 'white':
                self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
            else:
                self.w_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
            self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
            self.grid[move_from[0]][move_from[1]] = 0
        else:
            return False
        return True

    def knight_move(self, player, move_from, move_to):
        valid_moves, killing_moves, garbage = self.get_knight_moves(player, move_from[0], move_from[1])
        return self.movement_helper(player, valid_moves, killing_moves, move_from, move_to)

    def rook_move(self, player, move_from, move_to):
        valid_moves, killing_moves, garbage = self.get_rook_moves(player, move_from[0], move_from[1])
        return self.movement_helper(player, valid_moves, killing_moves, move_from, move_to)

    def bishop_move(self, player, move_from, move_to):
        valid_moves, killing_moves, garbage = self.get_bishop_moves(player, move_from[0], move_from[1])
        return self.movement_helper(player, valid_moves, killing_moves, move_from, move_to)

    def queen_move(self, player, move_from, move_to):
        return self.rook_move(player, move_from, move_to) or self.bishop_move(player, move_from, move_to)

    def pawn_move(self, player, move_from, move_to):
        dist = (move_from[0]-move_to[0])**2+(move_from[1]-move_to[1])**2
        if dist == 1:
            if self.grid[move_to[0]][move_to[1]]==0:
                if (move_to[0]-move_from[0]==1 and player=='black') or (move_to[0]-move_from[0]==-1 and player=='white'):
                    temp_loc = move_to
                    self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                    self.grid[move_from[0]][move_from[1]] = 0
                    if player == "black" and temp_loc[0] == 7:
                        # SHOW BLACK PIECES SELECTOR
                        self.grid[temp_loc[0]][temp_loc[1]] = self._pawn_update_selector("black")
                    elif player == "white" and temp_loc[0] == 0:
                        # SHOW WHITE PIECES SELECTOR
                        self.grid[temp_loc[0]][temp_loc[1]] = self._pawn_update_selector("white")
                    return True

        elif dist == 2:
            if self.grid[move_to[0]][move_to[1]]!=0 and self.grid[move_to[0]][move_to[1]][:5]!=player:
                if player == 'white':
                    self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                else:
                    self.w_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                temp_loc = move_to
                self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                self.grid[move_from[0]][move_from[1]] = 0
                if player == "black" and temp_loc[0] == 7:
                    # SHOW BLACK PIECES SELECTOR
                    self.grid[temp_loc[0]][temp_loc[1]] = self._pawn_update_selector("black")
                elif player == "white" and temp_loc[0] == 0:
                    # SHOW WHITE PIECES SELECTOR
                    self.grid[temp_loc[0]][temp_loc[1]] = self._pawn_update_selector("white")
                return True
        elif dist == 4:
            if abs(move_to[0]-move_from[0])==2 and self.grid[move_to[0]][move_to[1]]==0:
                if (player=='white' and move_from[0]==6 and self.grid[move_from[0]-1][move_from[1]]==0) or (player=='black' and move_from[0]==1 and self.grid[move_from[0]+1][move_from[1]]==0):
                    self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                    self.grid[move_from[0]][move_from[1]] = 0
                    return True
        else:
            return False

    """___________________________________________________________________________________"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """________________________VALID MOVEMENT DETECTION FUNCTIONS_________________________"""
    def select_box(self,pos, selector,player):
        x,y = self._cell_coordinates_by_point(pos)
        name = ['', 'white', 'black']
        if x != None and y != None:
            if selector == 1:
                self.move_from = [x, y]
                self.move_to = []
                self.valid_moves, self.pieces_under_attack, garbage = self.get_valid_moves(name[player], self.move_from)
            else:
                self.move_to = [x, y]
                status = self._move_peice(self.move_from,self.move_to, name[player])
                if status:
                    self.valid_moves = []
                    self.pieces_under_attack = []
                    return True, player*-1
                else:
                    self.valid_moves, self.pieces_under_attack, garbage = self.get_valid_moves(name[player], self.move_from)
                    return False, player
            return True, player
        else:
            return False, player

    def get_valid_moves(self, player, move_from):
        i,j = move_from
        if self.grid[i][j]==0 or self.grid[i][j][:5]!=player:
            return [],[],[]

        piece = self.grid[i][j][6:]

        if piece == 'pawn':
            return self.get_pawn_moves(player, i, j)
        elif piece == 'knight':
            return self.get_knight_moves(player, i, j)
        elif piece == 'bishop':
            return self.get_bishop_moves(player, i, j)
        elif piece == 'rook':
            return self.get_rook_moves(player, i, j)
        elif piece == 'queen':
            return self.get_queen_moves(player, i, j)
        elif piece == 'king':
            return self.get_king_moves(player, i, j)
        return [],[],[]

    def get_pawn_moves(self, player, i, j):
        moves = []
        under_attack_moves = []
        self_attack_moves = []
        if player == 'white':
            if j!=0:
                if self.grid[i-1][j-1]!=0:
                    if self.grid[i-1][j-1][:5]!=player:
                        under_attack_moves.append((i-1,j-1))
                    elif self.grid[i-1][j-1][:5]==player:
                        self_attack_moves.append((i-1,j-1))
            if j!=7:
                if self.grid[i-1][j+1]!=0:
                    if self.grid[i-1][j+1][:5]!=player:
                        under_attack_moves.append((i-1,j+1))
                    elif self.grid[i-1][j+1][:5]==player:
                        self_attack_moves.append((i-1,j+1))

            if self.grid[i-1][j]==0:
                moves.append((i-1,j))
                if i==6 and self.grid[i-2][j]==0:
                    moves.append((i-2,j))

        elif player == 'black':
            if j!=0:
                if self.grid[i+1][j-1]!=0:
                    if self.grid[i+1][j-1][:5]!=player:
                        under_attack_moves.append((i+1,j-1))
                    elif self.grid[i+1][j-1][:5]==player:
                        self_attack_moves.append((i+1,j-1))
            if j!=7:
                if self.grid[i+1][j+1]!=0:
                    if self.grid[i+1][j+1][:5]!=player:
                        under_attack_moves.append((i+1,j+1))
                    elif self.grid[i+1][j+1][:5]==player:
                        self_attack_moves.append((i+1,j+1))

            if self.grid[i+1][j]==0:
                moves.append((i+1,j))
                if i==1 and self.grid[i+2][j]==0:
                    moves.append((i+2,j))

        return moves, under_attack_moves, self_attack_moves

    def get_knight_moves(self, player, i, j):
        moves = []
        under_attack_moves = []
        self_attack_moves = []
        temp_points = [
            (i-2, j-1),
            (i-2, j+1),
            (i-1, j-2),
            (i-1, j+2),
            (i+2, j-1),
            (i+2, j+1),
            (i+1, j-2),
            (i+1, j+2),
        ]
        for point in temp_points:
            if point[0] in range(0,8) and point[1] in range(0,8):
                if self.grid[point[0]][point[1]] == 0:
                    moves.append(point)
                elif self.grid[point[0]][point[1]][:5]!=player:
                    under_attack_moves.append(point)
                else:
                    self_attack_moves.append(point)
        return moves, under_attack_moves, self_attack_moves

    def _bishop_and_rook_move_helper(self, player, i, j, i_flag, j_flag):
        moves = []
        under_attack_moves = []
        self_attack_moves = []
        for k in range(1, 8):
            if i + i_flag*k in range(8) and j + j_flag*k in range(8):
                if self.grid[i + i_flag*k][j + j_flag*k] == 0:
                    moves.append((i + i_flag*k, j + j_flag*k))
                elif self.grid[i + i_flag*k][j + j_flag*k][:5] != player:
                    under_attack_moves.append((i + i_flag*k, j + j_flag*k))
                    break
                else:
                    self_attack_moves.append((i + i_flag*k, j + j_flag*k))
                    break
            else:
                break
        return moves,under_attack_moves,self_attack_moves

    def get_bishop_moves(self, player, i, j):
        moves = []
        under_attack_moves = []
        self_attack_moves = []

        m1,m2,m3=self._bishop_and_rook_move_helper(player, i, j, -1, -1)
        moves+=m1
        under_attack_moves+=m2
        self_attack_moves+=m3
        m1,m2,m3=self._bishop_and_rook_move_helper(player, i, j, -1, 1)
        moves+=m1
        under_attack_moves+=m2
        self_attack_moves+=m3
        m1,m2,m3=self._bishop_and_rook_move_helper(player, i, j, 1, -1)
        moves+=m1
        under_attack_moves+=m2
        self_attack_moves+=m3
        m1,m2,m3=self._bishop_and_rook_move_helper(player, i, j, 1, 1)
        moves+=m1
        under_attack_moves+=m2
        self_attack_moves+=m3
        return moves,under_attack_moves,self_attack_moves

    def get_rook_moves(self, player, i, j):
        moves = []
        under_attack_moves = []
        self_attack_moves = []

        m1,m2,m3 = self._bishop_and_rook_move_helper(player, i, j, -1, 0)
        moves+=m1
        under_attack_moves+=m2
        self_attack_moves+=m3
        m1,m2,m3 = self._bishop_and_rook_move_helper(player, i, j, 1, 0)
        moves+=m1
        under_attack_moves+=m2
        self_attack_moves+=m3
        m1,m2,m3 = self._bishop_and_rook_move_helper(player, i, j, 0, -1)
        moves+=m1
        under_attack_moves+=m2
        self_attack_moves+=m3
        m1,m2,m3 = self._bishop_and_rook_move_helper(player, i, j, 0, 1)
        moves+=m1
        under_attack_moves+=m2
        self_attack_moves+=m3
        return moves,under_attack_moves, self_attack_moves

    def get_queen_moves(self, player, i, j):
        m1,m2,m5 = self.get_bishop_moves(player, i, j)
        m3,m4,m6 = self.get_rook_moves(player, i, j)
        return m1+m3, m2+m4, m5+m6

    def get_king_moves(self, player, i, j):
        moves = []
        under_attack_moves = []
        self_attack_moves = []
        temp_points = [
            (i-1,j-1),
            (i-1,j),
            (i-1,j+1),
            (i+1,j-1),
            (i+1,j),
            (i+1,j+1),
            (i,j-1),
            (i,j+1),
        ]

        for point in temp_points:
            if point[0] in range(0,8) and point[1] in range(0,8):
                if (player=='black' and self.white_attacking_cells[point[0]][point[1]]) or (player == 'white' and self.black_attacking_cells[point[0]][point[1]]):
                    pass
                else:
                    if self.grid[point[0]][point[1]] == 0:
                        moves.append(point)
                    elif self.grid[point[0]][point[1]][:5]!=player:
                        under_attack_moves.append(point)
                    else:
                        self_attack_moves.append((point))

        if player == 'white':
            if self.white_castle:
                if [i,j] == [7,4]:
                    if self.grid[7][0] == 'white rook' and self.grid[7][1:4] == [0, 0, 0] and not self.black_attacking_cells[7][2]:
                        moves.append((7,2))
                    elif self.grid[7][7] == 'white rook' and self.grid[7][5:7] == [0, 0] and not self.black_attacking_cells[7][6]:
                        moves.append((7,6))
        else:
            if self.black_castle:
                if [i, j] == [0, 4]:
                    if self.grid[0][0] == 'black rook' and self.grid[0][1:4] == [0, 0, 0] and not self.white_attacking_cells[0][2]:
                        moves.append((0, 2))
                    elif self.grid[0][7] == 'black rook' and self.grid[0][5:7] == [0, 0] and not self.white_attacking_cells[0][6]:
                        moves.append((0, 6))
        return moves, under_attack_moves, self_attack_moves

    """___________________________________________________________________________________"""
