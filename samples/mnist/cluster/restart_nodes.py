import multiprocessing
from cluster import *
import cluster_config


def start():
    pool = multiprocessing.Pool(8)

    nodes = get_nodes()

    pool.map(restart_node, nodes)
    pool.close()
    pool.join()


def restart_node((node_id, instance_id, dns)):
    key = get_key()

    if not check_ssh(key, dns):
        print "FAILED", node_id, instance_id, dns, "NOT REACHABLE"
        return False

    cmd = "tmux kill-session -t worker"

    ssh_command(key, dns, cmd)

    cmd = "tmux new -d -s worker %s" % (cluster_config.START_NODE)

    ssh_command(key, dns, cmd)

    return True


start()
