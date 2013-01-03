import numpy as np


def load_mnist(num_lines=None, with_y=True, path="data/mnist_train.csv"):
    f = open(path)
    lines = f.readlines()
    f.close()

    
    X = []
    y = []
    linecount = 0
    for line in lines[:num_lines]:
        line = line.strip()
        parts = line.split(",")

        if with_y:
            X.append(parts[1:])
            y.append(parts[0])
        else:
            X.append(parts)

        linecount += 1

    X = np.array(X, dtype='float32')

    if with_y:
        y = np.array(y, dtype='int')
    else:
        y = None

    return X, y
