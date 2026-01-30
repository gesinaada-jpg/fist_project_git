import arcade
import chess

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 750
SQUARE_SIZE = 65
BOARD_X = (SCREEN_WIDTH - SQUARE_SIZE * 8) // 2
BOARD_Y = (SCREEN_HEIGHT - SQUARE_SIZE * 8) // 2 + 30
X_OFFSET = -30
Y_OFFSET = -30


class ChessBoard(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Шахматы", resizable=True)

        self.board = chess.Board()

        self.piece_symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }

        self.selected_square = None
        self.valid_moves = []

        self.white_score = 0
        self.black_score = 0

        # Кнопка "Новая игра"
        self.new_game_button_x = SCREEN_WIDTH // 2
        self.new_game_button_y = 60
        self.new_game_button_width = 180
        self.new_game_button_height = 45

        # Кнопка "Назад"
        self.back_button_x = 80
        self.back_button_y = SCREEN_HEIGHT - 50
        self.back_button_width = 120
        self.back_button_height = 40

    def on_draw(self):
        self.clear()
        arcade.set_background_color((139, 90, 43))

        self.draw_board()
        self.draw_valid_moves()
        self.draw_pieces()
        self.draw_scores()
        self.draw_new_game_button()
        self.draw_back_button()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                x = BOARD_X + col * SQUARE_SIZE
                y = BOARD_Y + row * SQUARE_SIZE
                rect = arcade.rect.XYWH(x, y, SQUARE_SIZE, SQUARE_SIZE)

                if self.selected_square and chess.square(col, 7 - row) == self.selected_square:
                    color = (173, 216, 230)
                else:
                    color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)

                arcade.draw_rect_filled(rect, color)
                arcade.draw_rect_outline(rect, (101, 67, 33), 1)

    def draw_valid_moves(self):
        for move in self.valid_moves:
            col = chess.square_file(move.to_square)
            row = 7 - chess.square_rank(move.to_square)

            x = BOARD_X + col * SQUARE_SIZE + SQUARE_SIZE // 2 + X_OFFSET
            y = BOARD_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2 + Y_OFFSET

            arcade.draw_circle_filled(x, y, SQUARE_SIZE // 4, (0, 200, 0, 180))

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col = chess.square_file(square)
                row = chess.square_rank(square)

                x = BOARD_X + col * SQUARE_SIZE + SQUARE_SIZE // 2 + X_OFFSET
                y = BOARD_Y + (7 - row) * SQUARE_SIZE + SQUARE_SIZE // 2 + Y_OFFSET

                color = arcade.color.WHITE if piece.color == chess.WHITE else arcade.color.BLACK
                symbol = self.piece_symbols[piece.symbol()]

                arcade.draw_text(
                    symbol, x, y, color,
                    font_size=int(SQUARE_SIZE * 0.55),
                    anchor_x='center',
                    anchor_y='center',
                    font_name=("Arial Unicode MS", "DejaVu Sans", "Segoe UI Symbol")
                )

    def draw_scores(self):
        arcade.draw_text(
            f"БЕЛЫЕ: {self.white_score}",
            BOARD_X - 180,
            BOARD_Y + SQUARE_SIZE * 4,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_text(
            f"ЧЕРНЫЕ: {self.black_score}",
            BOARD_X + SQUARE_SIZE * 8 + 180,
            BOARD_Y + SQUARE_SIZE * 4,
            (220, 220, 220),
            24,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        turn_text = "ХОД БЕЛЫХ" if self.board.turn == chess.WHITE else "ХОД ЧЕРНЫХ"
        turn_color = arcade.color.WHITE if self.board.turn == chess.WHITE else (220, 220, 220)

        arcade.draw_text(
            turn_text,
            SCREEN_WIDTH // 2,
            BOARD_Y + SQUARE_SIZE * 8 + 40,
            turn_color,
            26,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    def draw_new_game_button(self):
        button_rect = arcade.rect.XYWH(
            self.new_game_button_x,
            self.new_game_button_y,
            self.new_game_button_width,
            self.new_game_button_height
        )

        arcade.draw_rect_filled(button_rect, (25, 110, 25))
        arcade.draw_rect_outline(button_rect, (200, 200, 200), 2)

        arcade.draw_text(
            "НОВАЯ ИГРА",
            self.new_game_button_x,
            self.new_game_button_y,
            arcade.color.WHITE,
            22,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    def draw_back_button(self):
        button_rect = arcade.rect.XYWH(
            self.back_button_x,
            self.back_button_y,
            self.back_button_width,
            self.back_button_height
        )

        arcade.draw_rect_filled(button_rect, (110, 25, 25))
        arcade.draw_rect_outline(button_rect, (200, 200, 200), 2)

        arcade.draw_text(
            "НАЗАД",
            self.back_button_x,
            self.back_button_y,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    def get_square_from_pixel(self, x, y):
        x_corrected = x - X_OFFSET
        y_corrected = y - Y_OFFSET

        col = int((x_corrected - BOARD_X) // SQUARE_SIZE)
        row = 7 - int((y_corrected - BOARD_Y) // SQUARE_SIZE)

        if 0 <= col < 8 and 0 <= row < 8:
            return chess.square(col, row)
        return None

    def is_new_game_button_clicked(self, x, y):
        return (abs(x - self.new_game_button_x) <= self.new_game_button_width / 2 and
                abs(y - self.new_game_button_y) <= self.new_game_button_height / 2)

    def is_back_button_clicked(self, x, y):
        return (abs(x - self.back_button_x) <= self.back_button_width / 2 and
                abs(y - self.back_button_y) <= self.back_button_height / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # ПРОСТО ЗАКРЫВАЕМ ОКНО ПРИ НАЖАТИИ "НАЗАД"
            if self.is_back_button_clicked(x, y):
                arcade.close_window()
                return

            if self.is_new_game_button_clicked(x, y):
                self.board.reset()
                self.selected_square = None
                self.valid_moves = []
                return

            square = self.get_square_from_pixel(x, y)
            if square is None:
                return

            piece = self.board.piece_at(square)

            if self.selected_square is None:
                if piece and piece.color == self.board.turn:
                    self.selected_square = square
                    self.valid_moves = [
                        move for move in self.board.legal_moves
                        if move.from_square == square
                    ]
            else:
                move = chess.Move(self.selected_square, square)

                if move in self.valid_moves:
                    self.board.push(move)

                    if self.board.is_checkmate():
                        if self.board.turn == chess.WHITE:
                            self.black_score += 1
                        else:
                            self.white_score += 1

                    self.selected_square = None
                    self.valid_moves = []
                else:
                    if piece and piece.color == self.board.turn:
                        self.selected_square = square
                        self.valid_moves = [
                            move for move in self.board.legal_moves
                            if move.from_square == square
                        ]
                    else:
                        self.selected_square = None
                        self.valid_moves = []

    def on_resize(self, width, height):
        global SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_X, BOARD_Y

        SCREEN_WIDTH = width
        SCREEN_HEIGHT = height

        BOARD_X = (SCREEN_WIDTH - SQUARE_SIZE * 8) // 2
        BOARD_Y = (SCREEN_HEIGHT - SQUARE_SIZE * 8) // 2 + 30

        self.new_game_button_x = SCREEN_WIDTH // 2
        self.new_game_button_y = 60

        self.back_button_x = 80
        self.back_button_y = SCREEN_HEIGHT - 50

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    window = ChessBoard()
    arcade.run()


if __name__ == "__main__":
    main()
