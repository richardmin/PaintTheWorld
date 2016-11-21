import pytest
from painttheworld.game import GameState
from painttheworld.constants import RED, BLUE
from painttheworld import constants


# gridsize
size = 10
test_coords = [(x,y) for x in range(size) for y in range(size)]

# create two empty grids and color one coordinate between them
@pytest.mark.parametrize("coordinate", test_coords)
def test_gamestate_diff(coordinate):
    gs1 = GameState(size, constants.gridsize)
    gs2 = GameState(size, constants.gridsize)
    gs2.update(coordinate, RED)
    diff = GameState.diff(gs1, gs2)
    assert diff == [(coordinate, RED)]

@pytest.mark.parameterize()
def test_convert(coordinate):
    gs = GameState(size, constants.gridsize)
    for i in range(0, constants.lobby_size):
        gs.add_user(10,10)
    assert gs.project(10, 10) == 11,11