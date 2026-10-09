"""Grupo 1311 Pareja 06
    Autores: Jaime Leon y Daniel Laiz
"""


from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from tournament import (
    StudentHeuristic,
)


def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)

#diferencia de fichas
def _coin_diff(state: TwoPlayerGameState):
    board = state.board
    me_label = state.player_max.label
    p1_label = state.player1.label
    p2_label = state.player2.label
    opp_label = p2_label if me_label == p1_label else p1_label
    my_coins = sum(1 for i in board.values() if i == me_label)
    opp_coins = sum(1 for i in board.values() if i == opp_label)
    return my_coins - opp_coins


#diferencia de esquinas capturadas
def _corner_diff(state: TwoPlayerGameState):
    board = state.board
    me_label = state.player_max.label
    p1_label = state.player1.label
    p2_label = state.player2.label
    opp_label = p2_label if me_label == p1_label else p1_label
    height = state.game.height
    width = state.game.width
    diff = 0
    for corner in [(1, 1), (1, height), (width, 1), (width, height)]:
        owner = board.get(corner)
        if owner == me_label:
            diff +=1
        elif owner == opp_label:
            diff -= 1
    return diff


def _danger_zones_diff(state: TwoPlayerGameState):
    board = state.board
    me_label = state.player_max.label
    p1_label = state.player1.label
    p2_label = state.player2.label
    opp_label = p2_label if me_label == p1_label else p1_label
    height = state.game.height
    width = state.game.width
    danger_zones = [(1, 2), (2, 1), (2, 2), (1, height-1), (2, height), (2, height-1), (width-1, 1), (width, 2), (width-1, 2), (width-1, height-1), (width-1, height), (width, height-1)] 
    diff = 0

    for zone in danger_zones:
        owner = board.get(zone)
        if owner == me_label:
            diff -=1
        elif owner == opp_label:
            diff += 1

    return diff



#Solo diferencia de fichas
class Solution1(StudentHeuristic):
    def get_name(self) -> str:
        return "coin_diff"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return _coin_diff(state)


#diferencia de fichas mas un bonus por esquina capturada
class Solution2(StudentHeuristic):
    def get_name(self) -> str:
        return "coin_and_corners"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return _coin_diff(state) + 25*_corner_diff(state)

#igual que el anterior pero dando mas peso a las esquinas
class Solution3(StudentHeuristic):
    def get_name(self) -> str:
        return "weighted_coin_corners"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return _coin_diff(state) + 30*_corner_diff(state)

#tiene en cuenta las esquinas pero tambien las zonas de peligro que son las casillas adyacentes a las esquinas
class Solution4(StudentHeuristic):
    def get_name(self) -> str:
        return "weighted_coin_corners_danger"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return _coin_diff(state) + 30*_corner_diff(state) + 15*_danger_zones_diff(state)