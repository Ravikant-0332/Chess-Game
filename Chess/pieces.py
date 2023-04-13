import pygame

class Piece:

    def __init__(self, size):
        self.size = size
        self.piece = {
            "black bishop": "assests/B_BISHOP.png",
            "black king": "assests/B_KING.png",
            "black knight": "assests/B_KNIGHT.png",
            "black pawn": "assests/B_PAWN.png",
            "black queen": "assests/B_QUEEN.png",
            "black rook": "assests/B_ROOK.png",
            "white bishop": "assests/W_BISHOP.png",
            "white king": "assests/W_KING.png",
            "white knight": "assests/W_KNIGHT.png",
            "white pawn": "assests/W_PAWN.png",
            "white queen": "assests/W_QUEEN.png",
            "white rook": "assests/W_ROOK.png",
        }

    def get_piece(self, piece_name):
        if self.piece.get(piece_name,None) == None:
            return None
        return pygame.transform.smoothscale(pygame.image.load(self.piece.get(piece_name,None)), self.size)