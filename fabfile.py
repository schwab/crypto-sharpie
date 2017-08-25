import os
import sys
from datetime import datetime
from fabric.api import *
from fabric.contrib.files import exists
from cube_server.repo.coin_data_importer import CoinDataImporter
from cube_server.provider.config_provider import ConfigProvider

test_files = ["cube_server.tests.test_downloader","cube_server.tests.test_coin_data_importer"]
dt_start = datetime(2015,1,1)
dt_end = datetime.now()
folders = ["data"]
env.name = "dev"

def clean_pyc():
    command = 'find . -name "*.pyc" -exec git rm -f "{}" \;'
    print "Remove any committed pyc files..."
    local(command)
@task(alias="docker-compose")
def dc(command="ps"):
    run_commands(["docker-compose %s" % (command)])
@task(alias="dep")
def dependencies():
    local("sudo pip install pandas")

@task(alias="import")
def import_data(import_type="exchange"):
    config_provider = ConfigProvider(required_settings=["connection"])
    cdi = CoinDataImporter(config_provider.data["connection"], \
        data_dir="./cube_server/data")
    if "exchange" in import_type:
        cdi.import_exchanges()
        
@task
def init():
    for f in folders:
        if not os.path.isdir(f):
            print "Creating directory %s/%s" % (os.getcwd(), f)
            local("mkdir %s/%s" % (os.getcwd(), f))
@task
def restart(names):
    services = split_comma(names)
    commands = []
    for service in services:
        commands.append("docker-compose restart %s" % (service))
    run_commands(commands)    

def run_commands(commands, warn_only=False):
    """
    Run one or more commands based on the current env.name (dev is local, otherwise remote)
    """
    if "dev" in env.name:
        #os.chdir(run_dir)
        for c in commands:
            if warn_only:
                with settings(warn_only=True):
                    local(c)
            else:
                local(c)
    else:
        #with cd(run_dir):
        for c in commands:
            if warn_only:
                with settings(warn_only=True):
                    run(c)
            else:
                run(c) 
def split_comma(names=""):
    return names.split(',')

@task(alias="s")
def stats():
    """Run docker stats to show running container and their resource usage"""
    run_commands(["docker stats $(docker ps --format={{.Names}})"])

@task
def test():
    for f in test_files:
        local("python -m unittest %s" % (f) )
@task
def up(services=None, detached=False):
    d = "-d" if detached else ""
    with settings(warn_only=True):
        if not services is None:
            srv_list = []
            if len(services) > 0:
                srv_list = split_comma(services)
            for service in srv_list:
                local("docker-compose build %s" % (service))
                local("docker-compose pull %s" % (service))
                local("docker-compose up %s --remove-orphans %s " % (d, service))
        else:
            local("docker-compose build")
            local("docker-compose pull")
            local("docker-compose up %s --remove-orphans" % (d))



