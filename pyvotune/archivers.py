import inspyred
from pyvotune.log import logger

try:
    import cPickle as pickle
except ImportError:
    import pickle

log = logger()


def pickle_wrap_archiver(random, population, archive, args):
    underlying_archiver = args['underlying_archiver']

    new_archive = underlying_archiver(
        random, population, archive, args)

    archive_path = args['archive_path']

    f = open(archive_path, "wb")
    pickle.dump(new_archive, f)
    f.close()

    for i, ind in enumerate(new_archive):
        log.info("Archiving #%d:\n%s" % (i, ind))

    return new_archive
