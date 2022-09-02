from mylogger import mylogger
import subprocess

class Git:
    default_app = "/bin/git"
    def __init__(self, app=None):
        if (not app):
            mylogger.warning("You doesn't specified a full path to git app.\n"
                         f"Current path to git app is \"{self.default_app}\".")
            self.app = self.default_app
        else:
            self.app = app
    
    def checkout(self, branch, new=False):
        cmd = [self.app, "checkout", branch]
        if (new): cmd.append("-b")
        self.run_bin(cmd)

    def push(self, repo=None, branch=None, force=None):
        cmd = [self.app, "push"]
        if (force): cmd.append("--force")
        if (repo): cmd.insert(2, repo)
        if (branch): cmd.insert(3, branch)
        self.run_bin(cmd)

    def pull(self, repo=None, branch=None, commit=False, rebase=False, force=None):
        cmd = [self.app, "pull"]
        if (repo): cmd.append(repo)
        if (branch): cmd.append(branch)
        if (rebase): cmd.append(f"--rebase={str(rebase).lower()}")
        if (force): cmd.append(force)
        cmd.append("--no-edit")
        cmd.append("--commit" if commit else "--no-commit")
        self.run_bin(cmd)

    def remote(self, command, name, url=None, branch=None, master=None, force=None):
        cmd = [self.app, "remote"]
        cmd.append(command)
        cmd.append(name)
        if (url): cmd.append(url)
        if (branch): cmd += ["-t", f"{branch}"] 
        if (master): cmd += ["-m", f"{master}"]
        if (force): cmd.append(f"-f")
        self.run_bin(cmd)

    def config(self, option, value=None, level=None, unset=False, replace=False):
        cmd = [self.app, "config", option]
        if (value): cmd.insert(3, value)
        if (level): cmd.append(level)
        if (unset): cmd.append("--unset-all")
        if (replace): cmd.append("--replace-all")
        self.run_bin(cmd)

    def add(self, path, force=None):
        cmd = [self.app, "add", path]
        if (force): cmd.append("--force")
        self.run_bin(cmd)

    def commit(self, path=None, _all=False, msg=None, author=None):
        cmd = [self.app, "commit"]
        if (_all): cmd.append("-a")
        if (msg): cmd += ["-m", f"{msg}"]
        if (path): cmd.insert(2, path)
        if (author): cmd += ["--author", f"{author}"]
        cmd.append("--no-edit")
        self.run_bin(cmd)

    def init(self, path=".", branch=None):
        cmd = [self.app, "init", path]
        if (branch): cmd += ["-b", f"{branch}"]
        self.run_bin(cmd)

    def run_bin(self, cmd):
        mylogger.warning(f"Executing: \"{' '.join(cmd)}\".");
        try:
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except:
            mylogger.warning(f"Process \"{' '.join(cmd)}\" failed.")
            return
        mylogger.warning(f"Process \"{' '.join(process.args)}\" returned "
                         f"({process.returncode})")

        
