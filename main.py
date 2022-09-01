from flask import Flask
from flask import request
from git import Git
#from mylogger import mylogger as mylogger2
import argparse
import os
import json
import configparser
import copy

config = configparser.ConfigParser()
config_global = None

git = Git("/bin/git")
cmdargs = None
scriptpath = os.path.abspath(os.curdir)

def init():
    global cmdargs, git, config, config_global

    parser = argparse.ArgumentParser()
    parser.add_argument("--localrepo", default="./localrepo")
    parser.add_argument("--config", default="./config")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=9999, type=int)
    args = parser.parse_args()
    cmdargs = args

    # Creaing local repo
    if os.path.exists(cmdargs.localrepo):
       # mylogger2.warning("dir '%s' already exists!" % cmdargs.localrepo)
        close()
    print(f"New dir at ({cmdargs.localrepo})")
    os.mkdir(cmdargs.localrepo)
 
    # Parsing 'config' file
    config.read(cmdargs.config)
    git.init(path=cmdargs.localrepo, branch=config['global']["branch"])
    config_global = copy.deepcopy(config['global'])
    config.remove_section('global')

    try:
        os.chdir(cmdargs.localrepo)

        # Uniting remote repostories into local repo
        for section in config.sections():
            remote = config[section]
            git.remote("add", section, url=remote['url'])
            git.pull(section, config_global["branch"], rebase=True) 
    except:
        os.chdir(scriptpath)


def close():
    # Deleting an repo
    for root, dirs, files in os.walk(cmdargs.localrepo, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for direct in dirs:
            os.rmdir(os.path.join(root, direct))
    os.rmdir(cmdargs.localrepo)


app = Flask(__name__)


@app.route("/", methods=["POST"])
def general():
    payload = json.loads(request.form.to_dict()['payload'])

    if request.headers['X-GitHub-Event'] == 'push':
        repository = None
        for section in config.sections():
            repository = config[section] if (config[section]['url'] == payload['repository']['ssh_url']) else repository
            if repository: break
        if not repository: return
        
        try:
            os.chdir(cmdargs.localrepo) 
            git.pull(repo=section, branch=config_global['branch'], commit=False)
            for section in config.sections():
                remote = config[section]
                if remote == repository: continue
                git.push(repo=section, branch=config_global['branch'])
        finally:
            os.chdir(scriptpath)
    return "Error"


try:
    init()
    app.run(host=cmdargs.host, port=cmdargs.port)
finally:
    close()
