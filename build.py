import os
import shutil
from distutils.dir_util import copy_tree
import sys

build_sys = "raspbian"
if len(sys.argv) > 1:
    if sys.argv[1] in ["raspbian", "linux"]:
        build_sys = sys.argv[1]
    else:
        print("Error: Supplied wrong arguments!")
        exit(1)

print("Building for "+build_sys)

cwd = os.getcwd()
new_dir = cwd+'/dist'

if not os.path.isdir(new_dir):
    os.mkdir(new_dir)

distributions = ['linux', 'raspbian']

for dist in distributions:
    if not os.path.isdir("dist/hiveMonitor-"+dist) or not os.path.isfile("dist/hiveMonitor-"+dist+".zip"):
        copy_tree("hiveMonitor", "dist/hiveMonitor"+dist)
        os.chdir(new_dir+'/hiveMonitor-'+dist)
        files = os.listdir()
        for file in files:
            if file.startswith(distributions[abs(distributions.index(dist)-1)]):
                os.remove(file)

        os.rename(dist+'_capture.py', 'device_capture.py')
        os.rename(dist+'_install.sh', 'install.sh')
        shutil.rmtree('.git', ignore_errors=True)
        shutil.rmtree('__pycache__', ignore_errors=True)
        shutil.rmtree('jm', ignore_errors=True)
        os.chdir('..')
        os.chdir('..')

if build_sys == "raspbian":
    os.chdir(new_dir)
    shutil.rmtree('hiveMonitor-linux', ignore_errors=True)
    os.chdir('..')
    os.chdir('..')
    copy_tree("RhiveMonitor/dist/hiveMonitor-raspbian", "hiveMonitor-raspbian")

    shutil.rmtree('hiveMonitor', ignore_errors=True)
    copy_tree("hiveMonitor-raspbian", "hiveMonitor")
    shutil.rmtree('hiveMonitor-raspbian', ignore_errors=True)
    exit(0)

else:
    os.chdir(new_dir)
    shutil.rmtree('hiveMonitor-raspbian', ignore_errors=True)
    os.chdir('..')
    os.chdir('..')
    copy_tree("hiveMonitor/dist/hiveMonitor-linux", "hiveMonitor-linux")

    shutil.rmtree('hiveMonitor', ignore_errors=True)
    copy_tree("hiveMonitor-linux", "hiveMonitor")
    shutil.rmtree('hiveMonitor-linux', ignore_errors=True)
    exit(0)

