import subprocess

class Xflux(object):
    def __init__(self):
        pass
    def update(self, lo, la, te):
        try:
            while True:
                getFluxPid = "pgrep xflux"
                fluxPID = subprocess.check_output(getFluxPid.split())
                killFlux = "kill -9 "+fluxPID
                subprocess.call(killFlux.split())
        except subprocess.CalledProcessError:
            pass
        finally:
            runFlux = "xflux -l %s -g %s -k %s" % (lo, la, te)
            subprocess.call(runFlux.split())
