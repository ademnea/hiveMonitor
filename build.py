import os
import shutil
from distutils.dir_util import copy_tree
cwd = os.getcwd()
new_dir = cwd+'/dist'

if not os.path.isdir(new_dir):
    os.mkdir(new_dir)
if not os.path.isfile('dist/Raspcapture-server.zip'):
    shutil.make_archive('dist/Raspcapture-server', 'zip', 'Raspcapture-server')

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
        shutil.make_archive('Raspcapture-client-'+dist, 'zip', 'Raspcapture-client-'+dist)
        shutil.rmtree('Raspcapture-client-'+dist)
        os.chdir('..')
