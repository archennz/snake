from game import players
from game.world import nrow, width

class TestApple:
    def test_apple_inside_world(self):
        apple = players.Apple()
        assert apple.x in range(0, nrow-1)
        assert apple.y in range(0, width-1)
        
    
