import subprocess

class Xflux(object):
    def __init__(self):
        pass
    def update(self, lo, la, te):
        try:
            while True:
                bash_flux_pid = "pgrep xflux"
                flux_pid = subprocess.check_output(bash_flux_pid.split())
                bash_kill_flux = "kill -9 "+flux_pid)
                subprocess.call(bash_kill_flux.split())
        except subprocess.CalledProcessError:
            pass
        finally:
            bash_run_flux = "xflux -l %s -g %s -k %s" % (lo, la, te)
            subprocess.call(bash_run_flux.split())
