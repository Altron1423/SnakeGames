
Grass = 1
Wall = 2
Fruit = 3

def run(snake, map):
    p = map.PosInfo(0, 1)
    if map.PosInfo(0, 1) == Wall and map.PosInfo(1, 0) != Wall:
        snake.Right()
        return
    ...