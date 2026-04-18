
import urwid
import boards

def status_make(line: str) -> str:
    l = len(line)
    offset = (100 - (l // 2)) // 2
    act_line = ""
    for _ in range(offset):
        act_line += " "
    act_line += line
    return act_line
class MyButton(urwid.Button):
    def __init__(self, h_ind: int, v_ind: int) -> None:
        self.h_ind = h_ind
        self.v_ind = v_ind
        super().__init__(".")
        urwid.connect_signal(self, "click", self.text_update)

    def text_update(self,bttn) -> None:
        if SeaBattle.players[0].alive_count > 0 and \
                SeaBattle.players[1].alive_count > 0:
            res = SeaBattle.strike(0, self.h_ind, self.v_ind)
            if res == 1:
                foot_a.set_text("       Alive ships - " +
                                str(SeaBattle.players[0].alive_count))
            for p in range(10):
                for q in range(10):
                    if SeaBattle.players[0].show[p][q] == 0:
                        CellsArrA[(10 * p) + q].set_label(".")
                    elif SeaBattle.players[0].show[p][q] == 2:
                        CellsArrA[(10 * p) + q].set_label("a")
                    elif SeaBattle.players[0].show[p][q] == 3:
                        CellsArrA[(10 * p) + q].set_label("X")
                    elif SeaBattle.players[0].show[p][q] == 4:
                        CellsArrA[(10 * p) + q].set_label("Y")

            # Check for Win/Turn change after Player 0's strike
            if SeaBattle.players[0].alive_count == 0:
                status_handler.set_text(status_make("YOU WIN!!!"))
                return None
            if res == 0:
                status_handler.set_text(status_make("COMPUTER TURN!!!"))
                botres = 1
                while botres == 1:
                    botres = SeaBattle.bot_strike()
                    if botres == 1:
                        foot_b.set_text("       Alive ships - " +
                                        str(SeaBattle.players[1].alive_count))
                    for r in range(0, 10):
                        for s in range(0, 10):
                            if SeaBattle.players[1].show[r][s] == 2:
                                CellsArrB[(10 * r) + s].set_text("a")
                            elif SeaBattle.players[1].show[r][s] == 3:
                                CellsArrB[(10 * r) + s].set_text("X")
                            elif SeaBattle.players[1].show[r][s] == 4:
                                CellsArrB[(10 * r) + s].set_text("Y")

                # Check for Win/Turn change after Computer's strike
                if SeaBattle.players[1].alive_count == 0:
                    status_handler.set_text(status_make("COMPUTER WIN!!!"))
                else:
                    status_handler.set_text(status_make("YOUR TURN!!!"))

    def keypress(self, size: tuple[int], key: str) -> str | None:
        parsed = super().keypress(size, key)
        if parsed in {"q", "Q"}:
            raise urwid.ExitMainLoop("Done")
        if parsed in {"s", "S"}:
            for p in range(0, 10):
                for r in range(0, 10):
                    if SeaBattle.players[0].ships[p][r] == 1:
                        CellsArrA[(10 * p) + r].set_label("X")
        return parsed

SeaBattle  = boards.TBattle()
try:
    SeaBattle.put_ships_auto(0)
    SeaBattle.put_ships_auto(1)
except:
    print("something went wrong")
    exit(1)
CellsArrA = []
CellsArrB = []
for i in range(10):
    for j in range(10):
        CellsArrA.append(MyButton(i,j))
        if SeaBattle.players[1].ships[i][j] == 1:
            CellsArrB.append(urwid.Text("H"))
        else:
            CellsArrB.append(urwid.Text("."))

def line_make(line, top, offset = 0, chgb = 0):
    l = len(line)
    if offset == 0:
        offset = (100 - (l // 2)) // 2
    act_line = ""
    for _ in range(offset):
        act_line += " "
    act_line += line
    foot_a_loc = urwid.Text(act_line)
    fill_foot_a_loc = urwid.Filler(foot_a_loc, 'top', top = top)
    if chgb == 0:
        return urwid.Padding(fill_foot_a_loc, 'center', width=100)
    if chgb == 1:
        return urwid.Padding(fill_foot_a_loc, 'center', width=100),foot_a_loc

# The following code is rewritten according to PEP-8 standard
grid_a = urwid.GridFlow(
    CellsArrA,
    cell_width=1,
    h_sep=2,
    v_sep=1,
    align='center'
)
fill_a = urwid.Filler(grid_a, 'top')
padd_a = urwid.Padding(fill_a, 'center', width=30)
foot_a = urwid.Text(
    "       Alive ships - " + str(SeaBattle.players[0].alive_count)
)
fill_foot_a = urwid.Filler(foot_a, 'top', top=1)
padd_foot_a = urwid.Padding(
    fill_foot_a,
    'right',
    width=30,
    left=10
)
fr_a = urwid.Pile([grid_a, padd_foot_a])

grid_b = urwid.GridFlow(
    CellsArrB,
    cell_width=1,
    h_sep=2,
    v_sep=1,
    align='center'
)
fill_b = urwid.Filler(grid_b, 'top')
padd_b = urwid.Padding(fill_b, 'center', width=30)
foot_b = urwid.Text(
    "       Alive ships - " + str(SeaBattle.players[1].alive_count)
)
fill_foot_b = urwid.Filler(foot_b, 'top', top=1)
padd_foot_b = urwid.Padding(
    fill_foot_b,
    'right',
    width=30,
    left=10
)
fr_b = urwid.Pile([grid_b, padd_foot_b])
grid_full = urwid.GridFlow([fr_a, fr_b], cell_width=30, h_sep=30, v_sep=1, align='center')
fill_full = urwid.Filler(grid_full, 'top')
padd_full = urwid.Padding(fill_full, 'center', width=100)

title_line = line_make("SEA BATTLE", 0)
status_line, status_handler = line_make("YOUR TURN!!!", 2, chgb=1)
help_line1 = line_make(". - unknown, a - no ship, H - your ship, X - damaged, Y - sinked", 3, 20)
help_line2 = line_make("q - exit, Enter - fire", 0)
big_pile = urwid.Pile([title_line, padd_full, status_line, help_line1, help_line2])
fill_big = urwid.Filler(big_pile, 'top')
padd_big = urwid.Padding(fill_big, 'center', width=100)
loop = urwid.MainLoop(padd_big)
loop.run()
