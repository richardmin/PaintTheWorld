import pytest
from painttheworld.game import GameState
from painttheworld.constants import Team
from painttheworld import constants


# gridsize
size = 10
test_coords = [(x,y) for x in range(size) for y in range(size)]

# create two empty grids and color one coordinate between them
@pytest.mark.parametrize("coordinate", test_coords)
def test_gamestate_diff(coordinate):
    gs1 = GameState(size, constants.gridsize)
    gs2 = GameState(size, constants.gridsize)

    # No Color to Red
    gs2.update(coordinate, Team.RED)
    diff = GameState.diff(gs1, gs2)
    assert diff == [(coordinate, Team.RED)]
    # Red to Blue
    gs2.update(coordinate, Team.BLUE)
    diff = GameState.diff(gs1, gs2)
    assert diff == [(coordinate, Team.BLUE)]
    # Blue to Red
    gs2.update(coordinate, Team.RED)
    diff = GameState.diff(gs1, gs2)
    assert diff == [(coordinate, Team.RED)]

# @pytest.mark.parametrize("coordinate", test_coords)
# def test_convert(coordinate):
#     gs = GameState(size, constants.gridsize)
#     for i in range(0, constants.lobby_size):
#         gs.add_user(10,10)
#     assert gs.project(10, 10) == 11,11