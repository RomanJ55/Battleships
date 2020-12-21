import pygame
from constants import GREY, GREEN, BLUE, RED, ORANGE, YELLOW


class Spot():
    def __init__(self, row, column, width=40):
        self.color = GREY
        self.row = row
        self.width = width
        self.column = column
        self.x = column*width
        self.y = row*width
        self.ship = False

    def get_position(self):
        return self.row, self.column

    def make_shippart(self):
        self.color = RED

    def is_shippart(self):
        return True if self.color == RED else False

    def make_water(self):
        self.color = BLUE

    def make_dead(self):
        self.color = GREEN

    def is_dead(self):
        return True if self.color == GREEN else False

    def reset(self):
        self.color = GREY
        self.ship = False

    def make_sunk(self):
        self.color = ORANGE

    def make_ship(self):
        self.ship = True

    def is_ship(self):
        return self.ship

    def is_sunk(self):
        return True if self.color == ORANGE else False

    def draw(self, win, margin):
        pygame.draw.rect(
            win, self.color, (self.x+margin, self.y+20, self.width, self.width))
        if self.ship:
            pygame.draw.circle(win, YELLOW, (self.x+margin+20, self.y+40), 7)


class Battleboard():
    def __init__(self, rows=10, columns=10):
        self.rows = rows
        self.columns = columns
        self.board = [[Spot(c, r) for c in range(self.rows)]
                      for r in range(self.columns)]
        self.turn = "p"  # "p" = Player1 "c" = Player2/Computer
        self.ships = {f"Ship{i}": None for i in range(5)}

    def get_turn(self):
        return self.turn

    def change_turn(self):
        if self.turn == "p":
            self.turn = "c"
        else:
            self.turn = "p"

    def is_winner(self):
        dead_counter = 0
        for row in self.board:
            for spot in row:
                if spot.is_dead():
                    dead_counter += 1
        return True if dead_counter > 16 else False

    def all_ships_placed(self):
        ship_counter = 0
        for row in self.board:
            for spot in row:
                if spot.is_shippart() or spot.is_dead():
                    ship_counter += 1
        return False if ship_counter < 17 else True

    def get_upper_shipparts(self, spot):
        upper_shipparts = []
        # up
        if spot.row > 0:
            for i in range(spot.row):
                if not self.board[spot.column][spot.row-(i+1)].is_shippart():
                    break
                else:
                    upper_shipparts.append(
                        self.board[spot.column][spot.row-(i+1)])
        return upper_shipparts

    def get_lower_shipparts(self, spot):
        lower_shipparts = []
        # down
        if spot.row < (self.rows-1):
            for i in range((self.rows-1)-spot.row):
                if not self.board[spot.column][spot.row+(i+1)].is_shippart():
                    break
                else:
                    lower_shipparts.append(
                        self.board[spot.column][spot.row+(i+1)])
        return lower_shipparts

    def get_vertical_shipparts(self, spot):
        vertical_shipparts = []
        upper = self.get_upper_shipparts(spot)
        lower = self.get_lower_shipparts(spot)

        vertical_shipparts = upper+lower
        vertical_shipparts.append(spot)

        return vertical_shipparts

    def get_righter_shipparts(self, spot):
        righter_shipparts = []
        if spot.column < self.columns-1:
            for i in range(self.columns-(spot.column + 1)):
                if not self.board[spot.column+(i+1)][spot.row].is_shippart():
                    break
                else:
                    righter_shipparts.append(
                        self.board[spot.column+(i+1)][spot.row])
        return righter_shipparts

    def get_lefter_shipparts(self, spot):
        lefter_shipparts = []
        if spot.column > 0:
            for i in range(spot.column):
                if not self.board[spot.column-(i+1)][spot.row].is_shippart():
                    break
                else:
                    lefter_shipparts.append(
                        self.board[spot.column-(i+1)][spot.row])

        return lefter_shipparts

    def get_horizontal_shipparts(self, spot):
        horizontal_shipparts = []
        righter = self.get_righter_shipparts(spot)
        lefter = self.get_lefter_shipparts(spot)

        horizontal_shipparts = righter+lefter
        horizontal_shipparts.append(spot)

        return horizontal_shipparts

    def validate_ships(self):
        parts = []
        ships = []
        for row in self.board:
            for spot in row:
                if spot.is_ship():
                    hor_parts = self.get_horizontal_shipparts(spot)
                    ver_parts = self.get_vertical_shipparts(spot)

                    if len(hor_parts) > 0:
                        for i, s in enumerate(hor_parts):
                            hor_parts[i] = (s.row, s.column)
                        hor_parts.sort(key=lambda tup: (tup[0], tup[1]))
                        if hor_parts not in parts:
                            parts.append(hor_parts)

                    if len(ver_parts) > 0:
                        for i, s in enumerate(ver_parts):
                            ver_parts[i] = (s.row, s.column)
                        ver_parts.sort(key=lambda tup: (tup[0], tup[1]))
                        if ver_parts not in parts:
                            parts.append(ver_parts)

        for i, _ in enumerate(parts):
            if len(parts[i]) > 1:
                ships.append(parts[i])

        if len(ships) == 5:
            for i, _ in enumerate(ships):
                ships[i].append(len(ships[i]))
            self.add_ships(ships)
            return True
        else:
            return False

    def add_ships(self, ships):
        for i, ship in enumerate(ships):
            self.ships[f"Ship{i}"] = ship

    def remove_shippart(self, spot):
        for k, v in self.ships.items():
            if (spot.row, spot.column) in v:
                self.ships[k][-1] -= 1
                return k

    def is_ship_fallen(self, ship):
        if self.ships[ship][-1] == 0:
            return True
        return False
