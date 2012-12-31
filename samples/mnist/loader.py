import numpy as np


def load_mnist(num_lines=None):
    f = open("data/mnist_train.csv")
    lines = f.readlines()
    f.close()

    
    X = []
    y = []
    linecount = 0
    for line in lines[1:num_lines if num_lines else len(lines)-1]:
        line = line.strip()
        parts = line.split(",")

        X.append(parts[1:])
        y.append(parts[0])

        linecount += 1

    X = np.array(X, dtype='float32')
    y = np.array(y, dtype='int')

    return X, y
