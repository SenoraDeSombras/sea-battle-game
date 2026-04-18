#Sea Battle Game, (c) SenoraDeSombras, 2025-2026,  Licensed under GPLv3
import random
import time

class TShip:
    def __init__(self, lives):
        self.lives = lives
        self.points = []


class TPlayer:
    def __init__(self, alive_count):
        self.ships = []
        self.show = []
        self.ship_arr = []
        self.alive_count = alive_count
        for _ in range(11):
            row = [0] * 11
            self.ships.append(row)
            self.show.append(row)
class TBattle:
    def __init__(self):
        self.players = []
        self.ships = (4, 3, 2, 2, 1, 1, 1)
        # self.ships = (6, 4)  # for debug
        self.players = [
            TPlayer(len(self.ships)),
            TPlayer(len(self.ships))
        ]
    def put_ships_auto(self, player_num) -> None:
        need_rerun = False

        for ship_size in self.ships:
            if ship_size > 0:
                position = random.randint(0, 1)  # 0 - vertical, 1 - horizontal
                good = False
                while not good:
                    iter_count = 0
                    if position == 0:
                        start_pos_x = random.randint(0, 9)
                        start_pos_y = random.randint(0, 9 - ship_size)
                        coords = []
                        for i in range(ship_size):
                            coords.extend([
                                [start_pos_x - 1, start_pos_y - 1 + i],
                                [start_pos_x, start_pos_y - 1 + i],
                                [start_pos_x + 1, start_pos_y - 1 + i],
                                [start_pos_x - 1, start_pos_y + i],
                                [start_pos_x, start_pos_y + i],
                                [start_pos_x + 1, start_pos_y + i],
                                [start_pos_x - 1, start_pos_y + 1 + i],
                                [start_pos_x, start_pos_y + 1 + i],
                                [start_pos_x + 1, start_pos_y + 1 + i]
                            ])
                    else:
                        start_pos_y = random.randint(0, 9 - ship_size)
                        start_pos_x = random.randint(0, 9)
                        coords = []
                        for i in range(ship_size):
                            coords.extend([
                                [start_pos_x - 1 + i, start_pos_y - 1],
                                [start_pos_x + i, start_pos_y - 1],
                                [start_pos_x + 1 + i, start_pos_y - 1],
                                [start_pos_x - 1 + i, start_pos_y],
                                [start_pos_x + i, start_pos_y],
                                [start_pos_x + 1 + i, start_pos_y],
                                [start_pos_x - 1 + i, start_pos_y + 1],
                                [start_pos_x + i, start_pos_y + 1],
                                [start_pos_x + 1 + i, start_pos_y + 1]
                            ])
                    good = True
                    for item in coords:
                        iter_count += 1
                        if -1 < item[0] < 9 and -1 < item[1] < 9:
                            if self.players[player_num].ships[item[0]][item[1]] == 1:
                                good = False
                        else:
                            good = False
                        if iter_count >= 100:
                            need_rerun = True
                            break

                    if good:
                        current_ship = TShip(ship_size)
                        for i in range(ship_size):
                            if position == 0:
                                self.players[player_num].ships[start_pos_x][
                                    start_pos_y + i] = 1
                                current_ship.points.append(
                                    [start_pos_x, start_pos_y + i])
                            else:
                                self.players[player_num].ships[start_pos_x + i][
                                    start_pos_y] = 1
                                current_ship.points.append(
                                    [start_pos_x + i, start_pos_y])

                        self.players[player_num].ship_arr.append(current_ship)

                    if need_rerun:
                        break

            if need_rerun:
                break

        if need_rerun:
            self.players = [
                TPlayer(len(self.ships)),
                TPlayer(len(self.ships))
            ]
            self.put_ships_auto(player_num)

        return None

    def strike(self, player_num, x, y):
        """Strike at coordinates (x, y) for a given player."""
        if self.players[player_num].ships[x][y] == 0:
            self.players[player_num].show[x][y] = 2  # Miss
            return 0
        else:
            self.players[player_num].show[x][y] = 3  # Hit
            ship_arr = self.players[player_num].ship_arr
            # Iterate through each ship in the player's array
            for i in range(len(ship_arr)):
                if [x, y] in ship_arr[i].points:
                    ship_arr[i].lives -= 1
                    if ship_arr[i].lives == 0:
                        # Ship sunk! Update display and decrease alive count
                        for j in ship_arr[i].points:
                            # Update the display for the ship's points
                            # Note: PEP8 suggests consistent spacing around operators/keywords
                            # Adjusted for consistency with existing logic structure
                            self.players[player_num].show[j[0] - 1][j[1] - 1] = 2
                            self.players[player_num].show[j[0]][j[1] - 1] = 2
                            self.players[player_num].show[j[0] + 1][j[1] - 1] = 2
                            self.players[player_num].show[j[0] - 1][j[1]] = 2
                            self.players[player_num].show[j[0]][j[1]] = 4  # Sunk marker (or specific value)
                            self.players[player_num].show[j[0] + 1][j[1]] = 2
                            self.players[player_num].show[j[0] - 1][j[1] + 1] = 2
                            self.players[player_num].show[j[0]][j[1] + 1] = 2
                            self.players[player_num].show[j[0] + 1][j[1] + 1] = 2

                        # After sinking, mark all points as sunk (value 4)
                        for j in ship_arr[i].points:
                            self.players[player_num].show[j[0]][j[1]] = 4
                        self.players[player_num].alive_count -= 1
                        return 1  # Ship sunk
                    else:
                        return 2

    def bot_strike(self) -> int:
        """
        Bot strikes against Player 1's ships (assuming Player 1 is the target).
        Returns 0 if no strike occurred, 1 if a strike occurred.
        """
        wound_coords = []
        result = 0
        # Check all 10x10 grid points for existing hits (value 3)
        for i in range(10):
            for j in range(10):
                if self.players[1].show[i][j] == 3:
                    wound_coords.append([i, j])
        if not wound_coords:
            # If no hits are known, strike at a random, un-missed (0) location
            h_ind = random.randint(0, 9)
            v_ind = random.randint(0, 9)
            while self.players[1].show[v_ind][v_ind] != 0:
                h_ind = random.randint(0, 9)
                v_ind = random.randint(0, 9)

            result = self.strike(1, h_ind, v_ind)
        else:
            # If hits are known, try to strike adjacent to the known hits first
            for wound in wound_coords:
                # Check North (row - 1)
                if self.players[1].show[wound[0] - 1][wound[1]] == 0:
                    result = self.strike(1, wound[0] - 1, wound[1])
                    break
                # Check South (row + 1)
                if self.players[1].show[wound[0] + 1][wound[1]] == 0:
                    result = self.strike(1, wound[0] + 1, wound[1])
                    break
                # Check West (col - 1)
                if self.players[1].show[wound[0]][wound[1] - 1] == 0:
                    result = self.strike(1, wound[0], wound[1] - 1)
                    break
                # Check East (col + 1)
                if self.players[1].show[wound[0]][wound[1] + 1] == 0:
                    result = self.strike(1, wound[0], wound[1] + 1)
                    break

        time.sleep(.3)
        if result == 0:
            return 0
        else:
            return 1
