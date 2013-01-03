import multiprocessing
from cluster import *
import cluster_config


def start():
    pool = multiprocessing.Pool(8)

    nodes = get_nodes()

    pool.map(fix_nfs, nodes)
    pool.close()
    pool.join()


def fix_nfs((node_id, instance_id, dns)):
    key = get_key()

    cmd = "mount /home"

    if not ssh_command(key, dns, cmd):
        print "FAILED", node_id, instance_id, dns, "NOT REACHABLE"

    #print "FAILED", node_id, instance_id, dns
    #reboot_node(node_id, instance_id, dns)
    return False



start()


