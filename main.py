from utils.board_visualizer import board_visualizer
from utils.piece_storage import PieceStorage
from notation.fen_notation_parser import FenNotationParser


if __name__ == '__main__':
    fen = "Q6Q/8/8/3QQ3/3QQ3/8/8/Q6Q"
    parser = FenNotationParser()
    storage = PieceStorage(is_standart=True)
    board = parser.parse(fen, storage)
    print(board_visualizer(board))
    print(parser.serialize(board))
