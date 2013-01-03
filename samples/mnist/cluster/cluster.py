import os
import re
import cluster_config

from sh import starcluster, ssh, ec2_reboot_instances
from ConfigParser import RawConfigParser


def get_key():
    conf = RawConfigParser()

    fname = os.path.expanduser("~/.starcluster/config")
    f = open(fname, "r")
    conf.readfp(f)
    f.close()

    return os.path.expanduser(conf.get("key clusterkey", "KEY_LOCATION"))


def check_ssh(key, dns):
    try:
        res = ssh("-oConnectTimeout=15", "-i", key, cluster_config.USER + "@" + dns, "whoami")
        return True
    except:
        return False


def ssh_command(key, dns, command):
    try:
        res = ssh("-oConnectTimeout=15", "-i", key, cluster_config.USER + "@" + dns, command)
        return res
    except Exception as e:
        print "Command failed", e
        return 


def reboot_node(node_id, instance_id, dns):
    print "Restarting node", node_id, instance_id
    try:
        ec2_reboot_instances(instance_id)
    except:
        print "Failed rebooting instance", instance_id


def get_nodes():
    out = starcluster("listclusters")

    node_re = re.compile("^\s+(node\d+) running ([-\w]+) ([-.\w]+)")
    nodes = []
    for line in out:
        match = node_re.match(line)
        if match:
            nodes.append((match.group(1), match.group(2), match.group(3)))

    return nodes
