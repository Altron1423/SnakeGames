
Grass = 1
Wall = 2
Fruit = 3

def run(snake, map):
    p = map.PosInfo(0, 1)
    print(p)
    print(p == Grass)
    if map.PosInfo(0, 1) == Wall:
        snake.Right()
        return
    ...