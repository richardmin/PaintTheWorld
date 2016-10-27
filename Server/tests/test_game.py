import pytest
from painttheworld.game import GameState, RED, BLUE

# gridsize
size = 10
test_coords = [(x,y) for x in range(size) for y in range(size)]

# create two empty grids and color one coordinate between them
@pytest.mark.parametrize("coordinate", test_coords)
def test_gamestate_diff(coordinate):
    gs1 = GameState(size)
    gs2 = GameState(size)
    gs2.update(coordinate, RED)
    diff = GameState.diff(gs1, gs2)
    assert diff == [(coordinate, RED)]
