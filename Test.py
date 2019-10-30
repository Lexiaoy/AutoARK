def test():
    path = 'temp/screen_shot.png'

    print(path[path.rindex("/", 0, len(path)):len(path)])

test()