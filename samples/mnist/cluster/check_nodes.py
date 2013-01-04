import multiprocessing
from cluster import *
import cluster_config
import time


def start():
    pool = multiprocessing.Pool(8)

    nodes = get_nodes()

    pool.map(test_node, nodes)
    pool.close()
    pool.join()


def test_node((node_id, instance_id, dns)):
    key = get_key()

    if check_ssh(key, dns):
        cmd = "tmux ls"
        if ssh_command(key, dns, cmd):
            print "OK", node_id
            return True
        else:
            print "Node is up, not running", node_id
    else:
        print "FAILED", node_id, instance_id, dns
        reboot_node(node_id, instance_id, dns)

        print "Waiting for", node_id, "to come up"
        while True:
            if check_ssh(key, dns):
                print "SSH Is up for", node_id
                break

            time.sleep(10)

    print "Starting", node_id

    cmd = "tmux new -d -s worker %s" % (cluster_config.START_NODE)
    ssh_command(key, dns, cmd)

    return True



start()
