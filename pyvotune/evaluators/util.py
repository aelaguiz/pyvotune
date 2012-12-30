try:
    import cPickle as pickle
except ImportError:
    import pickle


def get_args(args):
    pickled_args = {}
    for key in args:
        try:
            pickle.dumps(args[key])
            pickled_args[key] = args[key]
        except (TypeError, pickle.PickleError, pickle.PicklingError):
            pass

    return pickled_args
