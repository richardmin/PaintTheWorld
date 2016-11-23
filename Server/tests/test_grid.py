import pytest
from painttheworld.grid import Grid
from painttheworld.constants import Team
from painttheworld import const


# gridsize
size = 10
test_coords = [(x,y) for x in range(size) for y in range(size)]

# create two empty grids and color one coordinate between them
@pytest.mark.parametrize("coordinate", test_coords)
def test_gamestate_diff(coordinate):
    gs1 = Grid()
    gs2 = Grid()

    # No Color to Red
    gs2.update(coordinate, Team.RED)
    diff = Grid.diff(gs1, gs2)
    assert diff == [(coordinate, Team.RED)]

    # Red to Blue
    gs2.update(coordinate, Team.BLUE)
    diff = Grid.diff(gs1, gs2)
    assert diff == [(coordinate, Team.BLUE)]

    # Blue to Red
    gs2.update(coordinate, Team.RED)
    diff = Grid.diff(gs1, gs2)
    assert diff == [(coordinate, Team.RED)]
