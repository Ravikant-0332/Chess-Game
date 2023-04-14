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

        self.primary_color = (255,255,255)
        self.secondary_color = (4,84,4)
        self.selection_color = (200,0,0)
        self.color = [None, self.primary_color, self.secondary_color]

        self.b_dead_pieces = []
        self.w_dead_pieces = []

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

    def _get_piece(self, piece, surface, center):
        img = self.piece.get_piece(piece)
        if img != None:
            """ Getting Image of Piece and Displaying it in Current Box """
            img_rect = img.get_rect()
            img_rect.center = center
            surface.blit(img, img_rect)

    def draw_board(self):
        # GREEN AND WHITE STRIP AROUND PLAYING REGION
        pygame.draw.rect(self.board_surf, self.secondary_color, (0, 0, self.size, self.size))
        pygame.draw.rect(self.board_surf, self.primary_color, (3, 3, self.size - 6, self.size - 6))
        flag = 1
        for i in range(8):
            for j in range(8):
                if flag == 1:
                    pygame.draw.rect(self.board_surf, self.secondary_color, (16 + j * self.box_size, 16 + i * self.box_size, self.box_size, self.box_size))
                flag*=-1
                self._get_piece(self.grid[i][j], self.board_surf, (16 + j * self.box_size + self.box_center, 16 + i * self.box_size + self.box_center))
            flag*=-1
        # BORDER AROUND THE PLAYING REGION
        pygame.draw.rect(self.board_surf, self.secondary_color, (16, 16, self.size - 32, self.size - 32), width=2)

        """ Displaying Dead Pieces """
        self._display_dead_piece()

        """ Highlighting Selected Box to Move """
        if self.move_from != []:
            i = self.move_from[0]
            j = self.move_from[1]
            pygame.draw.rect(self.board_surf,self.selection_color, (16 + j * self.box_size, 16 + i * self.box_size, self.box_size, self.box_size), 2)

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

    def _move_peice(self, move_from, move_to, player):

        if self.grid[move_from[0]][move_from[1]]!=0:
            temp_piece = self.grid[move_from[0]][move_from[1]]
            # King's Move
            if temp_piece[6:] == 'king' and temp_piece[:5] == player:
                status = self.king_move(player, move_from, move_to)
                self.move_from = self.move_to
                self.move_to = []
                return status
            # Knight's Move
            elif temp_piece[6:] == 'knight' and temp_piece[:5] == player:
                status = self.knight_move(player, move_from, move_to)
                self.move_from = self.move_to
                self.move_to = []
                return status
            # Rook's Move
            elif temp_piece[6:] == 'rook' and temp_piece[:5] == player:
                status = self.rook_move(player, move_from, move_to)
                self.move_from = self.move_to
                self.move_to = []
                return status
            # Bishop's Move
            elif temp_piece[6:] == 'bishop' and temp_piece[:5] == player:
                status = self.bishop_move(player, move_from, move_to)
                self.move_from = self.move_to
                self.move_to = []
                return status
            # Queen's Move
            elif temp_piece[6:] == 'queen' and temp_piece[:5] == player:
                status = self.queen_move(player, move_from, move_to)
                self.move_from = self.move_to
                self.move_to = []
                return status

        update_piece = None
        if self.grid[move_from[0]][move_from[1]] != 0 and self.grid[move_from[0]][move_from[1]][:5] == player:
            if self.grid[move_to[0]][move_to[1]] == 0:
                """  Checking for Pawn Upgrade """
                piece_name = self.grid[move_from[0]][move_from[1]]
                if piece_name[5:] == " pawn":
                    if piece_name[:5] == "black" and move_to[0] == 7:
                        # SHOW BLACK PIECES SELECTOR
                        update_piece = self._pawn_update_selector("black")
                    elif piece_name[:5] == "white" and move_to[0] == 0:
                        # SHOW WHITE PIECES SELECTOR
                        update_piece = self._pawn_update_selector("white")

                self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                self.grid[move_from[0]][move_from[1]] = 0

                if update_piece != None:
                    self.grid[move_to[0]][move_to[1]] = update_piece

                self.move_from = self.move_to
                self.move_to = []
                return True

            elif self.grid[move_to[0]][move_to[1]][:5] != player:
                """  Checking for Pawn Upgrade """
                piece_name = self.grid[move_from[0]][move_from[1]]
                if piece_name[5:] == " pawn":
                    if piece_name[:5] == "black" and move_to[0] == 7:
                        # SHOW BLACK PIECES SELECTOR
                        update_piece = self._pawn_update_selector("black")
                    elif piece_name[:5] == "white" and move_to[0] == 0:
                        # SHOW WHITE PIECES SELECTOR
                        update_piece = self._pawn_update_selector("white")

                if self.grid[move_to[0]][move_to[1]][:5] == 'black':
                    self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                    self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                    self.grid[move_from[0]][move_from[1]] = 0

                elif self.grid[move_to[0]][move_to[1]][:5] == 'white':
                    self.w_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                    self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                    self.grid[move_from[0]][move_from[1]] = 0

                if update_piece != None:
                    self.grid[move_to[0]][move_to[1]] = update_piece

                self.move_from = self.move_to
                self.move_to = []

                return True
        self.move_from = self.move_to
        self.move_to = []
        return False

    def _pawn_update_selector(self, player):
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
            pygame.display.update()
            if selected_piece != None:
                break
        response = [None, 'queen', 'rook', 'bishop', 'knight']
        return f'{player} {response[selected_piece]}'

    def select_box(self,pos, selector,player):
        x,y = self._cell_coordinates_by_point(pos)
        if x != None and y != None:
            if selector == 1:
                self.move_from = [x, y]
                self.move_to = []
            else:
                self.move_to = [x, y]
                name = ['','white', 'black']
                status = self._move_peice(self.move_from,self.move_to, name[player])
                if status:
                    return True, player*-1
                else:
                    return False, player
            return True, player
        else:
            return False, player

    def king_move(self, player, move_from, move_to):
        dist = (move_from[0]-move_to[0])**2 + (move_from[1]-move_to[1])**2
        if dist<=3:
            if player=='white':
                if self.grid[move_to[0]][move_to[1]]==0:
                    self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                    self.grid[move_from[0]][move_from[1]] = 0
                    return True
                elif self.grid[move_to[0]][move_to[1]][:5]=='black':
                    self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                    self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                    self.grid[move_from[0]][move_from[1]] = 0
                    return True
            else:
                if self.grid[move_to[0]][move_to[1]]==0:
                    self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                    self.grid[move_from[0]][move_from[1]] = 0
                    return True
                elif self.grid[move_to[0]][move_to[1]][:5]=='white':
                    self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                    self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                    self.grid[move_from[0]][move_from[1]] = 0
                    return True

            return False

        else:
            if player=='white':
                if not self.white_castle:
                    return False
                else:
                    if move_from == [7,4]:
                        if move_to == [7,2] and self.grid[7][0]=='white rook' and self.grid[7][1:4] == [0,0,0]:
                            self.grid[7][0]=0
                            self.grid[7][4]=0
                            self.grid[7][2]='white king'
                            self.grid[7][3]='white rook'
                            self.white_castle=False
                            return True
                        elif move_to == [7,6] and self.grid[7][7]=='white rook' and self.grid[7][5:7] == [0,0]:
                            self.grid[7][7] = 0
                            self.grid[7][4] = 0
                            self.grid[7][6] = 'white king'
                            self.grid[7][5] = 'white rook'
                            self.white_castle=False
                            return True
                        else:
                            return False
            else:
                if not self.black_castle:
                    return False
                else:
                    if move_from == [0,4]:
                        if move_to == [0,2] and self.grid[0][0]=='black rook' and self.grid[0][1:4] == [0,0,0]:
                            self.grid[0][0]=0
                            self.grid[0][4]=0
                            self.grid[0][2]='black king'
                            self.grid[0][3]='black rook'
                            self.black_castle=False
                            return True
                        elif move_to == [0,6] and self.grid[0][7]=='black rook' and self.grid[0][5:7] == [0,0]:
                            self.grid[0][7] = 0
                            self.grid[0][4] = 0
                            self.grid[0][6] = 'black king'
                            self.grid[0][5] = 'black rook'
                            self.black_castle=False
                            return True
                        else:
                            return False

    def knight_move(self, player, move_from, move_to):
        dist = (move_from[0]-move_to[0])**2 + (move_from[1]-move_to[1])**2
        if dist==5:
            if self.grid[move_to[0]][move_to[1]] == 0:
                self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                self.grid[move_from[0]][move_from[1]] = 0
            elif self.grid[move_to[0]][move_to[1]][:5] != player:
                if player=='white':
                    self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                else:
                    self.w_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                self.grid[move_from[0]][move_from[1]] = 0
            else:
                return False
            return True
        else:
            return False

    def rook_move(self, player, move_from, move_to):
        if move_from[0]==move_to[0]:
            start = min(move_to[1], move_from[1])
            end = max(move_to[1], move_from[1])
            for i in range(1,end-start):
                if self.grid[move_from[0]][start+i] != 0:
                    return False

        elif move_from[1]==move_to[1]:
            start = min(move_to[0], move_from[0])
            end = max(move_to[0], move_from[0])
            for i in range(1,end-start):
                if self.grid[start+i][move_from[1]] != 0:
                    return False
        else:
            return False

        if self.grid[move_to[0]][move_to[1]] == 0:
            self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
            self.grid[move_from[0]][move_from[1]] = 0
        elif self.grid[move_to[0]][move_to[1]][:5] != player:
            if player == 'white':
                self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
            else:
                self.w_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
            self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
            self.grid[move_from[0]][move_from[1]] = 0
        else:
            return False
        return True

    def bishop_move(self, player, move_from, move_to):
        x_disp = abs(move_from[0]-move_to[0])
        y_disp = abs(move_from[1]-move_to[1])

        x_flag = 1 if move_from[0]<move_to[0] else -1
        y_flag = 1 if move_from[1] < move_to[1] else -1

        if abs(x_disp) == abs(y_disp):
            for i in range(1,x_disp):
                if self.grid[move_from[0] + x_flag*i][move_from[1] + y_flag*i] != 0:
                    return False
            if self.grid[move_to[0]][move_to[1]] == 0:
                self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                self.grid[move_from[0]][move_from[1]] = 0
            elif self.grid[move_to[0]][move_to[1]][:5] != player:
                if player == 'white':
                    self.b_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                else:
                    self.w_dead_pieces.append(self.grid[move_to[0]][move_to[1]])
                self.grid[move_to[0]][move_to[1]] = self.grid[move_from[0]][move_from[1]]
                self.grid[move_from[0]][move_from[1]] = 0
            else:
                return False
            return True
        else:
            return False

    def queen_move(self, player, move_from, move_to):
        return self.rook_move(player, move_from, move_to) or self.bishop_move(player, move_from, move_to)

