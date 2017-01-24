"""## general notes
- do i time everything with python or gphoto?
- possibility of running multiple cameras at once [parallax?]


## useful commands
http://www.gphoto.org/doc/manual/ref-gphoto2-cli.html

debugging:
--debug --debug-logfile FILENAME --debug-loglevel [ERROR, DEBUG, DATA, ALL] <-- ALL is default

possibly use to determine when something is complete
--hook-script FILENAME
"""

## this returns subprocess output as a list
from subprocess import Popen, PIPE
child = Popen(["gphoto2", "--list-config"], stdout=PIPE)
results = child.communicate()[0].split()
