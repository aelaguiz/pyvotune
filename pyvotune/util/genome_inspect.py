import itertools


def side_by_side(genomes, genome_max_width=40, screen_width=150):
    genome_padding = 3
    genomes_per_row = int(screen_width / (genome_max_width + 3))

    new_lines = []
    for row in chunks(genomes, genomes_per_row):
        new_lines += _side_by_side(row, genome_max_width, screen_width)

    return "\n".join(new_lines)


def _side_by_side(genomes, genome_max_width=40, screen_width=150):
    rep_lines = []
    for genome in genomes:
        str_rep = repr(genome)

        rep_lines.append(str_rep.split("\n"))

    new_lines = []
    for lines in itertools.izip_longest(*rep_lines):
        new_line = ""

        for line in lines:
            if new_line:
                new_line += " "

            if line:
                line = line.replace("\t", "    ")
                part = line[:genome_max_width].ljust(genome_max_width)
                new_line += part
            else:
                new_line += " " * genome_max_width

            new_line += " |"

        new_lines.append(new_line)

    return new_lines


def child_stats(parents, children, stats):
    parents = {p.genome_id: p for p in parents}

    for child in children:
        stats['num_children'] += 1

        if child.parent_id:
            parent = parents[child.parent_id[len(child.parent_id)-1]]
        else:
            parent = child

        if parent == child:
            stats['num_same'] += 1

        if len(child) > len(parent):
            stats['num_longer'] += 1
        elif len(child) < len(parent):
            stats['num_shorter'] += 1
        else:
            stats['num_same_length'] += 1

    return stats



def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

