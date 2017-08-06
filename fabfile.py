import os
from fabric.api import *
from fabric.contrib.files import exists

test_files = ["cube_server.tests.test_downloader","cube_server.tests.test_coin_data_importer"]

def clean_pyc():
    command = 'find . -name "*.pyc" -exec git rm -f "{}" \;'
    print "Remove any committed pyc files..."
    local(command)

@task(alias="dep")
def dependencies():
    local("sudo pip install pandas")
@task
def test():
    for f in test_files:
        local("python -m unittest %s" % (f) )
@task
def up(detached=False):
    d = "-d" if detached else ""
    local("docker-compose up %s" % (d))



