import subprocess
import thread
import select
import time
from xceptions import Rxpt

def read_lines(x, console):
    x.stdout.readline() #<-fix, first line is garbage and crashes app sometimes,
    # causing Gtk:ERROR:/build/buildd/gtk+3.0-3.10.8/./gtk/gtktextview.c:3892:gtk_text_view_validate_onscreen: assertion failed: (priv->onscreen_validated)
    while 1:
        x.poll()
        line = x.stdout.readline()
        console.append_txt(line)
        time.sleep(0.1)

class Xflux(object):
    def kill_flux(self):
        try:
            killed_pids = ""
            old_flux_pid = None
            while 1:
                bash_flux_pid = "pgrep xflux"
                flux_pid = subprocess.check_output(bash_flux_pid.split())
                bash_kill_flux = "kill -9 "+flux_pid
                subprocess.call(bash_kill_flux.split())
                if old_flux_pid != None and old_flux_pid == flux_pid:
                    raise Rxpt("cant kill xflux process with pid: "+flux_pid+" tried: "+bash_kill_flux)
                old_flux_pid = flux_pid
                killed_pids += flux_pid + ", "
        except subprocess.CalledProcessError:
            return killed_pids

    def run_flux(self, lo, la, te, console):
        try:
            bash_run_flux = "xflux -l %s -g %s -k %s" % (lo, la, te)
            x = subprocess.Popen(bash_run_flux.split(), stdout=subprocess.PIPE)
            thread.start_new_thread(read_lines, (x,console))
        except Exception as e:
            raise Rxpt(e.__str__()+"\nplease install xflux and try again.\napt-get example: 'sudo apt-get install xflux'")

    def update(self, lo, la, te, console):
        self.kill_flux()
        self.run_flux(lo, la, te, console)
