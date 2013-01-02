import pymurder
import subprocess

master = 'ec2-50-19-54-37.compute-1.amazonaws.com'
workers = ['ec2-54-242-91-188.compute-1.amazonaws.com']


def sendFiles(master):
    """
    Rsyncs the pyhoard files to the master for creation of the torrent
    to be used to deploy to all peers
    """

    callSpec = ['starcluster', 'put', 'lark', '.' 'pyvotune']
#callSpec = ['/usr/bin/rsync', "-avz", "--delete", "-e",
                #"ssh -i ~/.ssh/ec2key.pem -oStrictHostKeyChecking=no",
                #"~/build1/",
                #"%s@%s:%s" % ('ubuntu', master,
                              #'~')]
    proc = subprocess.Popen(callSpec)
    proc.wait()

pym = pymurder.PyMurder({
    'tracker': [master],
    'seeder': [master],
    'peer': workers + [master],
    'remote_murder_path': '/opt/local/murder',
    'pymurder_home': '.',
    'user': 'root',
    'key_filename': '~/.ssh/clusterkey.rsa'
})

#pym.distribute_files()
#pym.start_tracker()
#pym.create_torrent('.', '/opt/local/murder')

sendFiles(master)  # Send the build to the master server

#pym.start_seeding('pyvotune')
#pym.start_peering('pyvotune', '/opt/local/murder')
#pym.stop_all_peering()
#pym.stop_seeding('pyvotune')
#pym.stop_tracker()


