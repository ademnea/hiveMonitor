import os
import shutil
from distutils.dir_util import copy_tree
import sys
import subprocess

build_sys = "all"
if len(sys.argv) > 1:
    if sys.argv[1] in ["raspbian", "linux", "server"]:
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
    if not os.path.isdir("dist/Raspcapture-client-"+dist) or not os.path.isfile("dist/Raspcapture-client-"+dist+".zip"):
        copy_tree("Raspcapture-client", "dist/Raspcapture-client-"+dist)
        os.chdir(new_dir+'/Raspcapture-client-'+dist)
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
copy_tree("Raspcapture-server", "dist/Raspcapture-server")

if build_sys == "all":
    exit(0)

if build_sys == "server":
    os.chdir(new_dir)
    shutil.rmtree('Raspcapture-client-linux', ignore_errors=True)
    shutil.rmtree('Raspcapture-client-raspbian', ignore_errors=True)
    os.chdir('..')
    os.chdir('..')
    copy_tree("Raspcapture/dist/Raspcapture-server", "Raspcapture-server")

    shutil.rmtree('Raspcapture', ignore_errors=True)
    copy_tree("Raspcapture-server", "Raspcapture")
    shutil.rmtree('Raspcapture-server', ignore_errors=True)
    exit(0)

elif build_sys == "raspbian":
    os.chdir(new_dir)
    shutil.rmtree('Raspcapture-client-linux', ignore_errors=True)
    shutil.rmtree('Raspcapture-server', ignore_errors=True)
    os.chdir('..')
    os.chdir('..')
    copy_tree("Raspcapture/dist/Raspcapture-client-raspbian", "Raspcapture-client-raspbian")

    shutil.rmtree('Raspcapture', ignore_errors=True)
    copy_tree("Raspcapture-client-raspbian", "Raspcapture")
    shutil.rmtree('Raspcapture-client-raspbian', ignore_errors=True)
    exit(0)

else:
    os.chdir(new_dir)
    shutil.rmtree('Raspcapture-client-raspbian', ignore_errors=True)
    shutil.rmtree('Raspcapture-server', ignore_errors=True)
    os.chdir('..')
    os.chdir('..')
    copy_tree("Raspcapture/dist/Raspcapture-client-linux", "Raspcapture-client-linux")

    shutil.rmtree('Raspcapture', ignore_errors=True)
    copy_tree("Raspcapture-client-linux", "Raspcapture")
    shutil.rmtree('Raspcapture-client-linux', ignore_errors=True)
    exit(0)

