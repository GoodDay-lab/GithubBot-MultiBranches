from flask import Flask
from flask import request
from git import Git
from mylogger import mylogger
from defconfig import load_defconfig, create_config
import argparse
import os
import json
import configparser
import copy
import logging

config = configparser.ConfigParser()
config_global = None

app = Flask(__name__)
git = Git("/bin/git")
cmdargs = None

def init():
    global cmdargs, git, config, config_global, app

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./config")
    args = parser.parse_args()
    cmdargs = args
    
    # Parsing 'config' file
    config.read(cmdargs.config)
    config_global = copy.deepcopy(config["global"])
    config.remove_section("global")
    config_global = create_config(config_global)

    # Setting loggers
    loggers_t = ["error", "info", "debug"]
    levels = {"error": logging.ERROR, 
              "info": logging.INFO,
              "debug": logging.DEBUG}
    formatter = logging.Formatter("[%(asctime)s - %(name)s] %(levelname)s:  %(message)s")
    for logger_t in loggers_t:
        if (f"{logger_t} log" in config_global):
            handler = logging.FileHandler(config_global["%s log" % logger_t])
            handler.setFormatter(formatter)
            handler.setLevel(levels[logger_t])
            mylogger.addHandler(handler)

    # Setting flask logger
    logger = logging.getLogger("werkzeug")
    if (f"access log" in config_global):
        
        # Clear flask logger handlers
        logger.handlers = []

        handler = logging.FileHandler(config_global["access log"])
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
    
    # Creaing local repo
    if os.path.exists(config_global["repository"]):
        mylogger.warning("Directory '%s' already exists!" % config_global["repository"])
        close()
    git.init(path=config_global["repository"], branch=config_global["branch"])
    mylogger.info("Creaing directory on (%s)" % config_global["repository"])
 
    try:
        os.chdir(config_global['repository'])

        # Uniting remote repostories into local repo
        for section in config.sections():
            remote = config[section]
            git.remote("add", section, url=remote['url'])
            git.pull(section, config_global["branch"], rebase=True)
    except:
        os.chdir(config_global["workdirectory"])
    mylogger.info("Successfuly finished function 'init'")


def close():
    # Deleting an repo
    for root, dirs, files in os.walk(config_global["repository"], topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for direct in dirs:
            os.rmdir(os.path.join(root, direct))
    os.rmdir(config_global["repository"])


def get_protocol_name(url):
    if (url.startswith("git@github.com:")):
        return "ssh"
    else:
        return url[:url.find("://")]

def get_repository_config(payload):
    global config
    for remote in config:
        if (remote == "DEFAULT"): continue
        conf = config[remote]
        mylogger.info("func 'get_repository_config': conf: %s" % str(conf))
        protocol = get_protocol_name(conf["url"])
        if (conf["url"] == payload["repository"]["%s_url" % protocol]):
            break
    return [remote, conf]


@app.route("/", methods=["POST"])
def general():
    payload = json.loads(request.form.to_dict()['payload'])

    if request.headers['X-GitHub-Event'] == 'push':
        section, repository = get_repository_config(payload)
        mylogger.info("Got push on local repository (%s)\n" % str(section),
                      "Repository config %s" % str(repository))
        try:
            os.chdir(config_global["repository"]) 
            git.pull(repo=section, branch=config_global['branch'], commit=False)
            for section in config.sections():
                remote = config[section]
                if remote == repository: continue
                git.push(repo=section, branch=config_global['branch'])
        finally:
            os.chdir(config_global["workdirectory"])
    return "Error"

if __name__ == '__main__':
    init()
    try:
        app.run(host=config_global["host"], port=config_global["port"])
    finally:
        close()
