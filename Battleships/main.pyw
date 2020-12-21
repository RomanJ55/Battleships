import pygame
from battleships import Battleboard
from constants import WIDTH, HEIGHT, MARGIN, CELL_WIDTH, WHITE, RED
import copy
import time

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleships")
pygame.font.init()
myfont = pygame.font.SysFont("Britannic", 60)
myfont2 = pygame.font.SysFont("Britannic", 35)


def draw_board(win, board, position):
    if position == "left":
        margin = MARGIN
        for row in board.board:
            for spot in row:
                if not spot.is_dead() and not spot.is_shippart():
                    spot.make_water()
                spot.draw(win, margin)
        for i in range(board.rows+1):
            pygame.draw.line(win, (0, 0, 0), (margin, margin + i * CELL_WIDTH),
                             (margin + board.rows * CELL_WIDTH, margin + i*CELL_WIDTH))
        for j in range(board.columns+1):
            pygame.draw.line(win, (0, 0, 0), (j * CELL_WIDTH+margin, margin),
                             (j * CELL_WIDTH+margin, CELL_WIDTH * board.rows+margin))

    else:
        margin = MARGIN + 550
        for row in board.board:
            for spot in row:
                spot.draw(win, margin)
        for i in range(board.rows+1):
            pygame.draw.line(win, (0, 0, 0), (margin, MARGIN + i * CELL_WIDTH),
                             (margin + board.rows * CELL_WIDTH, MARGIN + i*CELL_WIDTH))
        for j in range(board.columns+1):
            pygame.draw.line(win, (0, 0, 0), (j * CELL_WIDTH+margin, MARGIN),
                             (j * CELL_WIDTH+margin, CELL_WIDTH * board.rows+MARGIN))


def draw_game(win, boards):
    win.fill((255, 255, 255))
    draw_board(win, boards[0], "left")
    draw_board(win, boards[1], "right")
    nlabel = myfont.render(
        "Attack!", 1, RED)
    nlabel1 = myfont2.render(
        "Click on one of the above spots!", 1, RED)
    nlabel2 = myfont2.render(
        "Blue = missed, Green = hit", 1, RED)
    nlabel3 = myfont2.render(
        "Orange = Ship sunk", 1, RED)
    win.blit(nlabel, (HEIGHT-100, WIDTH//2-50))
    win.blit(nlabel1, (HEIGHT-200, WIDTH//2))
    win.blit(nlabel2, (HEIGHT-160, WIDTH//2+50))
    win.blit(nlabel3, (HEIGHT-120, WIDTH//2+100))
    pygame.display.update()


def draw_phase_one(win, board):
    win.fill((255, 255, 255))
    draw_board(win, board, "left")
    nlabel = myfont.render(
        "Place your ships!", 1, RED)
    nlabel2 = myfont2.render(
        "Allowed ship lengths:", 1, RED)
    nlabel3 = myfont2.render(
        "1 X 5, 1 X 4, 2 X 3, 1 X 2", 1, RED)
    nlabel4 = myfont2.render(
        "Press any key when you're ready to fight!...", 1, RED)
    win.blit(nlabel, (45, WIDTH//2-50))
    win.blit(nlabel2, (50, WIDTH//2 + 50))
    win.blit(nlabel3, (50, WIDTH//2 + 100))
    win.blit(nlabel4, (50, WIDTH//2 + 200))
    pygame.display.update()


def draw_game_end(win):
    win.fill((84, 84, 84))
    nlabel = myfont.render(
        "Game ended.", 1, WHITE)
    nlabel1 = myfont.render(
        "Thanks for playing!", 1, WHITE)
    win.blit(nlabel, (WIDTH//2-150, HEIGHT//3))
    win.blit(nlabel1, (WIDTH//2-200, HEIGHT//2))
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = (y+20) // gap
    col = (x+20) // gap
    return row-1, col-1


def main(win):
    run = False
    phase_one = False
    start_screen = True
    left_board = Battleboard()
    right_board = Battleboard()

    # start screen
    while start_screen and not run:
        nlabel = myfont.render(
            "Welcome to Battleships:", 1, WHITE)
        img = pygame.image.load_extended("title.jpg")
        nlabel6 = myfont.render(
            "Press any key to continue...", 1, WHITE)
        win.fill((84, 84, 84))
        win.blit(img, (0, 0))
        win.blit(nlabel, (250, 100))
        win.blit(nlabel6, (200, 650))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
                run = False
            if event.type == pygame.KEYDOWN:
                start_screen = False
                phase_one = True

    # phase one(define ships)
    while phase_one:
        draw_phase_one(win, left_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                phase_one = False
                start_screen = False
            if event.type == pygame.KEYDOWN:
                if left_board.all_ships_placed():
                    if left_board.validate_ships():
                        phase_one = False
                        run = True

            if pygame.mouse.get_pressed()[0]:  # left mousebutton
                pos = pygame.mouse.get_pos()
                # if the mouse-pos is within the left board
                if MARGIN < pos[0] < MARGIN+400 and MARGIN < pos[1] < 400+MARGIN:
                    row, col = get_clicked_pos(pos, left_board.rows, 400)
                    spot = left_board.board[row][col]
                    if not spot.is_dead() and not left_board.all_ships_placed():
                        spot.make_shippart()
                        h_parts = left_board.get_horizontal_shipparts(spot)
                        v_parts = left_board.get_vertical_shipparts(spot)
                        if len(h_parts) > 1:
                            for spots in h_parts:
                                spots.make_ship()
                            spot.make_ship()
                        if len(v_parts) > 1:
                            for spots in v_parts:
                                spots.make_ship()
                            spot.make_ship()
            if pygame.mouse.get_pressed()[2]:  # right mousebutton
                pos = pygame.mouse.get_pos()
                # if the mouse-pos is within the left board
                if MARGIN < pos[0] < MARGIN+400 and MARGIN < pos[1] < 400+MARGIN:
                    row, col = get_clicked_pos(pos, left_board.rows, 400)
                    spot = left_board.board[row][col]
                    spot.reset()
    # mainloop
    while run and not start_screen:
        draw_game(win, [left_board, right_board])
        if left_board.turn == "c":
            pass
            # p2 / computer move
            # time.sleep(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # left mousebutton
                pos = pygame.mouse.get_pos()
                # if the mouse-pos is within the right board
                if 570 < pos[0] < 970 and MARGIN < pos[1] < 400+MARGIN:
                    pos = pos[0]-550, pos[1]
                    row, col = get_clicked_pos(pos, right_board.rows, 400)
                    spot = right_board.board[row][col]
                    if left_board.board[spot.column][spot.row].is_shippart():
                        spot.make_dead()
                        left_board.board[spot.column][spot.row].make_dead()
                        ship_name = left_board.remove_shippart(spot)
                        if left_board.is_ship_fallen(ship_name):
                            for part in left_board.ships[ship_name]:
                                if part != 0:
                                    right_board.board[part[1]
                                                      ][part[0]].make_sunk()
                        left_board.change_turn()
                    else:
                        if not spot.is_dead() and not spot.is_sunk():
                            spot.make_water()
                            left_board.change_turn()
        if left_board.is_winner():
            draw_game_end(WIN)
            time.sleep(2)
            run = False

    pygame.quit()


main(WIN)
