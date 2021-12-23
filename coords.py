
def generate_2d_normal(xmax, ymax):
    for y in range(ymax):
        for x in range(xmax):
            yield (x, y)

def generate_2d(xmax, ymax, x_first=True):
    for (x, y) in generate_2d_normal(xmax, ymax):
        yield (x, y) if x_first else (y, x)
